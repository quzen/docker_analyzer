"""
Docker top for Splunk
"""
import re
import time
from utils import call_subprocess, unit_translation

if __name__ == '__main__':
    ts = int(time.time())

    ps_output = call_subprocess('docker ps -a --format "{{.ID}}"')

    #print("ps_output=%s" % ps_output)

    ps_parsed = re.findall(r"(?P<container_id>\S+)", ps_output)
    #print("ps_parsed=%s" % ps_parsed)

    for container_id in ps_parsed:
        top_output = call_subprocess('docker exec -i '+container_id+' top -b -n1 -w512')

        top_parsed = re.findall(r"(?P<pid>\d+)\s+(?P<user>\S+)\s+(?P<priority>\d+)\s+(?P<nice>\d+)\s+(?P<mem_virt_val>[\d\.]+)(?P<mem_virt_unit>\S*)\s+(?P<mem_res_val>[\d\.]+)(?P<mem_res_unit>\S*)\s+(?P<mem_shr_val>[\d\.]+)(?P<mem_shr_unit>\S*)\s+(?P<status>\S+)\s+(?P<cpu_perc>[\d\.]+)\s+(?P<mem_perc>[\d\.]+)\s+(?P<time>[\d\.:]+)\s+(?P<command>\S+)", top_output)
        #print("top_parsed=%s" % top_parsed)


        if top_parsed:
            # print csv header
            #print('timestamp,container_id,pid,user,priority,nice,mem_virt_bytes,mem_res_bytes,mem_shr_bytes,status,cpu_perc,mem_perc,time,command')
            
            for line in top_parsed:
                pid = line[0]
                user = line[1]
                priority = line[2]
                nice = line[3]
                mem_virt_val = line[4]
                mem_virt_unit = line[5]
                mem_res_val = line[6]
                mem_res_unit = line[7]
                mem_shr_val = line[8]
                mem_shr_unit = line[9]
                status = line[10]
                cpu_perc = line[11]
                mem_perc = line[12]
                time = line[13]
                command = line[14]
                
                # translate units like GiB into multipliers
                if mem_virt_unit:
                    mem_virt_bytes = unit_translation(mem_virt_val, mem_virt_unit)
                else:
                    mem_virt_bytes = int(mem_virt_val) * 1024
                    
                if mem_res_unit:
                    mem_res_bytes = unit_translation(mem_res_val, mem_res_unit)
                else:
                    mem_res_bytes = int(mem_res_val) * 1024
                    
                if mem_shr_unit:
                    mem_shr_bytes = unit_translation(mem_shr_val, mem_shr_unit)
                else:
                    mem_shr_bytes = int(mem_shr_val) * 1024


                print('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"%s"' % (ts, container_id, pid, user, priority, nice, mem_virt_bytes, mem_res_bytes, mem_shr_bytes, status, cpu_perc, mem_perc, time, command))
