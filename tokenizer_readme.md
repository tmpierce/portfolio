# CSV Tokenizer
#### Video Demo:  https://youtu.be/hFB3rE1TzfY
#### Description: Provide how many tokens a CSV file would be for a given OpenAI model

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pandas, tikotken and pytest. This project also requires sys and unittest.mock

## Description: Why CS50 and why a tokenizer?

I’m currently a SQL analyst for a DTC Wine company. I’ve had to use Python occasionally in DBT and for tasks like merging incongruous CSVs in SageMaker, wanted to develop a proper foundation through CS50. The company has begun using ChatGPT for tasks such as returning sentiment analysis on customer reviews. One of our current challenges is knowing how many tokens a given customer file will require for a given prompt. In order to complete the task, I needed to learn how to properly use the pip packages Pandas and TikToken, as well as how to configure tests in PyTest using Fixtures and Parameters. For this project, I limited the scope to accurately providing the number of tokens for a given file and model. Future versions will split the file into chunks based on a token count specified by the user.

After researching OpenAI’s documentation, I found a BPE Tokeniser called TikToken https://pypi.org/project/tiktoken/

Using OpenAI’s recipe examples, I found that TikToken requires strings to be tokenized, so I then needed to convert our csv files into strings. https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken

Pandas has a method of converting CSVs into DataFrames, 2-dimensional objects similar to arrays, which can then be converted into strings.
https://www.w3schools.com/python/pandas/pandas_dataframes.asp
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_string.html

## Usage

### User Input 1: CSV File
The program requires two pieces of user input, a csv file and the OpenAI Model that we wish to encode for. Different models may have different token requirements for the same strings. Using the same process as in the Pizza assignment, I check that the initial command-line contains exactly one argument, the name (or path) of a CSV file. For testing in CS50.dev, I reused the Sicilian and Regular csvs in my project. The check_command_line() function checks if the command line had too many or too few arguments, and whether the file contains .csv. Pandas is able to convert the CSV into a data frame using the read_csv command. This is attempted with a FileNotFoundError thrown as an exception.

### User Input 2: AI Model Name
If all of these checks pass, the program prompts the user for an AI Model name. TikToken supports models using one of 3 encodings, cl100k_base, p50k_base and r50k_base. tiktoken.encoding_for_model() returns the proper encoding for a given model name. If an invalid model name is provided, tiktoken returns a KeyError. In this instance, I return a sys.exit message telling the user that the given model is not supported by TikToken.

### Passing the Inputs to num_tokens
Once we have a string of the CSV and a valid model, those inputs are passed onto TikToken’s num_tokens method to be converted into an integer which is passed back up the main function.

We then print the following message:
print("This CSV uses",tokens,"tokens in",model_name)

## Testing Overview
Finally, to test these functions properly in pytest, I needed to be able to pass sample arguments in the command line, and record the errors. To do this required the unittest mock library’s patch command,  as well as the Pytest Fixture, Parameter and Capture commands

 https://docs.python.org/3/library/unittest.mock.html
 https://docs.pytest.org/en/6.2.x/parametrize.html
 https://docs.pytest.org/en/6.2.x/capture.html
 https://docs.pytest.org/en/6.2.x/fixture.html#fixture-parametrize


I tested the following functions:
 check_command_line, validate_encoding, num_tokens_from_string

### Check Valid Arguments
Using a fixture, I passed the following mock system argument to the check command line function, then used capsys.readouterr to confirm there was no error

```
@pytest.fixture
def mock_sys_argv():
    original_argv = sys.argv
    sys.argv = ['project.py', 'sicilian.csv']
    yield
    sys.argv = original_argv

def test_check_command_line_valid_args(mock_sys_argv, capsys):
    check_command_line()
    captured = capsys.readouterr()
    assert captured.out == "['project.py', 'sicilian.csv']\n"
```

### Check Invalid Arguments
I parameterized a set of arguments, and asserted that each returned the proper error message on Sys.Exit

```

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
```

### Validate Encodings
I checked to ensure an invalid model raises a KeyError, and used the patch decorator as a context manager to ensure the proper encoding was returned for a valid model.

```
def test_check_invalid_encoding():
    		with pytest.raises(KeyError):
        		validate_encoding('apple')
def test_validate_encoding():
    		with patch('tiktoken.encoding_for_model', return_value='utf-8') as mock_encoding:
       	encoding = validate_encoding('gpt-3.5-turbo')
        	assert encoding == 'utf-8'
        	mock_encoding.assert_called_once_with('gpt-3.5-turbo')
```


### Ensure num_tokens returns correct Amount
Finally, i passed a test string through num_tokens to ensure the amount matches the result on https://platform.openai.com/tokenizer. In this case “I want to pass this course” should return 6,

```
def test_num_tokens_from_string():
    test_string = str('I want to pass this course')
    encoding = validate_encoding('gpt-3.5-turbo')
    expected_num_tokens = 6  # Number of tokens from https://platform.openai.com/tokenizer
    num_tokens = num_tokens_from_string(test_string,encoding)
    assert num_tokens == expected_num_tokens
```

Thank you for reading this!
