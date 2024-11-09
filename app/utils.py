import datetime 

def generate_response(topic: str, description: str):
    # Simulated response generation logic
    current_date = str(datetime.datetime.now())
    return {
        "created_at": current_date,
        "status": "To Do",
        "topic": topic,
        "description": description,
        "device": "Ноутбук",
        "failure_point": "Блок питания",
        "serial_number": "CH2200202"
    }
