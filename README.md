# gbatchkit-python
Google Cloud Platform Batch Kit (GBK)

## Why GBatchKit?

GCP Batch is a powerful serverless computing platform. `gbatchkit` provides lightweight tools to use Batch more effectively.

Key features:

* Create a straightforward job easily. This will run `my-script.py` in the given container on Batch.

  ```python
  container_uri = "container_uri"
  runnable = ContainerRunnable(
    image_uri=container_uri,
    entrypoint="python",
    commands=["my-script.py"]
  )
  task_count = 1
  job = create_standard_job(region, compute_config, task_count, [runnable])
  submit_job(job, "my_unique_job_id", region)
  ```

  * Also supports:
    * Customize the `service_account` and `network_interface` used to run the job.
    * Allocate a persistent disk for temp files.
    * Add dependency to other jobs (GCP Batch public preview feature).

* Create multi-task jobs (for one or multiple runnables).

  * Uses Google Cloud Storage to store task arguments.

  ```python
  task_arguments = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
  job = create_standard_job(region, compute_config, len(task_arguments), runnable)
  working_directory = "gs://a-bucket/a-directory/jobs"
  prepare_multitask_job(job, working_directory, tasks=task_arguments)
  submit_job(job, "my_unique_job_id", region)
  ```

  * Supports different arguments per runnable. In this example, the 1st runnable python script takes arguments `a` and `b` and the second runnable python script takes arguments `c` and `d`. Note that Batch requires all runnables to have the same number of tasks.

    ```python
    container_uri = "container_uri"
    runnable1 = ContainerRunnable(
      image_uri=container_uri,
      entrypoint="python",
      commands=["script1.py"]
    )
    runnable2 = ContainerRunnable(
      image_uri=container_uri,
      entrypoint="python",
      commands=["script2.py"]
    )
    task_arguments = [
      [{"a": 1, "b": 2}, {"a": 3, "b": 4}],
      [{"c": 1, "d": 2}, {"c": 3, "d": 4}],
    ]
    
    job = create_standard_job(region, compute_config, task_count=2, runnables=[runnable1, runnable2])
    working_directory = "gs://a-bucket/a-directory/jobs"
    prepare_multitask_job(job, working_directory, tasks=task_arguments)
    
    submit_job(job, "my_unique_job_id", region)
    ```

    
