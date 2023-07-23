# WINDOWS_CPU_FREQUENCY_POWERCFG_CHANGER

### A tool for limiting max CPU frequency in Windows by changing powercfg settings
- Useful for laptops
- Prevents power overuse
- Prevents overheating during the routine use or downtime
- Full max CPU frequency control

## Installation
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

## Config
Check `config.ini` and read the comments
###

## Additionally
If you want to run the script hidden in system tray from a start run:
```bat
freq.bat -h
```
You can autorun the script by creating `freq.bat` task in the windows task scheduler 
adding the `-h` argument if you want to run hidden in a system tray as well
###
To change frequency manually in windows power settings you must unhide 
`PROCFREQMAX` 
attribute by running following command (if you ran the script it runs 
automatically (if an attribute was hidden))
```bat
powercfg -attributes SUB_PROCESSOR PROCFREQMAX -ATTRIB_HIDE
```
###

###### Use at your own risk, the programmer is not responsible

