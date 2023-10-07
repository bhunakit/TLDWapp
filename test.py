import os
from dotenv import load_dotenv

load_dotenv()

print(str(os.getenv('OPENAI_API_KEY')))
