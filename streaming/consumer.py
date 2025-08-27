import sys, json, time, pathlib
import pandas as pd
from datetime import datetime

OUT_DIR = pathlib.Path("streaming/out")
OUT_DIR.mkdir(parents=True, exist_ok=True)

batch = []
last_write = time.time()

def maybe_flush():
    global batch, last_write
    if (time.time() - last_write) >= 60 and batch:
        df = pd.DataFrame(batch)
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        df.to_parquet(OUT_DIR / f"events_{ts}.parquet", index=False)
        batch = []
        last_write = time.time()

if __name__ == "__main__":
    for line in sys.stdin:
        try:
            evt = json.loads(line)
            batch.append(evt)
            maybe_flush()
        except Exception:
            continue
