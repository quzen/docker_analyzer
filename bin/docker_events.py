"""
Docker events for Splunk
"""
import argparse
from utils import call_subprocess

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--since', action='store', type=str)

    args = my_parser.parse_args()
    if args.since:
        since = args.since
    else:
        since = '60s'
    
    events_output = call_subprocess('docker events --since '+since+' --until 0m --format "{{json .}}" | grep --line-buffered -v "top\|exec_start\|exec_die\|exec_create"')
    
    if events_output:
        print("%s" % events_output)
