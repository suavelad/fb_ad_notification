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
    from tasks import background_task
    # Trigger the background task
    background_tasks.add_task(background_task,1,2)
    return {"message": "Task triggered successfully!"}
