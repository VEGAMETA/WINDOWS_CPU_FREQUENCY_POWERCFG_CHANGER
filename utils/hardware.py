import clr
from utils.wrappers import singleton

clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer, HardwareType, SensorType

temperature_sensors_names = ("CPU Package", "GPU Core")


class Component:
    def __init__(self, hardware=None, temperature_sensor=None) -> None:
        self._hardware = hardware
        self._temperature_sensor = temperature_sensor

    def set_hardware(self, hardware) -> None:
        self._hardware = hardware

    def get_hardware(self):
        return self._hardware

    def set_temperature_sensor(self) -> None:
        for sensor in self._hardware.Sensors:
            if sensor.SensorType == SensorType.Temperature and sensor.Name in temperature_sensors_names:
                self._temperature_sensor = sensor
                return None

    def get_temperature(self) -> int:
        self._hardware.Update()
        return int(self._temperature_sensor.get_Value())


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
            self._cpu_component.set_hardware(hardware) if hardware.HardwareType == HardwareType.CPU else ...
            self._gpu_component.set_hardware(hardware) if hardware.HardwareType in (HardwareType.GpuAti,
                                                                                    HardwareType.GpuNvidia) else ...

    def _set_components_temperature_sensors(self) -> None:
        self._cpu_component.set_temperature_sensor() if self._cpu_component.get_hardware() else ...
        self._gpu_component.set_temperature_sensor() if self._gpu_component.get_hardware() else ...

    def get_cpu_temperature(self) -> str:
        return f"CPU - {self._cpu_component.get_temperature()}°C" if self._cpu_component.get_hardware() else "CPU - ERR"

    def get_gpu_temperature(self) -> str:
        return f"GPU - {self._gpu_component.get_temperature()}°C" if self._gpu_component.get_hardware() else "GPU - IGP"
