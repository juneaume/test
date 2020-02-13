import RPi.GPIO as GPIO
import time
LedPin = 26

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LedPin, GPIO.OUT, initial=GPIO.HIGH)

def main():
	while True:
		GPIO.output(LedPin, GPIO.LOW)
		time.sleep(1.5)
		GPIO.output(LedPin, GPIO.HIGH)
		time.sleep(0.5)

def destroy():
	GPIO.output(LedPin, GPIO.HIGH)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()
