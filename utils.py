def get_week(today):
    # Will never return 0, will return 13 instead
    return (today.isocalendar()[1] % 13) or 13

def get_quarter(today):
    return (today.month - 1) // 3 + 1

def get_year(today):
    # This will break in year 2100
    return today.year % 100
