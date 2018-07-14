import os

from syspath import get_git_root
import dotenv


dotenv.load_dotenv(os.path.join(get_git_root(), '.env'))
