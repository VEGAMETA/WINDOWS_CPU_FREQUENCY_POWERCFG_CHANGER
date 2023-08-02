import clr
from utils.wrappers import singleton

clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer, HardwareType, SensorType

temperature_sensors_names = ("CPU Package", "GPU Core")


class Component:
    def __init__(self, hardware=None, temperature_sensor=None) -> None:
        self.hardware = hardware
        self.temperature_sensor = temperature_sensor

    def set_temperature_sensor(self) -> None:
        for sensor in self.hardware.Sensors:
            if sensor.SensorType == SensorType.Temperature and sensor.Name in temperature_sensors_names:
                self.temperature_sensor = sensor
                return None

    def get_temperature(self) -> int:
        self.hardware.Update()
        return int(self.temperature_sensor.get_Value())


@singleton
class MyComputer(Computer):
    def __init__(self) -> None:
        super().__init__()
        self.CPUEnabled = True
        self.GPUEnabled = True
        self.Open()

        self._cpu_component = Component()
        self._gpu_component = Component()

        self._set_components_hardware()
        self._set_components_temperature_sensors()

    def _set_components_hardware(self) -> None:
        for hardware in self.Hardware:
            hardware.Update()
            if hardware.HardwareType == HardwareType.CPU:
                self._cpu_component.hardware = hardware
            elif hardware.HardwareType in (HardwareType.GpuAti, HardwareType.GpuNvidia):
                self._gpu_component.hardware = hardware

    def _set_components_temperature_sensors(self) -> None:
        self._cpu_component.set_temperature_sensor() if self._cpu_component.hardware else ...
        self._gpu_component.set_temperature_sensor() if self._gpu_component.hardware else ...

    def get_cpu_temperature(self) -> str:
        return f"CPU - {self._cpu_component.get_temperature()}°C" if self._cpu_component.temperature_sensor \
            else "CPU - ERR"

    def get_gpu_temperature(self) -> str:
        return f"GPU - {self._gpu_component.get_temperature()}°C" if self._gpu_component.temperature_sensor \
            else "GPU - IGP"
