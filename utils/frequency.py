import subprocess


def un_hide_frequency() -> None:
    command: str = "powercfg -attributes SUB_PROCESSOR PROCFREQMAX -ATTRIB_HIDE"
    subprocess.run(command, shell=True)


def set_frequency(value: int) -> None:
    command: str = \
        f"powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX {value} && " \
        f"powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX {value} && " \
        "powercfg /S SCHEME_CURRENT"
    subprocess.run(command, shell=True)


def get_frequency() -> int:
    try:
        return int(subprocess.run(
            'powercfg /query SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX',
            capture_output=True, shell=True).stdout[-12:-4], 16)
    except ValueError:
        un_hide_frequency()
        return get_frequency()
