#
# Validation functions for input parameters
#

def get_login_info(msg: str) -> list[str]:
    cmd = input(msg + " ({username} {password}) > ").split()
    if cmd[0] == "exit":
        raise SystemExit
    if len(cmd) != 2:
        raise ValueError("Invalid parameters, two expected ({username} {password})!")
    return cmd

def parse_to_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid number ({value}) provided!")
