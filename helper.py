import requests
from loguru import logger
from settings import config


class FacebookApi:
    def __init__(self) -> None:
        pass

    def get_access_token(self):
        """
        Get the access token for the facebook api
        """
        url = f"{config.BASE_URL}/oauth/access_token?client_id={config.APP_ID}&client_secret={config.APP_SECRET}&grant_type=client_credentials"

        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Error getting access token {response.text}")
            return None
        access_token = response.json()["access_token"]

        return access_token

    def get_fb_account_url(self, account_id):
        """
        Get the url for the facebook account
        same of account_id is act_xxxxxxx
        """

        if not account_id.startswith("act_"):
            logger.error(f"Invalid account id {account_id}")
            return None

        return f"{config.BASE_URL}/{config.BASE_VERSION}/{account_id}?fields=amount_spent,balance,spend_cap&access_token={config.APP_ID}|{config.APP_SECRET}"
