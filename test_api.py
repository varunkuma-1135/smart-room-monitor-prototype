"""Small API tests. Run while app.py is running in another terminal."""
import unittest
import requests

BASE = "http://127.0.0.1:5000"

class SmartRoomApiTests(unittest.TestCase):
    def test_normal_reading(self):
        r = requests.post(BASE + "/api/data", json={
            "device_id": "test-room", "temperature": 25, "humidity": 50
        })
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["status"], "NORMAL")

    def test_high_temperature(self):
        r = requests.post(BASE + "/api/data", json={
            "device_id": "test-room", "temperature": 40, "humidity": 50
        })
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["status"], "HIGH_TEMP")

    def test_high_humidity(self):
        r = requests.post(BASE + "/api/data", json={
            "device_id": "test-room", "temperature": 25, "humidity": 90
        })
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["status"], "HIGH_HUMIDITY")

    def test_missing_field(self):
        r = requests.post(BASE + "/api/data", json={
            "device_id": "test-room", "temperature": 25
        })
        self.assertEqual(r.status_code, 400)

    def test_latest_endpoint(self):
        self.assertEqual(requests.get(BASE + "/api/latest").status_code, 200)

    def test_history_endpoint(self):
        r = requests.get(BASE + "/api/history?limit=5")
        self.assertEqual(r.status_code, 200)
        self.assertLessEqual(len(r.json()), 5)

    def test_stats_endpoint(self):
        r = requests.get(BASE + "/api/stats")
        self.assertEqual(r.status_code, 200)
        self.assertIn("alerts", r.json())

if __name__ == "__main__":
    unittest.main(verbosity=2)
