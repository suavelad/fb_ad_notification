import requests
from sqlalchemy.orm import Session

from helper import FacebookApi

from loguru import logger
from models import AdAccount
from settings import THRESHOLD_BALANCE, get_db


session = next(get_db())


class AccountService:
    def __init__(self) -> None:
        pass

    def get_all_user_account_ids(self, session: Session):
        # TODO: Assuming there is a model in the database that contains the user accounts with a field called account_id
        try:
            account_ids = (
                session.query(AdAccount)
                .filter(AdAccount.is_active == True, AdAccount.is_verified == True)
                .all()
            )
            return account_ids
        except Exception as e:
            logger.error(f"An error occurred while fetching the account ids: {e}")
            return None

    def get_user_balance(self, account_id):
        # expected response : { "amount_spent": "5120944", "balance": "986", "spend_cap": "5304148", "id": "act_xxxxxx" }

        fb = FacebookApi()
        url = fb.get_fb_account_url(account_id)

        response = requests.get(url)
        logger.debug(response)
        data = response.json()

        if response.status_code != 200:
            logger.error(f"An error occurred: {data}")
            return None

        ammount_spent = data.get("amount_spent", 0.0)
        spend_cap = data.get("spend_cap", 0.0)
        balance = data.get("balance", 0.0)
        returned_account_id = data.get("id", None)

        if returned_account_id is None or (returned_account_id != account_id):
            logger.error(f"Invalid account id returned {returned_account_id}")
            return None

        main_balance = (balance + (spend_cap - ammount_spent)) / 100

        payload = {
            "main_balance": main_balance,
            "account_id": returned_account_id,
            "currency": "USD",
            "threshold": THRESHOLD_BALANCE,
            "amount_spent": ammount_spent,
            "spend_cap": spend_cap,
            "balance": balance,
        }

        return payload
