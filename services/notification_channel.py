from loguru import logger
from .db import save_noticication_log

from settings import THRESHOLD_BALANCE, get_db

session = next(get_db())


class NotificationChannel:
    def __init__(self, account_object, message):
        self.account_object = account_object
        self.message = message

    def send_email(self):
        try:
            email = self.account_object.email
            message = self.message
            subject = "FB AD Balance Alert !!!"
            # TODO: Add an email service
            return True
        except Exception as e:
            logger.error(f"Error sending email {e}")
            return False

    def send_sms(self):
        phone = self.account_object.phone_number
        message = self.message

        # TODO: Add a sms service integration
        return False

    def send_push_notification(self):
        # TODO : Add a push notification service using FCM (google) and APN ( apple)
        return False


def send_notification_alert(balance_log, account_object, balance):
    try:
        if balance == THRESHOLD_BALANCE:
            logger.info(
                f"Balance for account id {account_object.fb_account_id} is exactly threshold. Sending alert"
            )
            message = f"Your account balance is {balance} and it is exactly the threshold balance set. Please top up your account"

        elif balance < THRESHOLD_BALANCE:
            logger.info(
                f"Balance for account id {account_object.fb_account_id} is below threshold. Sending alert"
            )
            message = f"Your account balance is {balance} and it is below the threshold balance set. Please top up your account"

        else:
            logger.info(
                f"Balance for account id {account_object.fb_account_id} is above threshold. No alert needed"
            )
            return None

        sent_via_email = False
        sent_via_phone = False
        sent_via_push_notification = False

        notification_channel = NotificationChannel(account_object, message)

        if account_object.email:
            email_response = notification_channel.send_email()
            sent_via_email = True if email_response else False

        if account_object.phone_number:
            sms_response = notification_channel.send_sms()
            sent_via_phone = True if sms_response else False

        push_response = notification_channel.send_push_notification()
        sent_via_push_notification = True if push_response else False

        alert_payload = {
            "ad_account_id": account_object.fb_account_id,
            "ad_balance_log_id": balance_log.id,
            "sent_via_email": sent_via_email,
            "sent_via_phone": sent_via_phone,
            "sent_via_push_notification": sent_via_push_notification,
        }

        save_noticication_log(session, alert_payload)
        return "Notification sent successfully"

    except Exception as e:
        logger.error(f"Error sending notification {e}")
        return None
