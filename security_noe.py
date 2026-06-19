import random
import time
import json
import requests
from datetime import datetime

class SecurityNode:
    def __init__(self, node_id="NODE-001"):
        self.node_id = node_id
        self.wifi_ssid = "DecodeLabs_Network"
        self.wifi_status = "Disconnected"
        self.distance = 0
        self.motion_detected = False
        self.alerts = []
        self.cloud_url = "https://api.adafruit.io/api/v2/feeds/security-data"
        self.api_key = "YOUR_API_KEY_HERE"

    def connect_wifi(self):
        print(f"\n📶 Connecting to Wi-Fi: {self.wifi_ssid}...")
        time.sleep(2)
        self.wifi_status = "Connected"
        print(f"✅ Wi-Fi connected successfully!")
        print(f"   IP Address: 192.168.1.{random.randint(10, 99)}")

    def read_ultrasonic_sensor(self):
        self.distance = random.randint(5, 150)
        self.motion_detected = self.distance < 30
        return self.distance

    def check_intruder(self):
        if self.motion_detected:
            alert = {
                "timestamp": datetime.now().isoformat(),
                "type": "INTRUDER DETECTED",
                "distance": self.distance,
                "node_id": self.node_id,
                "status": "ALERT"
            }
            self.alerts.append(alert)
            return alert
        return None

    def publish_data_http(self, data):
        try:
            payload = {
                "value": json.dumps(data)
            }
            headers = {
                "X-AIO-Key": self.api_key,
                "Content-Type": "application/json"
            }
            print(f"📤 Publishing data via HTTP POST...")
            # Simulated API call
            print(f"   Data: {json.dumps(data, indent=2)}")
            return True
        except Exception as e:
            print(f"   ❌ Error publishing: {e}")
            return False

    def simulate_telemetry(self, duration=15):
        print("\n" + "=" * 60)
        print("   CLOUD-CONNECTED SECURITY NODE")
        print("=" * 60)
        print(f"Node ID: {self.node_id}")
        print("=" * 60 + "\n")

        self.connect_wifi()

        print("\n🔍 Starting Security Monitoring...")
        print("   Distance < 30cm = INTRUDER DETECTED")
        print("=" * 60 + "\n")

        try:
            for i in range(duration):
                distance = self.read_ultrasonic_sensor()
                timestamp = datetime.now().strftime("%H:%M:%S")

                print(f"[{timestamp}] 📡 Distance: {distance}cm")

                if self.motion_detected:
                    alert = self.check_intruder()
                    if alert:
                        print(f"   🚨 INTRUDER DETECTED! Distance: {distance}cm")
                        self.publish_data_http(alert)
                else:
                    print(f"   ✅ Clear - No Motion")

                # Simulate cloud display
                self.display_cloud_dashboard(i + 1)

                time.sleep(1)

        except KeyboardInterrupt:
            print("\n👋 Security node stopped by user.")

        print("\n" + "=" * 60)
        print("   SECURITY NODE SUMMARY")
        print("=" * 60)
        print(f"Total Alerts: {len(self.alerts)}")
        print(f"Wi-Fi Status: {self.wifi_status}")
        if self.alerts:
            print("\nAlert Log:")
            for alert in self.alerts:
                print(f"  🚨 {alert['timestamp']} - {alert['type']} at {alert['distance']}cm")

    def display_cloud_dashboard(self, reading_count):
        if reading_count % 3 == 0:
            print("\n" + "-" * 40)
            print("📊 CLOUD DASHBOARD VISUALIZATION")
            print("-" * 40)
            print("| Time     | Distance | Status           |")
            print("|----------|----------|------------------|")

            recent = self.alerts[-3:] if self.alerts else []
            for alert in recent[-3:]:
                status = "🚨 ALERT" if alert['status'] == "ALERT" else "✅ CLEAR"
                print(f"| {alert['timestamp'][11:16]} | {alert['distance']:>5}cm | {status:<16} |")

            if not recent:
                print("| No recent alerts                               |")
            print("-" * 40)

def main():
    node = SecurityNode("SEC-NODE-001")
    node.simulate_telemetry(duration=15)

if __name__ == "__main__":
    main()