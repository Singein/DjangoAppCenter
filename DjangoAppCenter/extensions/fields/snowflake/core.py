from datetime import datetime
from threading import Lock

from DjangoAppCenter.extensions.fields.snowflake.config import *


lock = Lock()


def get_timestamp():
    return int(datetime.now().timestamp() * 1000)


def get_next_timestamp():
    timestamp = get_timestamp()
    while timestamp <= lastTimestamp:
        timestamp = get_timestamp()
    return timestamp


def get_snowflake_id():
    with lock:
        global lastTimestamp, sequence
        timestamp = get_timestamp()
        if lastTimestamp == timestamp:
            sequence = (sequence + 1) & sequenceMask
            if sequence == 0:
                timestamp = get_next_timestamp()
        else:
            sequence = 0

        if timestamp < lastTimestamp:
            if settings.LANGUAGE_CODE == 'en-us':
                raise Exception("TimeError: Please synchronize time!")
            else:
                raise Exception("时间戳出错，请同步时间")
        lastTimestamp = timestamp
        snowflake_id = ((timestamp - randomTime) << timestampLeftShift) | (dataCenterID << dataCenterIdShift) | (
            machineID << machineIdShift) | sequence
        return snowflake_id
