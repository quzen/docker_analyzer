import subprocess
import sys

# call subprocess function
def call_subprocess(command):
    output_str = ""
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if sys.version_info >= (3,):
        output_str = str(output.communicate()[0], "utf-8")
    else:
        output_str = output.communicate()[0]

    return output_str


# translate units into value multiplier
def unit_translation(value, unit):
    value = float(value)
    
    if unit.lower().startswith('tib'):
        translated = int(value * 1024 * 1024 * 1024 * 1024)
    elif unit.lower().startswith('gib'):
        translated = int(value * 1024 * 1024 * 1024)
    elif unit.lower().startswith('mib'):
        translated = int(value * 1024 * 1024)
    elif unit.lower().startswith('kib'):
        translated = int(value * 1024)
    elif unit.lower().startswith('t'):
        translated = int(value * 1000000000000)
    elif unit.lower().startswith('g'):
        translated = int(value * 1000000000)
    elif unit.lower().startswith('m'):
        translated = int(value * 1000000)
    elif unit.lower().startswith('k'):
        translated = int(value * 1000)
    elif unit.lower().startswith('b'):
        translated = int(value)
    else:
        translated = value
    
    return translated
