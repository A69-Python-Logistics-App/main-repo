def try_parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        raise ValueError("Invalid integer provided!")