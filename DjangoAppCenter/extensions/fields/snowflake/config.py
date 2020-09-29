from django.conf import settings

MACHINE_ID = getattr(settings, "SNOWFLAKE_MACHINE_ID", 1)  # 机器ID
DATA_CENTER_ID = getattr(settings, "SNOWFLAKE_DATA_CENTER_ID", 1)  # 数据中心ID
SEQUENCE = getattr(settings, "SNOWFLAKE_SEQUENCE", 14)  # 从哪个整数开始计数
RANDOM_TIME = getattr(settings, "SNOWFLAKE_RANDOM_TIME", 1288834974657)  # 时间戳 Timestamp

if MACHINE_ID is None:
    raise Exception(
        "Error: Please set MACHINE_ID,cannot exceed 5 digits,can only be an integer!")
elif MACHINE_ID > 99999:
    raise Exception(
        "Error: MACHINE_ID cannot exceed 5 digits,can only be an integer!")
else:
    machineID = MACHINE_ID

if DATA_CENTER_ID is None:
    raise Exception(
        "Error: Please set DATA_CENTER_ID,cannot exceed 5 digits,can only be an integer!")
elif DATA_CENTER_ID > 99999:
    raise Exception(
        "Error: DATA_CENTER_ID cannot exceed 5 digits,can only be an integer!")
else:
    dataCenterID = DATA_CENTER_ID

if SEQUENCE is None:
    raise Exception(
        "Error: Please set SEQUENCE,cannot exceed 12 digits,can only be an integer!")
elif SEQUENCE > 999999999999:
    raise Exception(
        "Error: SEQUENCE cannot exceed 12 digits,can only be an integer!")
else:
    sequence = SEQUENCE

if RANDOM_TIME is None:
    raise Exception("Error: Please set RANDOM_TIME,RANDOM_TIME is timestamp")
else:
    randomTime = RANDOM_TIME

machineIDBits = 5
dataCenterIDBits = 5
sequenceBits = 12
maxMachineID = -1 ^ -1 << machineIDBits
maxDataCenterID = -1 ^ (-1 << dataCenterIDBits)
machineIdShift = sequenceBits
dataCenterIdShift = sequenceBits + machineIDBits
timestampLeftShift = sequenceBits + machineIDBits + dataCenterIDBits
sequenceMask = -1 ^ -1 << sequenceBits
lastTimestamp = -1
