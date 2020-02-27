import datetime
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import os.path


##Expert code brought to you by Brittany Armstrong with assistance from Nicholas Bibeau



## These are the GPIO pins that are being read; they're stored this way so they can all be toggled on/off simultaneously
chan_list = [23,24,25,26]

## This is so the terminal doesn't spit out an error if the code starts while the sensors are already on; it still reads
GPIO.setwarnings(False)

## Sets code to read GPIO as numbers and turns off devices when the program starts
def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.HIGH)

## When the program is quit, this will turn off the sensors and make sure no extraneous files are left behind
def destroy():
	GPIO.output(chan_list, GPIO.HIGH)
	GPIO.cleanup()

## The whole program is on a loop
while True:
	setup()

	## Pulling sensor values. 22 references the sensor, DHT22, while the second value is the pin number
	hum1, temp1 = Adafruit_DHT.read_retry(22, 23)
	hum2, temp2 = Adafruit_DHT.read_retry(22, 24)
	hum3, temp3 = Adafruit_DHT.read_retry(22, 25)

	## Storing humidity values and temperature values together
	hums = [hum1, hum2, hum3]
	temps = [temp1, temp2, temp3]


	## Takes an average of provided values
	def avg(nums):
		## Reading through the provided list and looking at each value
		for i in range(nums.count(None)):
			## Removing any values that are 0
			nums.remove(None)

		toUse = []
		## Taking a temporary average of non-zero numbers
		avg = sum(nums)/len(nums)

		## Looking at non-zero numbers for values that are over 5% different from the average and removing them
		for x in range(len(nums)):
			if not (nums[x] < 0.95 * avg) or (nums[x] > 1.05 * avg):
				## Adding values that are within 5% of average to the list for final average 
				toUse.append(nums[x])
		## Computing a new average and returning the value
		return sum(toUse)/len(toUse)


	## Turning on the sensors
	GPIO.output(chan_list, GPIO.LOW)

	## Giving the sensors 31 seconds for readings; if the sensors are unsuccessful in reading, they will read up to 14 more times.
	## Readings take 2 seconds apiece. 1 extra second was given just in case there are any miniscule time lags.
	time.sleep(31.0)

	## After the 31 seconds has elapsed
	try:

		## Checking temperature list for empty values and assigning a value of 0; this gets removed for averages
		for x in range(len(temps)):
			if temps[x] == None: temps[x] = 0
		## Checking humidity list for empty values and assigning a value of 0; this gets removed for averages
		for i in range(len(hums)):
			if hums[i] == None: hums[i] = 0

		## formatting all temperature & humidity values to 2 decimals - this will be written to our log
		data1 = "{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}" .format(
			avg(temps), avg(hums), temps[0], hums[0], temps[1], hums[1], temps[2], hums[2])

		## global means this variable is usable outside of the "try" loop if needed
		global timestamp
		timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		date = datetime.datetime.now().strftime("%Y-%m-%d")

		## Creates a line with the date, time, all humidity & temperature values, then creates a new line
		string = timestamp + " , " + data1 + "\r\n"

		## Checks to see if a log already exists for the current day. if it doesn't, it creates the log
		if os.path.isfile("/home/pi/TempHum_Results/" + date + "_results.csv") == False:
			## Creating & opening the new file. "a" means append so it doesn't write over any values
			file = open("/home/pi/TempHum_Results/" + date + "_results.csv", "a")
			## Creates column headers for the first row
			file.write("Date,Time,AvgTemp,AvgHum,S1Temp,S1Hum,S2Temp,S2Hum,S3Temp,S3Hum\n")
			## Writes the data to the log
			file.write(string)

		## If the log already exists
		else:
			## Opens the existing log
			file = open("/home/pi/TempHum_Results/" + date + "_results.csv", "a")
			## Writes the data to the log
			file.write(string)

	## If our try loop didn't run for some reason, this will print the reason and run the destroy function
	except RuntimeError as error:
		print(error.args[0])
		destroy()

	## Turns the sensors back off until next time
	GPIO.output(chan_list, GPIO.HIGH)

	## Closes the log file to free up computer memory
	file.close()

	## Time until the loop repeats, in seconds. Currently set to the difference of 5 minutes minus the previous 31 second sensor reading
	time.sleep(279.0)


