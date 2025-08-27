import json, random, time, uuid
from datetime import datetime

def gen_event():
    return {
        "event_id": str(uuid.uuid4()),
        "ts": datetime.utcnow().isoformat(),
        "call_id": f"c_{random.randint(1, 999999):06d}",
        "operator_id": f"op_{random.randint(1, 50):02d}",
        "duration_seconds": random.randint(10, 600),
        "outcome": random.choice(["SUCCESS","NO_ANSWER","BUSY","DROP"])
    }

if __name__ == "__main__":
    while True:
        evt = gen_event()
        print(json.dumps(evt), flush=True)
        time.sleep(5)
