import time
from timeloop import Timeloop
from datetime import timedelta

MINUTE_INTERVAL = 10

t1 = Timeloop()

@t1.job(interval=timedelta(minutes=MINUTE_INTERVAL))
def update_json_time():
    start_time = time.time()
    json_contents = None
    try:
        with open("Cache/cache1.json") as f:
            json_contents = json.load(f)

        for entry in json_contents["cache_data"]:
            entry["time"] += MINUTE_INTERVAL
            if (int(entry["time"]) >= 60):
                json_contents["cache_data"].remove(entry)
        
        with open("Cache/cache1.json", "w") as f:
            json.dump(json_contents, f)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    t1.start(block=True)