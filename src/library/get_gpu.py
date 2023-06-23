#!/usr/bin/python
from ansible.module_utils.basic import *
import json
import subprocess

USER = "me"

# Todo: Make this work on ARM, RISCV, and x86!

# Gets GPUs from `lshw -json`
# Sends them to Ansible as a dictionary

# source:
# https://github.com/ansible/ansible/issues/72220#issuecomment-1021551392
# https://serverfault.com/questions/868770/ansible-pass-dictionary-from-python-script

def get_intel():
    data = get_lshw()
    device = data["children"][0]["children"][2]["children"][1]["product"]
    
    integrated = "HD Graphics" in device
    discrete = False
    
    return (discrete, integrated)

def get_virtio():
    data = get_lshw()
    device = data["children"][0]["children"][2]["children"][1]["product"]
    
    integrated = "Virtio GPU" in device
    discrete = False
    
    return (discrete, integrated)


def find_gpu():
    
    # Real GPUs
    amd_discrete, amd_integrated = False, False
    intel_discrete, intel_integrated = get_intel()
    nvidia_discrete, nvidia_integrated = False, False

    # Virtual GPU
    virtio_discrete, virtio_integrated = get_intel()
    # For APUs like Nvidia Jetson, & Grace Hopper

    gpus = {
        "amd": {
            "discrete": amd_discrete,
            "integrated": amd_integrated,
        },
        "intel": {
            "discrete": intel_discrete,
            "integrated": intel_integrated,
        },
        "nvidia": {
            "discrete": nvidia_discrete,
            "integrated": nvidia_integrated,
        },
        "virtio": {
            "discrete": virtio_discrete,
            "integrated": virtio_integrated,
        },
    }

    return gpus

def get_lshw():
    ori = subprocess.check_output(['lshw', '-json']).decode('ascii')

    data = json.loads(ori)
    return data

def _test():
    dbg = False
    print(find_gpu())

    def _dbg_write():
        # Write lshw to ~/Desktop
        name = "lshw"
        byte = subprocess.check_output(['lshw', '-json'])
        file = f"/home/{USER}/Desktop/{name}.json"
        f = open(file, "wb")
        f.write(byte)
        f.close()

    if dbg:
        _dbg_write()

def main():
    module = AnsibleModule(argument_spec={})
    gpu = find_gpu()
    module.exit_json(hw=gpu)

    # Works
    # module.exit_json(meta=gpu)

if __name__ == '__main__':  
    main()
