# Welcome to Cloud Functions for Firebase for Python!
# This script initializes Firebase and schedules a function to run every day.

from firebase_functions import scheduler_fn
import firebase_admin
import mainfunc

# Initialize Firebase
app = firebase_admin.initialize_app()

# 毎日朝九時に実行するよう指示
@scheduler_fn.on_schedule(schedule="every day 09:00", timezone="Asia/Tokyo")
def on_schedule(event: scheduler_fn.ScheduledEvent) -> None:
    # Call the main function from the mainfunc module
    mainfunc.main()