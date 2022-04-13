import os


from dotenv import load_dotenv

load_dotenv()


def get_env_var(value: str):
    return os.getenv(value)
