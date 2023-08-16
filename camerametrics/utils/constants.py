# Constants used in our camerametrics package
API_URL_TEMPLATE = "https://{host}:{port}/api/2.0/camera?apiKey={key}"
DEFAULT_CONFIG_FILE = ".config.toml"
DEFAULT_ENV = "Dev"
DEFAULT_LOG_FILE = "logs/camerametrics.log"
DEFAULT_LOG_FORMAT = "%(asctime)-15s  %(levelname)s  %(message)s"
DEFAULT_LOG_LEVEL = "INFO"
MAX_RETRIES = 3  # Maximum number of retries
RETRY_DELAY = 5  # Delay in seconds before retrying
