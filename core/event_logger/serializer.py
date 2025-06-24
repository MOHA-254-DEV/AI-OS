import json

def serialize_event(event_dict, pretty=False):
    """
    Serialize a dictionary to a JSON string.

    Args:
        event_dict (dict): Event data.
        pretty (bool): If True, format with indentation for readability.

    Returns:
        str: JSON-formatted string.
    """
    try:
        return json.dumps(event_dict, indent=4 if pretty else None)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Serialization error: {e}")

def deserialize_event(event_str, object_hook=None):
    """
    Deserialize a JSON string back to a dictionary.

    Args:
        event_str (str): JSON-formatted string.
        object_hook (callable, optional): Custom hook for decoding objects.

    Returns:
        dict: The original dictionary.
    """
    try:
        return json.loads(event_str, object_hook=object_hook)
    except (json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"Deserialization error: {e}")
