from loguru import logger
import time, uuid
def new_trace_id(): return str(uuid.uuid4())
def log_event(name, **meta): logger.info(f"{name} | {meta}")
