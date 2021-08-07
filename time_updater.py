from apscheduler.schedulers.blocking import BlockingScheduler
import requests

# Minutes to add to each entry in the database
TIME_INTERVAL = 1
def time_updater():
    requests.get('http://localhost:5001/update?mins=' + str(TIME_INTERVAL))

sched = BlockingScheduler()
sched.add_job(time_updater, 'interval', minutes=TIME_INTERVAL)
sched.start()
