"""
Docker inventory for Splunk
"""
from utils import call_subprocess

if __name__ == '__main__':
    inventory_output = call_subprocess('docker inspect $(docker ps -aq)')
    
    if inventory_output:
        print("%s" % inventory_output)
