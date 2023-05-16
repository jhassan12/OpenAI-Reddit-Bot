from reddit import run
from dotenv import load_dotenv
import openai
import os

if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.environ["openai_api_token"] 
    run()