import pytest
from unittest.mock import patch
import sys
from project import check_command_line, validate_encoding, num_tokens_from_string

@pytest.fixture
def mock_sys_argv():
    original_argv = sys.argv
    sys.argv = ['project.py', 'sicilian.csv']
    yield
    sys.argv = original_argv

def main():
    pytest.main()

def test_check_command_line_valid_args(mock_sys_argv, capsys):
    check_command_line()
    captured = capsys.readouterr()
    assert captured.out == "['project.py', 'sicilian.csv']\n"

@pytest.mark.parametrize("argv, expected_error", [
    (['project.py'], "Too few command-line arguments"),
    (['project.py', 'sicilian.csv', 'extra_arg'], "Too many command-line arguments"),
    (['project.py', 'sicilian.txt'], "Not a csv file")
])

def test_check_command_line_invalid_args(argv, expected_error):
    with pytest.raises(SystemExit) as e:
        sys.argv = argv
        check_command_line()
    assert str(e.value) == expected_error

def test_check_invalid_encoding():
     with pytest.raises(KeyError):
         validate_encoding('apple')

def test_validate_encoding():
    with patch('tiktoken.encoding_for_model', return_value='utf-8') as mock_encoding:
        encoding = validate_encoding('gpt-3.5-turbo')
        assert encoding == 'utf-8'
        mock_encoding.assert_called_once_with('gpt-3.5-turbo')

def test_num_tokens_from_string():
    test_string = str('I want to pass this course')
    encoding = validate_encoding('gpt-3.5-turbo')
    expected_num_tokens = 6  # Number of tokens from https://platform.openai.com/tokenizer
    num_tokens = num_tokens_from_string(test_string,encoding)
    assert num_tokens == expected_num_tokens

if __name__ == "__main__":
    main()
