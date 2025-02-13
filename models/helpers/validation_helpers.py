#
# Validation functions for input parameters
#

def parse_to_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid number ({value}) provided!")