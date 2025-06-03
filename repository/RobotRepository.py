latest_data = {}

def save_robot_data(data: dict):
    global latest_data
    latest_data = data

def get_latest_data():
    return latest_data