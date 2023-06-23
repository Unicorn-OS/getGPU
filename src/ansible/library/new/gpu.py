from ansible.module_utils.basic import *

debug = False

class Lshw():
    import json, subprocess

    def __init__(self):
        self.data = Lshw.get_lshw()

    def get_lshw():
        ori = subprocess.check_output(['lshw', '-json']).decode('ascii')
        data = json.loads(ori)
        return data

    def pci_num(self):
        device = self.data["children"][0]["children"]
        num = 0
        for d in device:
            if d["id"] == "pci":
                return num
                # break
            num += 1

class GPU():
    def __init__(self):
        self.lshw = Lshw()
        self.data = self.lshw.data
        self.gpu = self._get_gpu()
        self.intel = self._has_intel()


    def _has_intel(self):
        integrated = "HD Graphics" in self.gpu
        return integrated

    def _get_gpu(self):
        pci_num = self.lshw.pci_num()

        pci_devices = self.data["children"][0]["children"][pci_num]["children"]

        display = 0
        for p in pci_devices:
            if p["id"] == "display":
                break
            display += 1
    
        # works
        gpu = self.data["children"][0]["children"][pci_num]["children"][display]["product"]

        # debug
        if debug:
            print(f"GPU: {gpu}")
            return
        else:
            return gpu


gpu = GPU()
print(f"Intel: {gpu.intel} model: {gpu.gpu}")