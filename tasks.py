from celery_config import celery_app
from loguru import logger

from services.db import save_ad_account_balance_log
from settings import THRESHOLD_BALANCE,get_db

from services.accounts import AccountService
from services.notification_channel import send_notification_alert 


session = next(get_db())


@celery_app.task(name="send_balance_alert")
def send_balance_alert():
    """
    If the balance is less than the set threshold, send an alert to the user account via the notification channel

    This function will be called by a cron job that runs every 24 hours
    """

    account_service = AccountService()
    ad_accounts = account_service.get_all_user_account_ids()

    if not ad_accounts:
        logger.error("No account ids found")
        return None

    for ad_account in ad_accounts:
        account_id = ad_account.fb_account_id
        balance_payload = account_service.get_user_balance(account_id)

        if balance_payload is None or balance_payload["main_balance"] is None:
            logger.error(f"Error getting balance for account id {account_id}")
            continue

        balance = balance_payload["main_balance"]

        # Save the balance log to the db
        balance_log = save_ad_account_balance_log(session, balance_payload)

        if balance > THRESHOLD_BALANCE:
            logger.info(
                f"Balance for account id {account_id} is above threshold. No alert needed"
            )
            continue
        else:
            send_notification_alert(balance_log, ad_account, balance)
    return "Alert Sent"



@celery_app.task(name='testing')
def background_task(arg1, arg2):
    # Perform some background task here
    result = arg1 + arg2
    return result