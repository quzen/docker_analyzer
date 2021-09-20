"""
Docker events for Splunk
"""
from utils import call_subprocess

if __name__ == '__main__':
    # time period
    since = '1m'
    
    events_output = call_subprocess('docker events --since '+since+' --until 0m --format "{{json .}}" | grep --line-buffered -v "top\|exec_start\|exec_die\|exec_create"')
    events_output = str(events_output, "utf-8")
    
    if events_output:
        print("%s" % events_output)
