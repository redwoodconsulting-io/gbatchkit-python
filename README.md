# ☁️🛠️ gbatchkit

## 🎯 Overview

`gbatchkit` is a Python library that simplifies defining, configuring, and submitting Google Cloud Batch jobs. It offers:

*   **Programmatic Job Definition:** Construct Batch jobs in Python (machine types, GPUs, storage, etc.).
*   **Task Argument Handling:** Parse arguments for batch tasks, with Pydantic support.
*   **Simplified Submission:** A wrapper around `gcloud` for job submission.
*   **Multitask Utilities:** Helpers for jobs with multiple runnables/arguments.

**Typical Workflow:**

1.  ➡️ **Define Task Args:** Use `gbatchkit.inputs.get_task_arguments` in your task script.
2.  ➡️ **Build Job:** Use `gbatchkit.jobs` and `gbatchkit.types` (e.g., `create_standard_job`, `ContainerRunnable`) to create the job dict.
3.  ➡️ **(Optional) Prep Multitask Args:** Use `jobs.prepare_multitask_job` if tasks need varied arguments.
4.  ➡️ **Submit:** Call `jobs.submit_job`.

Key modules: `gbatchkit.jobs`, `gbatchkit.types`, `gbatchkit.inputs`.

## 🚀 Simple Usage Example

Define and submit a basic Google Cloud Batch job:

```python
from gbatchkit import jobs, types

# Define a container and compute resources
container = types.ContainerRunnable(
    image_uri="gcr.io/google-containers/busybox",
    entrypoint="/bin/sh",
    commands=["-c", "echo Hello from task ${BATCH_TASK_INDEX}! && sleep 10"]
)
compute_config = types.ComputeConfig(machine_type="n1-standard-1") # SPOT is default

# Create job definition (single task)
job_definition = jobs.create_standard_job(
    region="us-central1", # Specify your GCP region
    compute_config=compute_config,
    task_count=1,
    runnables=[container]
)

# For jobs with multiple tasks needing different arguments, `jobs.prepare_multitask_job`
# serializes a list of argument dicts (one per task) to a specified cloud storage
# `working_directory`. Each task then uses `inputs.get_task_arguments()` to load
# its specific arguments from files within that directory (e.g., `task_0_args.json`).
# The job definition is updated with environment variables pointing to these argument files.

# Submit the job
try:
    job_id = "my-gbatchkit-job"
    jobs.submit_job(job=job_definition, job_id=job_id, region="us-central1")
    print(f"Submitted job: {job_id}")
except RuntimeError as e:
    print(f"Error: {e}")
```

## 📦 Installation

Install `gbatchkit` from PyPI (recommended) or source:

```bash
pip install gbatchkit  # From PyPI
pip install .          # From local source
```
Requires Python 3.9+. Dependencies are in `requirements.txt`.

## ✅ Running Tests

Tests use `pytest`. Install dev dependencies and run:

```bash
pip install .[dev]
pytest
```
The tests are in the `tests/` directory.
