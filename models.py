from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    PrimaryKeyConstraint,
    DateTime,
    JSON,
    Float,
)
from datetime import datetime

from sqlalchemy.orm import relationship


from settings import Base


class AdAccount(Base):
    __tablename__ = "ad_account"

    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String(255), nullable=False, unique=False)
    last_name = Column(String(255), nullable=False, unique=False)
    business_name = Column(String(255), nullable=False, unique=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(255), nullable=False, unique=True)
    fb_account_id = Column(String(255), nullable=False, unique=True)
    ad_account_balance = Column(Float, nullable=False)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.now)
    modified_date = Column(DateTime, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_date = Column(DateTime, nullable=True)

    UniqueConstraint("email", name="uq_user_email")
    UniqueConstraint("ad_account_id", name="uq_user_ad_account_id")
    PrimaryKeyConstraint("id", name="pk_user_id")

    def get_user(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "fb_account_id": self.fb_account_id,
        }

    def __repr__(self):
        return f"{self.business_name} >>> {self.first_name} {self.last_name} | {self.email}"


class FacebookAdBalanceLog(Base):
    __tablename__ = "facebook_ad_balance_log"

    id = Column(Integer, nullable=False, primary_key=True)
    fb_account_id = Column(String(255), nullable=False, unique=True)
    amount_spent = Column(Float, nullable=False)
    main_balance = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    threshold = Column(Float, nullable=False)
    spend_cap = Column(Float, nullable=False)
    json_data = Column(JSON)
    created_date = Column(DateTime, default=datetime.now)

    notification_sent_log = relationship(
        "NotificationSentLog", uselist=False, back_populates="ad_balance_log"
    )

    UniqueConstraint("ad_account_id", name="uq_ad_account_id")
    PrimaryKeyConstraint("id", name="pk_log_id")

    def __repr__(self):
        return f"{self.ad_account_id} >>> {self.amount_spent} {self.balance} | {self.spend_cap}"


class NotificationSentLog(Base):
    __tablename__ = "notification_sent_log"

    id = Column(Integer, nullable=False, primary_key=True)
    fb_account_id = Column(String(255), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.now)
    sent_via_email = Column(Boolean, default=False)
    sent_via_phone = Column(Boolean, default=False)
    sent_via_push_notification = Column(Boolean, default=False)

    ad_balance_log_id = Column(Integer, ForeignKey("facebook_ad_balance_log.id"))
    ad_balance_log = relationship(
        "FacebookAdBalanceLog", uselist=False, back_populates="notification_sent_log"
    )

    UniqueConstraint("ad_account_id", name="uq_notification_ad_account_id")
    PrimaryKeyConstraint("id", name="pk_notification_id")

    def __repr__(self):
        return f"{self.ad_account_id} >>> {self.message}"
