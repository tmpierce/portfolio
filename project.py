import pandas as pd
import sys
import tiktoken

def main():
    check_command_line()
    try:
        with open(sys.argv[1],"r") as file:
            df = pd.read_csv(file)
            csv_string = df.to_csv(index=False)
    except FileNotFoundError:
        sys.exit("File does not exist")
    # Get model to use
    model_name = str(input("What AI model will you be using? "))
    # Validate model
    # gpt-3.5-turbo
    try:
        encoding = validate_encoding(model_name)
    except KeyError:
        sys.exit("This model is not supported by TikToken")
    tokens = num_tokens_from_string(csv_string, encoding)
    print("This CSV uses",tokens,"tokens in",model_name)

def check_command_line():
    print(sys.argv)
    if len(sys.argv) <2:
        sys.exit("Too few command-line arguments")
    if len(sys.argv) >2:
        sys.exit("Too many command-line arguments")
    if ".csv" not in sys.argv[1]:
        sys.exit("Not a csv file")

def validate_encoding(model_name):
    encoding = tiktoken.encoding_for_model(model_name)
    return encoding

def num_tokens_from_string(string: str, encoding) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return num_tokens

if __name__ == "__main__":
    main()
