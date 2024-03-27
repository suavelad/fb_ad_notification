from pydantic import BaseModel, Json


class AdAccountLogSerializer(BaseModel):
    ad_account_id: str
    main_balance: float
    currency: str
    threshold: float
    amount_spent: float
    spend_cap: str
    json_data: Json

    class Config:
        from_attributes = True


class AlertNotificationLogSerializer(BaseModel):
    ad_account_id: str
    ad_balance_log_id: str
    sent_via_email: bool
    sent_via_phone: bool
    sent_via_push_notification: bool

    class Config:
        from_attributes = True
