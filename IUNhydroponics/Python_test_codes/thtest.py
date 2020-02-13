import datetime
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import os.path

##Expert code brought to you by Brittany Armstrong

chan_list = [23,24,25,26]

GPIO.setwarnings(False)

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)

def destroy():
	GPIO.output(chan_list, GPIO.HIGH)
	GPIO.cleanup()

while True:
	setup()

	hum1, temp1 = Adafruit_DHT.read_retry(22, 23)
	hum2, temp2 = Adafruit_DHT.read_retry(22, 24)
	hum3, temp3 = Adafruit_DHT.read_retry(22, 25)

	hums = [hum1, hum2, hum3]
	temps = [temp1, temp2, temp3]

	def avg(nums):
		values = nums
		for i in range(values.count(None)): values.remove(None)
		toUse = []
		avg = sum(values)/len(values)
		for x in range(len(values)):
			if not (values[x] < 0.9 * avg) or (values[x] > 1.1 * avg):
				toUse.append(values[x])
		return sum(toUse)/len(toUse)

	GPIO.output(chan_list, GPIO.LOW)
	time.sleep(31.0)
	try:
		for x in range(len(temps)):
			if temps[x] == None: temps[x] = 0
		for i in range(len(hums)):
			if hums[i] == None: hums[i] = 0

		data1 = "{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}" .format(
			avg(temps), avg(hums), temps[0], hums[0], temps[1], hums[1], temps[2], hums[2])

		timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		date = datetime.datetime.now().strftime("%Y-%m-%d")

		string = timestamp + " , " + data1 + "\r\n"

		if os.path.isfile("/home/pi/" + date + "_results.csv") == False:
			file = open("/home/pi/" + date + "_results.csv", "a")
			file.write("Date, Time, AvgTemp, AvgHum, S1Temp, S1Hum, S2Temp, S2Hum, S3Temp, S3Hum \n")
			file.write(string)
		else:
			file = open("/home/pi/" + date + "_results.csv", "a")
			file.write(string)


		print(timestamp + "\t Average: {:.2f}*C, {:.2f}% \t Sensor 1: {:.2f}*C, {:.2f}% \t Sensor 2: {:.2f}*C, {:.2f}% \t Sensor 3: {:.2f}*C, {:.2f}%" .format(
			avg(temps), avg(hums), temps[0], hums[0], temps[1], hums[1], temps[2], hums[2]))
	except RuntimeError as error:
		print(error.args[0])
		destroy()

	GPIO.output(chan_list, GPIO.HIGH)

	file.close()
	time.sleep(29.0)

