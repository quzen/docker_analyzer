"""
Docker logs for Splunk
"""
import argparse
import re
import time
from utils import call_subprocess

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--since', action='store', type=str)

    args = my_parser.parse_args()
    if args.since:
        since = args.since
    else:
        since = '60s'

    ps_output = call_subprocess('docker ps -a --format "{{.ID}}"')

    ps_parsed = re.findall(r"(?P<container_id>\S+)", ps_output)

    for container_id in ps_parsed:
        logs_output = call_subprocess('docker logs --since '+since+' '+container_id)
        
        ts = "{:.9f}".format(time.time())
        command = ''
        pid = ''
        message = ''
        
        for line in logs_output.split('\n'):
            line = line.strip()

            if line:
                logs_parsed = re.findall(r"^(?P<time>\d{10}\.\d{9}):(?P<command>[^:]+):(?P<pid>\d+):(?P<message>.*)", line)
                if logs_parsed:
                    ts = logs_parsed[0][0]
                    command = logs_parsed[0][1]
                    pid = logs_parsed[0][2]
                    message = logs_parsed[0][3]
                
                    print('%s:%s:%s:%s:%s' % (container_id, ts, command, pid, message))
                else:
                    print('%s:%s:%s:%s:%s' % (container_id, ts, command, pid, line))
