"""
Docker logs for Splunk
"""
import re
import time
from utils import call_subprocess

if __name__ == '__main__':
    # time period
    since = '1m'

    ps_output = call_subprocess('docker ps -a --format "{{.ID}}"')
    ps_output = str(ps_output, "utf-8")

    #print("ps_output=%s" % ps_output)

    ps_parsed = re.findall(r"(?P<container_id>\S+)", ps_output)
    #print("ps_parsed=%s" % ps_parsed)

    for container_id in ps_parsed:
        logs_output = call_subprocess('docker logs --since '+since+' '+container_id)
        logs_output = str(logs_output, "utf-8")
        #print("logs_output=%s" % logs_output)
        
        ts = "{:.9f}".format(time.time())
        command = ''
        pid = ''
        message = ''
        
        for line in logs_output.split('\n'):
            line = line.strip()
            #print("line=%s" % line)
            if line:
                logs_parsed = re.findall(r"^(?P<time>\d{10}\.\d{9}):(?P<command>[^:]+):(?P<pid>\d+):(?P<message>.*)", line)
                if logs_parsed:
                    #print("logs_parsed=%s" % logs_parsed)
                    ts = logs_parsed[0][0]
                    command = logs_parsed[0][1]
                    pid = logs_parsed[0][2]
                    message = logs_parsed[0][3]
                
                    print('%s:%s:%s:%s:%s' % (container_id, ts, command, pid, message))
                else:
                    print('%s:%s:%s:%s:%s' % (container_id, ts, command, pid, line))
