import os
from dotenv import load_dotenv


class Variables:
    # Load variables from .env file
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, "variables.env"))

    # Access environment variables
    PROXY = os.getenv("PROXY")
    INPUT_URL = os.getenv("INPUT_URL")
    OUTPUT_FILE = os.getenv("OUTPUT_FILE")


if __name__ == "__main__":
    print(Variables.PROXY)
    print(Variables.INPUT_URL)
    print(Variables.OUTPUT_FILE)
