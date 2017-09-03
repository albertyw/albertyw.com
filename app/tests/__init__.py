import os

import dotenv


current_path = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_path, '..', '..', '.env')
dotenv.read_dotenv(env_path)
