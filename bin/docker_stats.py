"""
Docker stats for Splunk
"""
import argparse
import re
import time
from utils import call_subprocess, unit_translation

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--label', action='store', type=str)

    args = my_parser.parse_args()
    
    ts = int(time.time())
    stats_output = call_subprocess('docker stats --no-stream=true --format "{{.ID}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}"')
    stats_output = str(stats_output, "utf-8")

    ps_output = call_subprocess('docker ps -a --format "{{.ID}}\t{{.Image}}\t{{.Names}}\t{{.CreatedAt}}\t{{.Status}}\t{{.Labels}}"')
    ps_output = str(ps_output, "utf-8")

    ps_parsed = re.findall(r"(?P<container_id>\S+)\t(?P<image>[^\t]+)\t(?P<names>[^\t]+)\t(?P<created_at>[^\t]+)\t(?P<status_short>\S+)\s+(?P<status_since>[^\t]+)\t(?P<labels>[^\n]+)", ps_output)

    stats_parsed = re.findall(r"(?P<container_id>\S+)\t(?P<cpu_perc>[\d\.]+)%\t(?P<mem_usage_val>[\d\.]+)(?P<mem_usage_unit>\S+) \/ (?P<mem_limit_val>[\d\.]+)(?P<mem_limit_unit>\S+)\t(?P<mem_perc>[\d\.]+)%\t(?P<netio_sent_val>[\d\.]+)(?P<netio_sent_unit>\S+) \/ (?P<netio_recv_val>[\d\.]+)(?P<netio_recv_unit>\S+)\t(?P<blockio_read_val>[\d\.]+)(?P<blockio_read_unit>\S+) \/ (?P<blockio_write_val>[\d\.]+)(?P<blockio_write_unit>\S+)\t(?P<pid_count>\d+)", stats_output)

    ps_data = dict()
    if ps_parsed:
        for line in ps_parsed:
            container_id = line[0]
            image = line[1]
            names = line[2]
            created_at = line[3]
            status_short = line[4]
            status_since = line[5]
            labels = line[6]
                
            if args.label in labels:
                label_re = r"" + args.label + "=(?P<label>[^,]+)"
                label_parsed = re.findall(label_re, labels)
                labels = label_parsed[0]
            else:
                labels = "NoLabel"
            
            ps_data.setdefault(container_id, {})
            ps_data[container_id]['image'] = image
            ps_data[container_id]['names'] = names
            ps_data[container_id]['created_at'] = created_at
            ps_data[container_id]['status_short'] = status_short
            ps_data[container_id]['status_since'] = status_since
            ps_data[container_id]['labels'] = labels

    if stats_parsed:
        for line in stats_parsed:
            container_id = line[0]
            cpu_perc = line[1]
            mem_usage_val = line[2]
            mem_usage_unit = line[3]
            mem_limit_val = line[4]
            mem_limit_unit = line[5]
            mem_perc = line[6]
            netio_sent_val = line[7]
            netio_sent_unit = line[8]
            netio_recv_val = line[9]
            netio_recv_unit = line[10]
            blockio_read_val = line[11]
            blockio_read_unit = line[12]
            blockio_write_val = line[13]
            blockio_write_unit = line[14]
            pid_count = line[15]
            
            if ps_data.get(container_id):
                image = ps_data[container_id]['image']
                names = ps_data[container_id]['names']
                created_at = ps_data[container_id]['created_at']
                status_short = ps_data[container_id]['status_short']
                status_since = ps_data[container_id]['status_since']
                labels = ps_data[container_id]['labels']
            else:
                image = ''
                names = ''
                created_at = ''
                status_short = ''
                status_since = ''
                labels = ''
            
            # translate units like GiB into multipliers
            mem_usage_bytes = unit_translation(mem_usage_val, mem_usage_unit)
            mem_limit_bytes = unit_translation(mem_limit_val, mem_limit_unit)
            netio_sent_bytes = unit_translation(netio_sent_val, netio_sent_unit)
            netio_recv_bytes = unit_translation(netio_recv_val, netio_recv_unit)
            blockio_read_bytes = unit_translation(blockio_read_val, blockio_read_unit)
            blockio_write_bytes = unit_translation(blockio_write_val, blockio_write_unit)


            print('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"%s","%s",%s,%s,%s,"%s"' % (ts, container_id, cpu_perc, mem_usage_bytes, mem_limit_bytes, mem_perc, netio_sent_bytes, netio_recv_bytes, blockio_read_bytes, blockio_write_bytes, pid_count, image, names, created_at, status_short, status_since, labels))
