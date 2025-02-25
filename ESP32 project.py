import network
import urequests
import utime
from machine import Pin, ADC, I2C
from dht import DHT11


SSID = "Delapanbelas-2nd"
PASSWORD = "senyumduludong"


GOOGLE_SHEET_URL = "https://script.google.com/macros/s/YOUR_GOOGLE_SCRIPT_URL/exec"


UBIDOTS_TOKEN =
UBIDOTS_MQTT_BROKER = 
UBIDOTS_DEVICE_LABEL = 


MONGO_API_URL = 

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)
while not station.isconnected():
    pass
print("WiFi connected")


sensor = DHT11(Pin(4))
led_red = Pin(2, Pin.OUT)
led_yellow = Pin(13, Pin.OUT)
buzzer = Pin(15, Pin.OUT)
pir = Pin(5, Pin.IN)

def send_to_google_sheets(temp, hum):
    try:
        urequests.get(f"{GOOGLE_SHEET_URL}?temperature={temp}&humidity={hum}")
    except Exception as e:
        print("Error sending to Google Sheets:", e)

# Fungsi untuk mengirim data ke Ubidots
def send_to_ubidots(temp, hum):
    payload = {"temperature": temp, "humidity": hum}
    topic = f"/v1.6/devices/{UBIDOTS_DEVICE_LABEL}"
    client.publish(topic, str(payload))

while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    print(f"Temp: {temperature}C, Hum: {humidity}%")
    
    if utime.time() % (8 * 3600) == 0:
        send_to_google_sheets(temperature, humidity)
        send_to_ubidots(temperature, humidity)
       
    if temperature > 5:
        for _ in range(5):
            led_red.value(1)
            buzzer.value(1)
            utime.sleep(0.5)
            led_red.value(0)
            buzzer.value(0)
            utime.sleep(0.5)
    
    current_hour = utime.localtime()[3]
    if 20 <= current_hour or current_hour < 06:
        if pir.value():
            led_yellow.value(1)
            buzzer.value(1)
            utime.sleep(2)
            led_yellow.value(0)
            buzzer.value(0)
            send_to_google_sheets("Motion Detected", "")
    
    utime.sleep(1)
