# WINDOWS_CPU_FREQUENCY_POWERCFG_CHANGER

### A tool for limiting max CPU frequency in Windows by changing powercfg settings

- Useful for laptops
- Prevents power overuse
- Prevents overheating during the routine use or downtime
- Full max CPU frequency control

![img](https://github.com/VEGAMETA/WINDOWS_CPU_FREQUENCY_POWERCFG_CHANGER/assets/100537523/e65d4541-b952-4d83-92e7-ffedbbb9bc95)

## Requirements

- Windows
- Python >= 3.8
- Git (optional)
- UAC admin rights accessibility

## Installation
###### (Make sure Python is in your system PATH environment variable)
Default installation:

```bat
git clone https://github.com/VEGAMETA/WINDOWS_CPU_FREQUENCY_POWERCFG_CHANGER.git
cd WINDOWS_CPU_FREQUENCY_POWERCFG_CHANGER

python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

## Running

To run the script you can use (and modify as you want) `freq.bat` or run by command:

```bat
.\venv\Scripts\pythonw .\main.py
```

or

```bat
.\freq
```

## Configuration

Check `config.ini` and read the comments

###

## Additionally

#### Turn off any other built-in or other limiter utilities for proper operation.

If you want to run the script hidden in system tray from a start run:

```bat
freq.bat -h
```

###

To change frequency manually in windows power settings you must unhide `PROCFREQMAX` attribute by running following
command (runs automatically if an attribute was hidden)

```bat
powercfg -attributes SUB_PROCESSOR PROCFREQMAX -ATTRIB_HIDE
```

###

Make sure that script execution is enabled if you activate the venv in powershell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

###

This command stops the service, so you can delete OpenHardwareMonitorLib.sys file if you need to:

```bat
sc stop WinRing0_1_2_0
```

#

###### Use at your own risk, the developer is not responsible.

