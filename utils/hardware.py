import clr

clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer, HardwareType, SensorType


class MyComputer(Computer):
    def __init__(self) -> None:
        super().__init__()
        self.CPUEnabled = True
        self.GPUEnabled = True
        self.Open()
        self.get_sensors()

    def get_sensors(self) -> None:
        for hardware in self.Hardware:
            if hardware.HardwareType == HardwareType.CPU:
                for sensor in hardware.Sensors:
                    if sensor.SensorType == SensorType.Temperature and "CPU Package" in sensor.Name:
                        self.cpu_sensor = sensor
                        break
            if hardware.HardwareType in (HardwareType.GpuAti, HardwareType.GpuNvidia):
                for sensor in hardware.Sensors:
                    if sensor.SensorType == SensorType.Temperature and "GPU Core" in sensor.Name:
                        self.gpu_sensor = sensor
                        break

    def get_cpu_temperature(self) -> str:
        temperature: str = str(self.cpu_sensor.get_Value())[:-2]
        self.Hardware[0].Update()
        return temperature

    def get_gpu_temperature(self) -> str:
        temperature: str = str(self.gpu_sensor.get_Value())[:-2]
        self.Hardware[1].Update()
        return temperature

    def get_str_gpu_temperature(self) -> str:
        return "GPU - " + self.get_gpu_temperature() + "°C"

    def get_str_cpu_temperature(self) -> str:
        return "CPU - " + self.get_cpu_temperature() + "°C"
