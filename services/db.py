from sqlalchemy.orm import Session

from schema import AdAccountLogSerializer, AlertNotificationLogSerializer
from models import FacebookAdBalanceLog, NotificationSentLog


def save_ad_account_balance_log(session: Session, payload: AdAccountLogSerializer):
    """
    Save the balance log for the facebook ad account
    """

    db_logger = FacebookAdBalanceLog(**payload)
    session.add(db_logger)
    session.commit()
    session.refresh(db_logger)
    return db_logger


def save_noticication_log(session: Session, payload: AlertNotificationLogSerializer):
    """
    Save the sent notification log for the facebook ad account balance
    """

    db_logger = NotificationSentLog(**payload)
    session.add(db_logger)
    session.commit()
    session.refresh(db_logger)
    return db_logger
