import subprocess


def set_frequency(value: int) -> None:
    commands: str = \
        f"powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX {value} && " \
        f"powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX {value} && " \
        "powercfg /S SCHEME_CURRENT"

    subprocess.run(commands, shell=True)


def get_frequency() -> int:
    return int(subprocess.Popen(
        'powercfg /query SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX',
        stdout=subprocess.PIPE
    ).stdout.read()[-12:-4], 16)
