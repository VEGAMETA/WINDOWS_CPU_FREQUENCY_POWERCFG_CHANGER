import clr

clr.AddReference(r'OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer


class MyComputer(Computer):
    def __init__(self) -> None:
        super().__init__()
        self.CPUEnabled = True
        self.GPUEnabled = True
        self.Open()
        self.cpu_index: int = self.get_cpu_index()
        self.gpu_index: int = self.get_gpu_index()

    def get_cpu_index(self) -> int:
        last_index: int = 0
        for index in range(0, len(self.Hardware[0].Sensors)):
            if "/temperature" in str(self.Hardware[0].Sensors[index].Identifier):
                last_index = index
        return last_index

    def get_gpu_index(self) -> int:
        last_index: int = 0
        for index in range(0, len(self.Hardware[1].Sensors)):
            if "/temperature" in str(self.Hardware[1].Sensors[index].Identifier):
                last_index = index
        return last_index

    def get_cpu_temperature(self) -> str:
        temperature: str = str(self.Hardware[0].Sensors[self.cpu_index].get_Value())[:-2]
        self.Hardware[0].Update()
        return temperature

    def get_gpu_temperature(self) -> str:
        temperature: str = str(self.Hardware[1].Sensors[self.gpu_index].get_Value())[:-2]
        self.Hardware[1].Update()
        return temperature

    def get_str_gpu_temperature(self) -> str:
        return "GPU - " + self.get_gpu_temperature() + "°C"

    def get_str_cpu_temperature(self) -> str:
        return "CPU - " + self.get_cpu_temperature() + "°C"
