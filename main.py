from fastapi import FastAPI,BackgroundTasks
# from celery import Celery
# from celery.schedules import crontab


app = FastAPI(
    title="TRIGGER  API",
    description="Trigger service",
    docs_url="/",
)





@app.get('/trigger_task',
          tags=["Trigger"]
)
def trigger_task(background_tasks: BackgroundTasks):
    from tasks import send_balance_alert
    # Trigger the background task
    background_tasks.add_task(send_balance_alert)
    return {"message": "Task triggered successfully!"}
