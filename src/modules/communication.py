def encode_data(tag: str, temp: float, request: bool):
    if request:
        return f"{tag}:{temp}:1"
    else:
        return f"{tag}:{temp}:0"

def decode_data(data: str):
    parts = data.split(":")
    return parts[0], float(parts[1]), parts[2] == "1"