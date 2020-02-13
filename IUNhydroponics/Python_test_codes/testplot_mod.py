import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import datetime, os
from datetime import time


class Buttons():
	def __init__(self):
		w = tk.Tk(screenName = None, baseName = None, className = " Main Control Panel", useTk = 1)
		w.title("Control Panel")

		self.lab1 = tk.Label(w, text = "Close the program.", wraplength = "150")
		self.lab1.grid(row = 2, column = 2, padx = "10")
		self.lab2 = tk.Label(w, text = "Choose a file in which to graph temperature and humidity values.", wraplength = "150")
		self.lab2.grid(row = 2, column = 1, padx = "10")
		self.but1 = tk.Button(w, text = "Close Window", command = w.destroy)
		self.but1.grid(row = 1, column = 2, pady = "10", padx = "10")
		self.but2 = tk.Button(w, text = "New Graph", command = self.plot)
		self.but2.grid(row = 1, column = 1, padx = "10")

		w.mainloop()

	def xtickval(self, value):
		toUse = []
		for i in range(len(value)):
			if len(value) < 300:
				if (i % 10 == 0) == True:
					toUse.append(value[i])
			elif len(value) > 300:
				if (i % 50 == 0) == True:
					toUse.append(value[i])
		return toUse

	def plot(self):
		df =  pd.DataFrame(self.newfile())
		times = df.index

		hours = [datetime.time.isoformat(datetime.time(i, 0, 0, 0)) for i in range(24)]

		df.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], axis='columns', inplace=True)

		atemps = df['B']
		ahums = df['C']

		plt.figure()

		ax1 = plt.subplot(211)
		ax1.plot(times, atemps, color="green")
		#plt.xlim(min(hours), max(hours))
		#plt.ylim(min(allt), max(allt))
		plt.ylabel('Temperature (*C)')
		#plt.xticks(self.xtickval(times))
		#plt.xticks(hours)
		ax1.xaxis.set_major_locator(mdates.HourLocator(interval = 1))
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
		plt.setp(ax1.get_xticklabels(), rotation = -25, ha = "left")

		offset = -72
		bbox = dict(boxstyle="round", fc="0.8")
		arrowprops = dict(arrowstyle = "->", connectionstyle = "angle, angleA = 0, angleB = 90, rad = 10")

		ax1.annotate((
			"Maximum " + str(atemps.max()) + '*C at' + str(atemps.idxmax())),
			xy=(atemps.idxmax(), atemps.max()),
			xytext=(offset, 2.5*offset), textcoords='offset points',
			bbox=bbox, arrowprops = arrowprops)

		plt.grid(True)


		ax2 = plt.subplot(212)
		ax2.plot(times, ahums, color="purple")
		plt.xlim(min(times), max(times))
		#plt.ylim(min(allh), max(allh))
		plt.xlabel('Time between' + str(min(times)) + 'and' + str(max(times)))
		plt.ylabel('Humidity (%)')
		plt.xticks(self.xtickval(times))
		plt.setp(ax2.get_xticklabels(), rotation = -25, ha = "left")

		ax2.annotate((
			"Maximum " + str(ahums.max()) + '% at' + str(ahums.idxmax())),
			xy=(ahums.idxmax(), ahums.max()),
			xytext=(offset, 2.5*offset), textcoords='offset points',
			bbox = bbox, arrowprops = arrowprops)

		plt.grid(True)

		plt.suptitle("Temperature and Humidity for " + df.iloc[1]['A'])

		mng = plt.get_current_fig_manager()
		mng.resize(*mng.window.maxsize())
		plt.show()

	def newfile(self):
		file = pd.read_csv(filedialog.askopenfilename(
			initialdir = (os.environ['HOME'] + "/TempHum_Results"), 
				title = "Select file", 
				filetypes = [("Spreadsheets", "*.csv")]),
			sep=',', index_col=1)
		#file = pd.read_csv("/home/pi/TempHum_Results/2019-12-19_results.csv", sep=',', index_col=1)
		return file


Buttons()

