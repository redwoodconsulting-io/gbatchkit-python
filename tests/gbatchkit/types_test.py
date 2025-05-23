import pytest

from gbatchkit.types import parse_compute_config


def test_parse_compute_config():
    # Test with all parts specified
    config = parse_compute_config("n1-standard-8:SPOT+nvidia-tesla-t4:1")
    assert config.machine_type == "n1-standard-8"
    assert config.provisioning_model == "SPOT"
    assert config.accelerator_type == "nvidia-tesla-t4"
    assert config.accelerator_count == 1

    config = parse_compute_config("n1-standard-8:SPOT+nvidia-tesla-t4")
    assert config.accelerator_type == "nvidia-tesla-t4"
    assert config.accelerator_count == 1

    # Test with only machine type and provisioning model
    config = parse_compute_config("n1-standard-8:SPOT")
    assert config.machine_type == "n1-standard-8"
    assert config.provisioning_model == "SPOT"
    assert config.accelerator_type == ""
    assert config.accelerator_count == 0

    # Test with only machine type
    config = parse_compute_config("n1-standard-8")
    assert config.machine_type == "n1-standard-8"
    assert config.provisioning_model == "SPOT"
    assert config.accelerator_type == ""
    assert config.accelerator_count == 0

    # Test with empty string
    with pytest.raises(ValueError):
        parse_compute_config("")

    # Test with invalid format
    with pytest.raises(ValueError):
        parse_compute_config("invalid+format+string")
    with pytest.raises(ValueError):
        parse_compute_config("invalid:format:string")
    with pytest.raises(ValueError):
        parse_compute_config("n1-standard-4:SPOT+gpu:1:1")
