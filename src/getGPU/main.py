import json
import subprocess
from contextlib import redirect_stdout
import io

# Todo: Make this work on ARM, RISCV, and x86!

# Get GPUs from `lshw -json`
# https://github.com/ansible/ansible/issues/72220#issuecomment-1021551392

debug = False
# debug = True

def debug_write():
    name = "lshw"
    byte = subprocess.check_output(['lshw', '-json'])
    file = f"/home/me/Desktop/{name}.json"
    f = open(file, "wb")
    f.write(byte)
    f.close()


def get_intel_integrated():
    data = get_lshw()
    device = data["children"][0]["children"][2]["children"][1]["product"]
    return "HD Graphics" in device


def find_gpu():
    amd_discrete_gpu = False
    amd_integrated_gpu = False
    intel_discrete_gpu = False
    intel_integrated_gpu = get_intel_integrated()
    nvidia_discrete_gpu = False
    # For APUs like Nvidia Jetson, & Grace Hopper
    nvidia_integrated_gpu = False

    gpus = {
        "AMD": {
            "discrete": amd_discrete_gpu,
            "integrated": amd_integrated_gpu,
        },
        "Intel": {
            "discrete": intel_discrete_gpu,
            "integrated": intel_integrated_gpu,
        },
        "Nvidia": {
            "discrete": nvidia_discrete_gpu,
            "integrated": nvidia_integrated_gpu,
        },
    }

    return gpus

def get_lshw():
    ori = subprocess.check_output(['lshw', '-json']).decode('ascii')

    data = json.loads(ori)
    return data

def stdout():
    f = io.StringIO()
    with redirect_stdout(f):
        help(pow)
    s = f.getvalue()

if __name__ == '__main__':
    gpus = find_gpu()
    if debug:
        debug_write()
        print(gpus)