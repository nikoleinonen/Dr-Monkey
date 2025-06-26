def format_large_number(number: int | float) -> str:
    """
    Formats a number with spaces as thousand separators and handles float precision.
    Integers are formatted without decimals. Floats are formatted to 2 decimal places.
    Example: 12345 -> "12 345", 123.456 -> "123.46".
    """
    if isinstance(number, float):
        return f"{number:,.2f}".replace(",", " ")
    return f"{int(number):,}".replace(",", " ")
