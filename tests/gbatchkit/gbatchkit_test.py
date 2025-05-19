from gbatchkit.jobs import create_standard_job
from gbatchkit.types import (
    ServiceAccountConfig,
    NetworkInterfaceConfig,
    ComputeConfig,
    ContainerRunnable,
)


def test_create_standard_job():
    job = create_standard_job(
        region="a-region",
        compute_config=ComputeConfig(
            machine_type="n1-standard-123",
            accelerator_type="NVIDIA_TESLA_V100",
            accelerator_count=7,
        ),
        task_count=1,
        runnables=[
            ContainerRunnable(
                image_uri="gcr.io/my-project/my-image",
                entrypoint="command",
                commands=["arg1", "arg2"],
            ),
            ContainerRunnable(
                image_uri="gcr.io/my-project/my-image-2",
                entrypoint="command-2",
                commands=["arg1-2", "arg2-2"],
            ),
        ],
        tmp_dir="/tmp-workspace",
        tmp_dir_size_gb=321,
        network_interface=NetworkInterfaceConfig(
            network="projects/my-project/global/networks/my-network",
            subnetwork="projects/my-project/regions/us-central1/subnetworks/my-subnetwork",
        ),
        service_account=ServiceAccountConfig(
            email="service@account.com",
            scopes=["scope1", "scope2"],
        ),
        depends_on_job_ids=["job-id-1", "job-id-2"],
    )

    assert job == {
        "taskGroups": [
            {
                "taskSpec": {
                    "maxRetryCount": 3,
                    "lifecyclePolicies": [
                        {
                            "action": "RETRY_TASK",
                            "actionCondition": {"exitCodes": [50001]},
                        }
                    ],
                    "environment": {
                        "variables": {"TMPDIR": "/tmp-workspace"},
                    },
                    "runnables": [
                        {
                            "container": {
                                "image_uri": "gcr.io/my-project/my-image",
                                "entrypoint": "command",
                                "commands": ["arg1", "arg2"],
                            }
                        },
                        {
                            "container": {
                                "image_uri": "gcr.io/my-project/my-image-2",
                                "entrypoint": "command-2",
                                "commands": ["arg1-2", "arg2-2"],
                            }
                        },
                    ],
                    "volumes": [
                        {
                            "deviceName": "job-workspace",
                            "mountPath": "/tmp-workspace",
                        }
                    ],
                },
                "taskCount": 1,
                "taskCountPerNode": 1,
                "parallelism": 1,
            }
        ],
        "allocationPolicy": {
            "instances": [
                {
                    "installGpuDrivers": True,
                    "policy": {
                        "machineType": "n1-standard-123",
                        "provisioningModel": "SPOT",
                        "accelerators": [
                            {
                                "type": "NVIDIA_TESLA_V100",
                                "count": 7,
                            }
                        ],
                        "disks": [
                            {
                                "deviceName": "job-workspace",
                                "newDisk": {
                                    "type": "pd-balanced",
                                    "sizeGb": 321,
                                },
                            }
                        ],
                    },
                }
            ],
            "location": {
                "allowedLocations": ["regions/a-region"],
            },
            "network": {
                "networkInterfaces": [
                    {
                        "network": "projects/my-project/global/networks/my-network",
                        "subnetwork": "projects/my-project/regions/us-central1/subnetworks/my-subnetwork",
                        "no_external_ip_address": False,
                    }
                ],
            },
            "serviceAccount": {
                "email": "service@account.com",
                "scopes": ["scope1", "scope2"],
            },
        },
        "logsPolicy": {"destination": "CLOUD_LOGGING"},
        "dependencies": [
            {
                "items": {
                    "job-id-1": "SUCCEEDED",
                    "job-id-2": "SUCCEEDED",
                }
            }
        ],
    }
