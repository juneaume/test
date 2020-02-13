import datetime
import time
import board
import adafruit_dht

dht1 = adafruit_dht.DHT22(board.D23)
dht2 = adafruit_dht.DHT22(board.D24)
dht3 = adafruit_dht.DHT22(board.D25)

file = open("/home/pi/results.csv", "w")

temp1 = dht1.temperature
hum1 = dht1.humidity
temp2 = dht2.temperature
hum2 = dht2.humidity
temp3 = dht3.temperature
hum3 = dht3.humidity
timestamp = datetime.datetime.now().strftime("%m/%d/%Y,%H:%M:%S")


avgt = (temp1 + temp2 + temp3) / 3
avgh = (hum1 + hum2 + hum3) / 3

while True:
	try:
		data1 = "{:.1f},{:.1f}  {:.1f},{:.1f}	{:.1f},{:.1f}	{:.1f},{:.1f}" .format(avgt, avgh, temp1, hum1, temp2, hum2, temp3, hum3)
		string = timestamp + "," + data1 + "\r\n"
		file.write(string)
		print(timestamp, "	Average: ", round(avgt, 2),"*C,", round(avgh, 2),"%,	Sensor 1:", temp1,"*C,", hum1,"%,	Sensor 2:", temp2,"*C,", hum2,"%,	Sensor 3:", temp3,"*C,", hum3,"%")
	except RuntimeError as error:
		print(error.args[0])

	time.sleep(10.0)
