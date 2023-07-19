import clr

clr.AddReference(r'OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer


class MyComputer(Computer):
    def __init__(self):
        super().__init__()
        self.CPUEnabled = True
        self.GPUEnabled = True
        self.Open()
        self.cpu_index = self.get_cpu_index()
        self.gpu_index = self.get_gpu_index()

    def get_cpu_index(self):
        last_index = 0
        for index in range(0, len(self.Hardware[0].Sensors)):
            if "/temperature" in str(self.Hardware[0].Sensors[index].Identifier):
                last_index = index
        return last_index

    def get_gpu_index(self):
        last_index = 0
        for index in range(0, len(self.Hardware[1].Sensors)):
            if "/temperature" in str(self.Hardware[1].Sensors[index].Identifier):
                last_index = index
        return last_index

    def get_cpu_temperature(self):
        temperature = str(self.Hardware[0].Sensors[self.cpu_index].get_Value())[:-2]
        self.Hardware[0].Update()
        return temperature

    def get_gpu_temperature(self):
        temperature = str(self.Hardware[1].Sensors[self.gpu_index].get_Value())[:-2]
        self.Hardware[1].Update()
        return temperature
