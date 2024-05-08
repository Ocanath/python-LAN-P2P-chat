
from datetime import datetime
import time

"""
    INPUTS:
        prefix: "Arrived: " or "Left: " indicates state to be pre-pended to the timestamp information
        timestamp: the time the event occurred, as a python datetime timestamp. used for log file naming, and also for entry creation
"""
def write_log_entry(prefix, timestamp):
    filename = timestamp.strftime("%m-%d-%Y")+".csv"
    f = open(filename, "a")
    f.write(prefix+timestamp.strftime("%m/%d/%Y %H:%M:%S")+'\n')
    f.close()

