import json
import os

import pytest
from pydantic import BaseModel

from gbatchkit.inputs import get_task_arguments


class TaskArgs(BaseModel):
    arg1: int
    arg2: str


@pytest.fixture
def mock_env_path(tmp_path):
    """
    Fixture for mocking GBATCHKIT_ARGS_PATH environment variable to use a temporary file.
    """
    task_data = [{"arg1": 100, "arg2": "value1"}, {"arg1": 200, "arg2": "value2"}]
    file_path = tmp_path / "task_args.json"
    with open(file_path, "w") as f:
        json.dump(task_data, f)
    os.environ["GBATCHKIT_ARGS_PATH"] = str(file_path)
    yield
    del os.environ["GBATCHKIT_ARGS_PATH"]


@pytest.fixture
def mock_task_index():
    """
    Fixture for mocking BATCH_TASK_INDEX environment variable.
    """
    os.environ["BATCH_TASK_INDEX"] = "1"
    yield
    del os.environ["BATCH_TASK_INDEX"]


def test_get_untyped_arguments_from_env(mock_env_path, mock_task_index):
    """
    Test get_task_arguments reading untyped arguments from the environment variable GBATCHKIT_ARGS_PATH.
    """
    task_args = get_task_arguments()
    assert task_args["arg1"] == 200
    assert task_args["arg2"] == "value2"


def test_get_task_arguments_from_env(mock_env_path, mock_task_index):
    """
    Test get_task_arguments reading arguments from the environment variable GBATCHKIT_ARGS_PATH.
    """
    task_args = get_task_arguments(TaskArgs)
    assert task_args.arg1 == 200
    assert task_args.arg2 == "value2"


def test_get_task_arguments_from_cmd_args():
    """
    Test get_task_arguments parsing from provided command-line arguments.
    """
    cmd_args = ["--arg1", "300", "--arg2", "value3"]
    task_args = get_task_arguments(TaskArgs, args=cmd_args)
    assert task_args.arg1 == 300
    assert task_args.arg2 == "value3"


def test_get_task_arguments_no_env_or_args():
    """
    Test get_task_arguments failure when neither GBATCHKIT_ARGS_PATH nor valid task_args_cls is provided.
    """
    with pytest.raises(
        ValueError,
        match="Need GBATCHKIT_ARGS_PATH env, or task_args_cls to read from args",
    ):
        get_task_arguments()
