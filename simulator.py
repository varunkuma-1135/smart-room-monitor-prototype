"""Virtual sensors for the Smart Room Monitor prototype."""
import random
import time
import requests
import sys

API_URL = "http://127.0.0.1:5000/api/data"
ROOMS = {
    "living-room": 28.0,
    "bedroom": 27.0,
    "kitchen": 30.0,
}

def make_reading(room, base_temperature):
    temperature = base_temperature + random.uniform(-2, 3)
    humidity = random.uniform(45, 75)
    # Occasionally create an alert so the alert feature can be demonstrated.
    if random.random() < 0.12:
        temperature += random.uniform(7, 10)
    if random.random() < 0.08:
        humidity = random.uniform(82, 95)
    return {
        "device_id": room,
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1)
    }

def main():
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 1
    for number in range(rounds):
        for room, base in ROOMS.items():
            reading = make_reading(room, base)
            try:
                response = requests.post(API_URL, json=reading, timeout=5)
                print(room, response.status_code, response.json())
            except requests.RequestException as error:
                print("Could not connect to the API. Start app.py first.", error)
                return
        time.sleep(delay)
    print(f"Finished: sent readings for {rounds} rounds.")

if __name__ == "__main__":
    main()
