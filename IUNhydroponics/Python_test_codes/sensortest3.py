import datetime
import time
import RPi.GPIO as GPIO
import Adafruit_DHT

chan_list = [23,24,25]
file = open("/home/pi/results.csv", "a")

def setup():
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)



def avg(values):
        nonZeroValues = []
        for i in range(len(values)):
                if values[i] > 0:
                        nonZeroValues.append(values[i])
        toUse = []
        avg = sum(nonZeroValues)/len(nonZeroValues)
        for x in range(len(nonZeroValues)):
                if not (nonZeroValues[x] < 0.9 * avg) or (nonZeroValues[x] > 1.1 * avg):
                        toUse.append(nonZeroValues[x])
        return round((sum(toUse)/len(toUse)), 2)

while True:
        hums = []
        temps = []
        setup()
	hum1, temp1 = Adafruit_DHT.read(22, 23)
	hum2, temp2 = Adafruit_DHT.read(22, 24)
	hum3, temp3 = Adafruit_DHT.read(22, 25)

        if type(hum1) == float:
                hums.append(round(hum1,2))
        else: hums.append(0.00)
        if type(hum2) == float:
                hums.append(round(hum2,2))
        else: hums.append(0.00)
        if type(hum3) == float:
                hums.append(round(hum3,2))
        else: hums.append(0.00)
        if type(temp1) == float:
                temps.append(round(temp1,2))
        else: temps.append(0.00)
        if type(temp2) == float:
                temps.append(round(temp2,2))
        else: temps.append(0.00)
        if type(temp3) == float:
                temps.append(round(temp3,2))
        else: temps.append(0.00)

        GPIO.output(chan_list, GPIO.LOW)
	time.sleep(5.0)

        try:
                data1 = "{:.2f},{:.2f} \t {:.1f},{:.1f} \t {:.1f},{:.1f} \t {:.1f},{:.1f}".format(avg(temps), avg(hums), temps[0], hums[0], temps[1], hums[1], temps[2], hums[2])
                timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                string = timestamp + "\t" + data1 + "\r\n"
                file.write(string)
                print(timestamp + "\t Average: {:.2f}*C, {:.2f}% \t Sensor 1: {:.2f}*C, {:.2f}% \t Sensor 2: {:.2f}*C, {:.2f}% \t Sensor 3: {:.2f}*C,{:.2f}%" .format(
                        avg(temps), avg(hums), temps[0], hums[0], temps[1], hums[1], temps[2], hums[2]))

	except RuntimeError as error:
		print(error.args[0])
        
	GPIO.output(chan_list, GPIO.HIGH)
	time.sleep(10.0)
