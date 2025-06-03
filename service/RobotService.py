from repository import RobotRepository

def process_data(data: dict):
    print(f"[Service] Data received at {data['timestamp']}")
    RobotRepository.save_data(data)

def get_data():
    return RobotRepository.get_latest_data()