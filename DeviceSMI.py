import os
import subprocess

import psutil
import torch

DEVICE_NAME = "Name"
MEMORY_TOTAL = "Memory-total"
MEMORY_USED = "Memory-in-use"
MEMORY_PROCESS = "Process memory"
UTILIZATION = "Utilization"
PCIE_BUS_ID = "PCIe Bus ID"
PCIE_GEN = "PCIe Gen"
PCIE_LINK = "PCIe Link"
DRIVER_VERSION = "Driver Version"
MANUFACTURE = "Manufacturer"


class BaseInfo:
    def __init__(self, name: str, model: str, manufacture: str, memory_total: int, memory_used: int, memory_process: int, utilization: int):
        self.name = name
        self.model = model
        self.manufacture = manufacture
        self.memory_total = memory_total
        self.memory_used = memory_used
        self.memory_process = memory_process
        self.utilization = utilization


class DeviceSMI():
    def __init__(self, device: torch.device):
        self.device = device

    def get_info(self):
        if self.device.type == 'cuda':
            try:
                cudas = os.environ.get("CUDA_VISIBLE_DEVICES")
                if cudas and len(cudas) >= self.device.index:
                    gpu_id = cudas[self.device.index]
                else:
                    gpu_id = self.device.index  # or raise Exception?

                args = [
                    'nvidia-smi',
                    f'--id={gpu_id}',
                    '--query-gpu='
                    'name,'
                    'memory.total,'
                    'memory.used,'
                    'utilization.gpu,'
                    'pci.bus_id,'
                    'pcie.link.gen.max,'
                    'pcie.link.gen.current,'
                    'driver_version',
                    '--format=csv,noheader,nounits'
                ]
                print(f"command: {''.join(args).replace('--', ' --')}")
                result = subprocess.run(
                    args=args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                if result.returncode != 0:
                    raise RuntimeError(result.stderr)

                output = result.stdout.strip().split('\n')[0]
                name, total_memory, used_memory, utilization, pci_bus_id, pcie_gen, pcie_width, driver_version = output.split(', ')

                return {
                    DEVICE_NAME: name,
                    MEMORY_TOTAL: int(total_memory),
                    MEMORY_USED: int(used_memory),
                    UTILIZATION: int(utilization),
                    PCIE_BUS_ID: pci_bus_id,
                    PCIE_GEN: f"Gen{pcie_gen}",
                    PCIE_LINK: f"x{pcie_width}",
                    DRIVER_VERSION: driver_version,
                }
            except FileNotFoundError:
                return {"Error": "nvidia-smi command not found. Ensure NVIDIA drivers are installed."}
            except Exception as e:
                return {"Error": str(e)}
        elif self.device.type == 'cpu':
            cpu_info = {
                DEVICE_NAME: "CPU",
                MANUFACTURE: "Generic" if psutil.MACOS else "Intel/AMD",
                UTILIZATION: psutil.cpu_percent(interval=1),
                MEMORY_USED: psutil.virtual_memory().percent,
                MEMORY_TOTAL: psutil.virtual_memory().total,
                MEMORY_PROCESS: psutil.Process().memory_info().rss,
            }
            return cpu_info
        else:
            return {"Error": "Device not supported or unavailable"}
