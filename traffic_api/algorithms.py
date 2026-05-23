def calculate_signal(vehicle_count, emergency_vehicle=False):

    # Safe type handling 
    try:
        vehicle_count = int(vehicle_count)
    except:
        return {
            "signal": "RED",
            "green_time": 0,
            "traffic_level": "INVALID"
        }

    emergency_vehicle = str(emergency_vehicle).lower() == "true"

    # Emergency vehicle highest priority
    if emergency_vehicle:
        return {
            "signal": "GREEN",
            "green_time": 60,
            "traffic_level": "EMERGENCY"
        }

    #  Invalid data 
    if vehicle_count < 0:
        return {
            "signal": "RED",
            "green_time": 0,
            "traffic_level": "INVALID"
        }

    #  Low traffic 
    if vehicle_count <= 10:
        return {
            "signal": "RED",
            "green_time": 15,
            "traffic_level": "LOW"
        }

    #  Medium traffic 
    elif vehicle_count <= 30:
        return {
            "signal": "YELLOW",
            "green_time": 30,
            "traffic_level": "MEDIUM"
        }

    #  High traffic 
    elif vehicle_count <= 60:
        return {
            "signal": "GREEN",
            "green_time": 45,
            "traffic_level": "HIGH"
        }

    #  Very high traffic 
    else:
        return {
            "signal": "GREEN",
            "green_time": 60,
            "traffic_level": "VERY HIGH"
        }