from src.aws_utils import download_s3
from src.utils import load_model, load_data, load_config
from unittest.mock import mock_open, patch
import yaml
from yaml.error import YAMLError
import pytest
import pandas as pd

def test_load_model():
    with patch('joblib.load') as mock_load:
        mock_load.return_value = "Mock Model"
        result = load_model("dummy_model_path")
    assert result == "Mock Model"

def test_load_data():
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.return_value = pd.DataFrame()
        result = load_data("dummy_data_path")
    assert isinstance(result, pd.DataFrame)

def test_download_s3():
    with patch('boto3.client') as mock_s3:
        instance = mock_s3.return_value
        instance.download_file.return_value = None
        assert download_s3("test_bucket", "test_key", "test_file_path") == None

def test_load_config():

    # Mock configuration data
    mock_data = {
        "key": "value"
    }
    
    # YAML dump to create a string representation of mock data
    mock_yaml = yaml.dump(mock_data)

    # Mock the open function
    m = mock_open(read_data=mock_yaml)

    with patch("builtins.open", m):
        with patch("yaml.load") as mock_yaml_load:
            with patch("src.utils.logger") as mock_logger:
                mock_yaml_load.return_value = mock_data
                
                # Test correct yaml loading
                config = load_config("path/to/config.yml")
                assert config == mock_data
                mock_logger.info.assert_called_once_with("Configuration file loaded from %s", "path/to/config.yml")
                
                # Test incorrect yaml loading
                mock_yaml_load.side_effect = YAMLError
                with pytest.raises(NotImplementedError):
                    load_config("path/to/config.yml")
                mock_logger.error.assert_called_once_with("Error while loading configuration from %s", "path/to/config.yml")
