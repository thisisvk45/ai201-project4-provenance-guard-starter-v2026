"""Append one structured operational record per HTTP response.

The request log deliberately excludes submitted text, appeal reasons, and
query strings. The audit log remains the durable record of decisions.
"""

import json
import os
import threading

import config


_lock = threading.Lock()


def append(entry: dict) -> None:
    line = (json.dumps(entry, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    with _lock:
        config.REQUEST_LOG.parent.mkdir(parents=True, exist_ok=True)
        with config.REQUEST_LOG.open("ab") as stream:
            stream.write(line)
            stream.flush()
            os.fsync(stream.fileno())
