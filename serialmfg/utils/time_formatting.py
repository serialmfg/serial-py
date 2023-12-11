from datetime import datetime

def is_iso_timestamp(timestamp):
    """Checks if a timestamp is in ISO 8601 format

    Args:
        timestamp (str): timestamp to check

    Returns:
        bool: True if timestamp is in ISO 8601 format, False otherwise
    """
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        print(f"Invalid timestamp format - {timestamp} could not be converted to ISO 8601")
        return False
