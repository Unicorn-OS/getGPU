#!/usr/bin/python3
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

def get_pci_device():
    data = get_lshw()
    device = data["children"][0]["children"]

    num = 0
    for d in device:
        if d["id"] == "pci":
            return num
            # break
        num += 1

def get_pci_gpu():
    # Find GPU on a PCI bus
    data = get_lshw()
    num = get_pci_device()
    gpu = data["children"][0]["children"][num]["children"][0]["product"]    
    return gpu


def find_gpu():
    
    # Real GPUs
    amd_discrete, amd_integrated = False, False
    intel_discrete, intel_integrated = False, get_pci_gpu() == "HD Graphics"
    nvidia_discrete, nvidia_integrated = False, False

    # Virtual GPU
    virtio_gpu = get_pci_gpu() == "Virtio GPU"

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
            "gpu": virtio_gpu,
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
    gpu = find_gpu()
    module = AnsibleModule(argument_spec={})
    module.exit_json(hw=gpu)

    # bac.Works
    # module.exit_json(meta=gpu)

    # Debug
    # print(get_gpu())
    # print(gpu)

if __name__ == '__main__':  
    main()
