# Example of generating authenticating codes using guard module
# To use is you have to obtain 'shared_secret' and 'identity_secret'
# From your Steamguard file

import os

from dotenv import load_dotenv
from steampy.guard import generate_confirmation_key, generate_one_time_code

# Load environment variables from .env file
load_dotenv()

shared_secret = os.getenv('STEAM_SHARED_SECRET', '')
identity_secret = os.getenv('STEAM_IDENTITY_SECRET', '')

one_time_authentication_code = generate_one_time_code(shared_secret)
print(one_time_authentication_code)

confirmation_key = generate_confirmation_key(identity_secret, 'conf')
print(confirmation_key)
