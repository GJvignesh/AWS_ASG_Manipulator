"""
    Program to increase the count of desired capacity of an asg.
"""
import logging
import os
import boto3
from botocore.exceptions import ClientError


class AsgCount:
    """
        Class for increasing ASG desired_count to +1
        Having functions to get desired count and increasing desired count
    """
    def __init__(self, asg_client=None) -> None:
        # Modifying the default retries behaviour {mode: standard->adaptive} (max_attempts: 5->10)
        config = boto3.session.Config(retries={"max_attempts": 10, "mode": "adaptive"})
        session = boto3.session.Session()  # initializing the boto3 session
        self.log = logging.getLogger('Asgcount')
        self.log.setLevel(os.getenv("LOG_LEVEL", "INFO"))
        try:
            # initializing the ASG session
            if not asg_client:
                self._asg = session.client("autoscaling", config=config)
                self.log.info('session initiated')
            else:
                self._asg = asg_client
        except ClientError as error:
            logging.warning(error)

    def check_scaling_policy(self, name: str) -> bool:
        """
            Used to check whether the given ASG has dynamic scaling policies or not
            Expects one parameter name of an ASG


            Parameters
            ----------
            name : str
                Name of the ASG

            Returns
            -------
            - bool
                The return value is True for success scenario, False otherwise.
        """
        response = self._asg.describe_policies(
            AutoScalingGroupName=name)
        scaling_policy = response.get('ScalingPolicies', None)
        return bool(scaling_policy)

    def get_names_filtered(self, key: str, value: str) -> list:
        """
            Returns the list of all the asg names

            Parameters
            ----------
            key : str
                Key of ASG_TAG
            value : str
                Value of ASG_TAG

            Returns
            -------
            asg_name_list : list of str
                List of ASG matched with provided key:value TAG
        """

        # Pagination to avoid long page issue
        paginator = self._asg.get_paginator('describe_auto_scaling_groups')
        iterator = paginator.paginate(PaginationConfig={'MaxItems': 100000})
        # JMESPath filter using given key:value under Tags
        filtered_asgs = iterator.search(
            'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(
                key, value)
        )
        asg_name_list = []
        for asg in filtered_asgs:
            asg_name_list.append(asg['AutoScalingGroupName'])
        self.log.debug("Total number of Asg's are = %s", str(len(asg_name_list)))
        return asg_name_list

    def get_asg_desired_max_capacity(self, asg_name: str) -> tuple:
        """
            Returns the desired and maximum capacity of provided asg_name.

            Parameters
            ----------
            asg_name : str
                Name of the ASG

            Returns
            -------
            tuple containing int (desired_cap, max_cap)
            - desired_cap : int
                desired capacity of the provided ASG
            - max_cap : int
                maximum capacity of the provided ASG
        """
        response = self._asg.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                asg_name,
            ])
        details = response.get('AutoScalingGroups', None)
        if not details:
            self.log.warning("Could not find this ASG %s", asg_name)
            return -1, -1
        else:
            desired_cap, max_cap = int(details[0]['DesiredCapacity']), int(details[0]['MaxSize'])
            self.log.info("%s Desired=%s Maximum=%s", asg_name, str(desired_cap), str(max_cap))
            return desired_cap, max_cap

    def increase_desired_capacity(self, name: str, new_count: int) -> None:
        """
            It takes two parameter ASG name and
            new desired count value for increasing the ASG to desired value.
            It doesn't return anything,

            Parameters
            ----------
            name : str
                Name of the ASG
            new_count : int
                New desired capacity

            Returns
            -------
            None
        """
        self._asg.set_desired_capacity(
            AutoScalingGroupName=name,
            DesiredCapacity=new_count,
            HonorCooldown=False
        )

    @staticmethod
    def get_filter_tags() -> tuple:
        """
            Return the filter key and filter value by
             fetching from container environment variables
             takes no argumentcmd

            Returns
            -------
            tuple containing str (filter_key, filter_value)
            - filter_key : str
                Tag name used to filter the ASG
            - filter_value : str
                Tag value used to filter the ASG
        """
        filter_key = os.getenv('ASG_TAG_NAME')
        filter_value = os.getenv('ASG_TAG_VALUE')
        return filter_key, filter_value

    def run(self) -> None:
        """
            Retrieves the names of auto-scaling groups in the current AWS account and region
            that matches with provided tag filter
            If ASG's are present, determine the desired and maximum capacity of each ASG.
            If the desired capacity is less than the maximum capacity and have scaling policy
            then increase the desired capacity by plus 1.
        """
        # fetching filter tags from container environment variables using static method defined
        filter_key, filter_value = self.get_filter_tags()
        self.log.info('Fetched Tag -> key:%s, value:%s', filter_key, filter_value)
        # retrieve ASG with only matched key:value
        asg_names = self.get_names_filtered(key=filter_key, value=filter_value)
        self.log.info('total fetched ASG: %i', len(asg_names))
        if len(asg_names) > 0:  # If only any match found
            for name in asg_names:
                # get desired and max capacity
                self.log.info('The ASG: %s', name)
                desired, max_cap = self.get_asg_desired_max_capacity(name)
                if desired < max_cap:  # if we can increase
                    if self.check_scaling_policy(name):
                        # increase desired to +1
                        self.increase_desired_capacity(name,desired+1)
                        self.log.info("Desired Capacity of %s has been increased by 1.", name)
                    else:
                        self.log.info("Scaling policy not exist for %s", name)


def _main() -> None:
    AsgCount().run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting app')
    _main()