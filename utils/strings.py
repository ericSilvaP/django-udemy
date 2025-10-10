def is_positive_number(n):
    try:
        n = float(n)
    except (ValueError, TypeError):
        return False

    return n > 0
