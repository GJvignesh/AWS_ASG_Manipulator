"""
    Unit test cases for asgtest
"""
import unittest
import os
from unittest.mock import MagicMock
from asgtest import asgtest as tool


class TestAsgCount(unittest.TestCase):
    """
        Test Class for ASGCount class
    """

    def setUp(self) -> None:
        """
        overriding setUp method to create AsgCount object with mocked boto3 asg_client
        """
        super().setUp()
        self.asg_obj = tool.AsgCount(
            asg_client=MagicMock(name="asg_client")
        )

    def test_check_scaling_policy_success_one(self):
        """
        Method to validate one scaling policy scenario
        """

        # response dict to mock session.client("autoscaling").describe_policies
        describe_policies_success_response = {
            "ScalingPolicies": [
                {
                    "AutoScalingGroupName": "Demo_ASG",
                    "PolicyName": "Demo_ASG-CPUReservation-66PCVKCX4CAJ",
                    "PolicyARN": "Demo_ARN",
                    "PolicyType": "SimpleScaling",
                    "AdjustmentType": "PercentChangeInCapacity",
                    "ScalingAdjustment": 5,
                    "Cooldown": 300,
                    "StepAdjustments": [],
                    "Alarms": [
                        {
                            "AlarmName": "Demo_alarm",
                            "AlarmARN": "arn:aws:cloudwatch:us-west-2:00000000:alarm:Demo_alarm",
                        }
                    ],
                    "Enabled": True,
                }
            ],
            "ResponseMetadata": {
                "RequestId": "cbba6b94-6d72-4902-aca8-e0b128ce19ac",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "cbba6b94-6d72-4902-aca8-e0b128ce19ac",
                    "content-type": "text/xml",
                    "content-length": "3661",
                    "vary": "accept-encoding",
                    "date": "xx, xx xx 2022 16:51:26 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.asg_obj._asg.describe_policies.return_value = describe_policies_success_response
        result = self.asg_obj.check_scaling_policy('Demo_ASG')
        self.assertTrue(result)

    def test_check_scaling_policy_success_two(self):
        """
        Method to validate more than one scaling policy scenario
        """

        # response dict to mock session.client("autoscaling").describe_policies
        describe_policies_success_response = {
            "ScalingPolicies": [
                {
                    "AutoScalingGroupName": "Demo_ASG_1",
                    "PolicyName": "Demo_ASG_1-CPUReservation-66PCVKCX4CAJ",
                    "PolicyARN": "Demo_ARN_1",
                    "PolicyType": "SimpleScaling",
                    "AdjustmentType": "PercentChangeInCapacity",
                    "ScalingAdjustment": 5,
                    "Cooldown": 300,
                    "StepAdjustments": [],
                    "Alarms": [
                        {
                            "AlarmName": "Demo_alarm_1",
                            "AlarmARN": "arn:aws:cloudwatch:us-west-2:00000000:alarm:Demo_alarm_1",
                        }
                    ],
                    "Enabled": True,
                },
                {
                    "AutoScalingGroupName": "Demo_ASG_2",
                    "PolicyName": "Demo_ASG_2-CPUReservation-66PCVKCX4CAJ",
                    "PolicyARN": "Demo_ARN_2",
                    "PolicyType": "SimpleScaling",
                    "AdjustmentType": "PercentChangeInCapacity",
                    "ScalingAdjustment": 5,
                    "Cooldown": 300,
                    "StepAdjustments": [],
                    "Alarms": [
                        {
                            "AlarmName": "Demo_alarm_2",
                            "AlarmARN": "arn:aws:cloudwatch:us-west-2:00000000:alarm:Demo_alarm_2",
                        }
                    ],
                    "Enabled": True,
                },
                {
                    "AutoScalingGroupName": "Demo_ASG_3",
                    "PolicyName": "Demo_ASG_3-CPUReservation-66PCVKCX4CAJ",
                    "PolicyARN": "Demo_ARN_3",
                    "PolicyType": "SimpleScaling",
                    "AdjustmentType": "PercentChangeInCapacity",
                    "ScalingAdjustment": 5,
                    "Cooldown": 300,
                    "StepAdjustments": [],
                    "Alarms": [
                        {
                            "AlarmName": "Demo_alarm_3",
                            "AlarmARN": "arn:aws:cloudwatch:us-west-2:00000000:alarm:Demo_alarm_3",
                        }
                    ],
                    "Enabled": True,
                },
            ],
            "ResponseMetadata": {
                "RequestId": "cbba6b94-6d72-4902-aca8-e0b128ce19ac",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "cbba6b94-6d72-4902-aca8-e0b128ce19ac",
                    "content-type": "text/xml",
                    "content-length": "3661",
                    "vary": "accept-encoding",
                    "date": "xx, xx xx 2022 16:51:26 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.asg_obj._asg.describe_policies.return_value = describe_policies_success_response
        result = self.asg_obj.check_scaling_policy('Demo_ASG')
        self.assertTrue(result)

    def test_check_scaling_policy_failure(self):
        """
        Method to validate no scaling policy scenario
        """

        # response dict to mock session.client("autoscaling").describe_policies
        describe_policies_failure_response = {
            "ScalingPolicies": [],
            "ResponseMetadata": {
                "RequestId": "c9f53a08-40f1-4086-a01b-30d169298542",
                "HTTPStatusCode": 200,
                "HTTPHeaders": {
                    "x-amzn-requestid": "c9f53a08-40f1-4086-a01b-30d169298542",
                    "content-type": "text/xml",
                    "content-length": "297",
                    "date": "xx, xx xx 2022 16:51:26 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.asg_obj._asg.describe_policies.return_value = describe_policies_failure_response
        result = self.asg_obj.check_scaling_policy('Demo_ASG')
        self.assertFalse(result)

    @staticmethod
    def get_paginator_response_success():
        """
        Static method to mock paginate.search() results where we have filter match
        """

        # response dict to mock session.client("autoscaling").get_paginator.paginator.search()
        paginator_response_success = {
            "AutoScalingGroupName": "Demo_ASG_1",
            "AutoScalingGroupARN": "Demo_ARN",
            "MixedInstancesPolicy": {
                "LaunchTemplate": {
                    "LaunchTemplateSpecification": {
                        "LaunchTemplateId": "lt-0f85ff6b7c4b26d7c",
                        "LaunchTemplateName": "Demo_LaunchTemplate",
                        "Version": "2",
                    },
                    "Overrides": [{"InstanceType": "m5.4xlarge"}],
                },
            },
            "MinSize": 1,
            "MaxSize": 5,
            "DesiredCapacity": 1,
            "DefaultCooldown": 300,
            "AvailabilityZones": ["us-west-2a"],
            "LoadBalancerNames": [],
            "TargetGroupARNs": [],
            "HealthCheckType": "EC2",
            "HealthCheckGracePeriod": 15,
            "Instances": [],
            "SuspendedProcesses": [],
            "VPCZoneIdentifier": "subnet-Demo_1",
            "EnabledMetrics": [],
            "Tags": [
                {
                    "ResourceId": "Demo_ASG_1",
                    "ResourceType": "auto-scaling-group",
                    "Key": "Test_key",
                    "Value": "Test_value",
                    "PropagateAtLaunch": True,
                },
            ],
            "NewInstancesProtectedFromScaleIn": False,
            "ServiceLinkedRoleARN": "Demo_ARN",
            "CapacityRebalance": True,
        }
        yield paginator_response_success

    def test_get_names_filtered_success(self):
        """
        Method to validate get_name_filtered success scenario
        this will use static method get_paginator_response_success()
        to mock success scenario generator object
        """

        self.asg_obj._asg.get_paginator.return_value. \
            paginate.return_value. \
            search.return_value = self.get_paginator_response_success()
        result = self.asg_obj.\
            get_names_filtered(key='Test_key', value='Test_value')
        self.assertEqual(result, ['Demo_ASG_1'])

    @staticmethod
    def get_paginator_response_failure():
        """
        Static method to mock paginate.search() results where we don't find any filter match
        """

        # response dict to mock session.client("autoscaling").get_paginator.paginator.search()
        paginator_response_failure = {}
        yield from paginator_response_failure

    def test_get_names_filtered_failure(self):
        """
        Method to validate get_name_filtered success scenario
        this will use static method get_paginator_response_success()
        to mock failure scenario generator object
        """

        self.asg_obj._asg.get_paginator.return_value. \
            paginate.return_value. \
            search.return_value = self.get_paginator_response_failure()
        result = self.asg_obj.\
            get_names_filtered(key='Test_key', value='Test_value')
        self.assertEqual(result, [])

    def test_get_asg_desired_max_capacity_success(self):
        """
        Method to validate success scenario
        where we should be able to fetch desired and max capacity
        from describe_auto_scaling_groups response
        """

        # response dict to mock session.client("autoscaling").describe_auto_scaling_groups()
        describe_auto_scaling_groups_response_success = {
            "AutoScalingGroups": [
                {
                    "AutoScalingGroupName": "Demo_ASG_1",
                    "AutoScalingGroupARN": "Demo_ARN",
                    "MixedInstancesPolicy": {
                        "LaunchTemplate": {
                            "LaunchTemplateSpecification": {
                                "LaunchTemplateId": "lt-0f85ff6b7c4b26d7c",
                                "LaunchTemplateName": "Demo_LaunchTemplate",
                                "Version": "2",
                            },
                            "Overrides": [{"InstanceType": "m5.4xlarge"}],
                        },
                        "InstancesDistribution": {
                            "OnDemandAllocationStrategy": "prioritized",
                            "OnDemandBaseCapacity": 0,
                            "OnDemandPercentageAboveBaseCapacity": 100,
                            "SpotAllocationStrategy": "lowest-price",
                            "SpotInstancePools": 2,
                        },
                    },
                    "MinSize": 1,
                    "MaxSize": 5,
                    "DesiredCapacity": 1,
                    "DefaultCooldown": 300,
                    "AvailabilityZones": ["us-west-2a"],
                    "LoadBalancerNames": [],
                    "TargetGroupARNs": [],
                    "HealthCheckType": "EC2",
                    "HealthCheckGracePeriod": 15,
                    "CreatedTime": "12-12-2020",
                    "SuspendedProcesses": [],
                    "VPCZoneIdentifier": "subnet-Demo_1",
                    "EnabledMetrics": [],
                    "Tags": [
                        {
                            "ResourceId": "Demo_ASG_1",
                            "ResourceType": "auto-scaling-group",
                            "Key": "Test_key",
                            "Value": "Test_value",
                            "PropagateAtLaunch": True,
                        },
                    ],
                    "NewInstancesProtectedFromScaleIn": False,
                    "ServiceLinkedRoleARN": "Demo_ARN",
                    "CapacityRebalance": True,
                }
            ],
        }
        self.asg_obj._asg.\
        describe_auto_scaling_groups.return_value = describe_auto_scaling_groups_response_success
        desired, max_cap = self.asg_obj.\
            get_asg_desired_max_capacity(asg_name='Demo_ASG_1')
        self.assertEqual(1, desired)
        self.assertEqual(5, max_cap)

    def test_get_asg_desired_max_capacity_failure(self):
        """
        Method to validate failure scenario
        where describe_auto_scaling_groups doesn't have any response payload
        """

        # response dict to mock session.client("autoscaling").describe_auto_scaling_groups()
        describe_auto_scaling_groups_response_failure = {}
        self.asg_obj._asg.describe_auto_scaling_groups.return_value\
            = describe_auto_scaling_groups_response_failure
        desired, max_cap = self.asg_obj.\
            get_asg_desired_max_capacity(asg_name='Demo_ASG')
        self.assertEqual(-1, desired)
        self.assertEqual(-1, max_cap)

    def test_get_filter_tags_success(self):
        """
        Method to validate the success scenario
        where we are able to successfully fetch filter tags from
        container environments variables
        """

        # mocking container environment variable setting
        os.environ["ASG_TAG_NAME"] = "Demo_key"
        os.environ["ASG_TAG_VALUE"] = "Demo_value"
        filter_key, filter_value = self.asg_obj. \
            get_filter_tags()
        self.assertEqual('Demo_key', filter_key)
        self.assertEqual('Demo_value', filter_value)

    def test_get_filter_tags_failure(self):
        """
        Method to validate the failure scenario
        where we are not able to successfully fetch filter tags from
        container environments variables (missing scenario)
        """

        filter_key, filter_value = self.asg_obj. \
            get_filter_tags()
        self.assertEqual(None, filter_key)
        self.assertEqual(None, filter_value)


if __name__ == "__main__":
    unittest.main()
