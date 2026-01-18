import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask Configuration
TIMEZONE = os.getenv('TIMEZONE', 'America/Vancouver')
APP_SECRET = os.getenv('APP_SECRET', 'YOUR_SECRET_KEY')
DEBUG_MODE = os.getenv('DEBUG_MODE', 'True').lower() in ('true', '1', 'yes')
BASE_URL = os.getenv('BASE_URL', 'https://localhost')

# Database Configuration
DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING', 'sqlite:////deploy/database.db')
DB_SEED = os.getenv('DB_SEED', 'True').lower() in ('true', '1', 'yes')

# Logging Configuration
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
LOGGING_MAX_SIZE_KB = int(os.getenv('LOGGING_MAX_SIZE_KB', '1000'))
LOGGING_MAX_LOGS = int(os.getenv('LOGGING_MAX_LOGS', '3'))
LOGGING_FILE = os.getenv('LOGGING_FILE', './boilerplate/logs/main.log')
LOGGING_LOG_400_ERRORS = os.getenv('LOGGING_LOG_400_ERRORS', 'True').lower() in ('true', '1', 'yes')
LOGGING_LOG_403_ERRORS = os.getenv('LOGGING_LOG_403_ERRORS', 'True').lower() in ('true', '1', 'yes')
LOGGING_LOG_404_ERRORS = os.getenv('LOGGING_LOG_404_ERRORS', 'True').lower() in ('true', '1', 'yes')
LOGGING_LOG_500_ERRORS = os.getenv('LOGGING_LOG_500_ERRORS', 'True').lower() in ('true', '1', 'yes')

# Session Configuration (Minutes)
SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '1440'))

# Password Rules
PASSWORD_MIN_CHARACTERS = int(os.getenv('PASSWORD_MIN_CHARACTERS', '12'))
PASSWORD_MAX_CHARACTERS = int(os.getenv('PASSWORD_MAX_CHARACTERS', '255'))
PASSWORD_REQUIRE_LOWER_CASE = os.getenv('PASSWORD_REQUIRE_LOWER_CASE', 'True').lower() in ('true', '1', 'yes')
PASSWORD_REQUIRE_UPPER_CASE = os.getenv('PASSWORD_REQUIRE_UPPER_CASE', 'True').lower() in ('true', '1', 'yes')
PASSWORD_REQUIRE_NUMERALS = os.getenv('PASSWORD_REQUIRE_NUMERALS', 'True').lower() in ('true', '1', 'yes')
PASSWORD_REQUIRE_SPECIAL_CHARACTERS = os.getenv('PASSWORD_REQUIRE_SPECIAL_CHARACTERS', 'True').lower() in ('true', '1', 'yes')
PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS = os.getenv('PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS', '!#$%&()*+,-./:;<=>?@^_{|}~')
PASSWORD_RESET_CODE_VALIDITY = int(os.getenv('PASSWORD_RESET_CODE_VALIDITY', '120'))

# Profile Configuration
NUMBER_OF_PROFILE_COLORS = int(os.getenv('NUMBER_OF_PROFILE_COLORS', '8'))