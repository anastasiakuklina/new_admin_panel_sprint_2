from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()


include(
    'components/common.py',
    'components/urls.py',
    'components/apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/database.py',
    'components/auth.py',
    'components/static.py',
    'components/locale.py',
    # 'components/logger.py'
)
