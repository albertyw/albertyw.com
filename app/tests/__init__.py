from syspath import git_root, get_git_root  # NOQA
import dotenv


dotenv.load_dotenv(get_git_root() / '.env')
