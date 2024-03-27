from decouple import config

BASE_URL = config("FACEBOOK_BASE_URL")
BASE_VERSION = config("VERSION")
APP_ID = config("APP_ID")
APP_SECRET = config("APP_SECRET")


THRESHOLD_BALANCE = 1000  # Threshold balance for the facebook ad account balance for alerting




# REDIS_HOST = config("REDIS_HOST")
# REDIS_PORT = config("REDIS_PORT")
# REDIS_PASSWORD = config("REDIS_PASSWORD")
# REDIS_USERNAME = config("REDIS_USERNAME")

# REDIS_URL = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
