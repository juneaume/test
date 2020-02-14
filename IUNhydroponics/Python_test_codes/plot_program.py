import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import datetime, os
from tkinter import *

class Buttons():
	def __init__(self):
		w = tk.Tk(screenName = None, baseName = None, className = "Control Panel", useTk = 1)
		w.title("Main Menu")

		def opentl():
			w2 = tk.Toplevel()
			w2.title("Select Time Period")

			frame1 = Frame(w2)
			frame1.pack()
			self.v = tk.IntVar()
			rbyes = Radiobutton(frame1, text = "Yesterday", variable = self.v, value = '1', command = self.v.set("1"))
			rbyes.grid(row = 1, column = 1)

			rblw = Radiobutton(frame1, text = "Last week", variable = self.v, value = '2', command = self.v.set("2"))
			rblw.grid(row = 1, column = 2)

			rblm = Radiobutton(frame1, text = "Last month", variable = self.v, value = '3', command = self.v.set("3"))
			rblm.grid(row = 1, column = 3)

			frame2 = Frame(w2)
			frame2.pack()

			self.but5 = tk.Button(frame2, text = "Graph", command = self.processRb)
			self.but5.grid(row = 1, column = 2, padx = "10")

			self.but6 = tk.Button(frame2, text = "Close", command = w2.withdraw)
			self.but6.grid(row = 1, column = 3, padx = "10")

			w2.mainloop()



		self.but1 = tk.Button(w, text = "New Graph", command = self.plot)
		self.but1.grid(row = 1, column = 1, padx = "10")
		self.lab1 = tk.Label(w, text = "Choose one data set. Opens a file dialog box.", wraplength = "150")
		self.lab1.grid(row = 2, column = 1, padx = "10")

		self.but2 = tk.Button(w, text = "Previous Trends", command = opentl)
		self.but2.grid(row = 1, column = 2, padx = "10")
		self.lab2 = tk.Label(w, text = "See trends, ending with yesterday's full data set.", wraplength = "150")
		self.lab2.grid(row = 2, column = 2, padx = "10")

		self.but3 = tk.Button(w, text = "Live Graph", command = self.live)
		self.but3.grid(row = 1, column = 3, padx = "10")
		self.lab3 = tk.Label(w, text = "Graphs today's data as it is recorded.", wraplength = "150")
		self.lab3.grid(row = 2, column = 3, padx = "10")

		self.but4 = tk.Button(w, text = "Close Window", command = w.destroy)
		self.but4.grid(row = 1, column = 4, pady = "10", padx = "10")
		self.lab4 = tk.Label(w, text = "Close the program. Note - this will close all loaded graphs.", wraplength = "150")
		self.lab4.grid(row = 2, column = 4, padx = "10")

		w.mainloop()

	def xtickval(self, value):
		toUse = []
		for i in range(len(value)):
			if len(value) <= 25:
				toUse.append(value[i])
			elif len(value) > 25 and len(value) < 300:
				if (i % 8 == 0) == True:
					toUse.append(value[i])
			elif len(value) >= 300:
				if (i % 50 == 0) == True:
					toUse.append(value[i])

		return toUse

	def plot(self):
		df = pd.DataFrame(self.newfile())
		times = df.index
		df.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], axis='columns', inplace=True)
		atemps = df['B']
		ahums = df['C']

		plt.figure()
		ax1 = plt.subplot(211)
		ax1.plot(times, atemps, color = "black", label = "Average", linewidth = 3.0)
		ax1.plot(times, df['D'], color = "green", label = "Sensor 1")
		ax1.plot(times, df['F'], color = "blue", label = "Sensor 2")
		ax1.plot(times, df['H'], color = "purple", label = "Sensor 3")
		plt.xlim(min(times), max(times))
		plt.ylabel('Temperature (*C)')
		plt.xticks(self.xtickval(times))
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
		plt.legend(bbox_to_anchor = (1.001, 1), loc = 'upper left', borderaxespad = 0)

		ax2 = plt.subplot(212)
		ax2.plot(times, ahums, color = "black", label = "Average", linewidth = 3.0)
		ax2.plot(times, df['E'], color = "green", label = "Sensor 1")
		ax2.plot(times, df['G'], color = "blue", label = "Sensor 2")
		ax2.plot(times, df['I'], color = "purple", label = "Sensor 3")
		plt.xlim(min(times), max(times))
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
		plt.legend(bbox_to_anchor = (1.001, 1), loc = 'upper left', borderaxespad = 0)
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
		return file

	def prev(self, val):
		from datetime import timedelta

		atemps = []
		ahums = []
		times = []

		date = datetime.date.today()
		length = []
		delta = timedelta(days = 1)

		for i in range(val):
			date = date - delta
			length.append(date)

		if val > 1:
			for j in range(len(length)):
				fdate = length[j].strftime("%Y-%m-%d")
				df = pd.DataFrame(pd.read_csv((os.environ['HOME'] + "/TempHum_Results/" + fdate + "_results.csv"), sep=',', index_col=1))
				df.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], axis='columns', inplace=True)

				time = df.index
				counttime = len(time)
				divtime = counttime // 8
				tt = 0

				fdate2 = length[j].strftime("%d %b")
				times.append(time[tt] + ", " + fdate2)
				atemps.append(df.iloc[tt]['B'])
				ahums.append(df.iloc[tt]['C'])

				for k in range(7):
					tt += divtime
					times.append(time[tt] + ", " + fdate2)
					atemps.append(df.iloc[tt]['B'])
					ahums.append(df.iloc[tt]['C'])

			times.reverse()

		else:
			fdate = length[0].strftime("%Y-%m-%d")
			df = pd.DataFrame(pd.read_csv((os.environ['HOME'] + "/TempHum_Results/" + fdate + "_results.csv"), sep=',', index_col=1))
			df.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], axis='columns', inplace=True)

			time = df.index

			for m in range(len(time)):
				times.append(time[m])
				atemps.append(df.iloc[m]['B'])
				ahums.append(df.iloc[m]['C'])


		plt.figure()
		ax1 = plt.subplot(211)
		ax1.plot(times, atemps, color = "black", label = "Average", linewidth = 3.0)
		plt.ylabel('Temperature (*C)')
		plt.xticks(self.xtickval(times))
		plt.setp(ax1.get_xticklabels(), rotation = -25, ha = "left")
		plt.grid(True)


		ax2 = plt.subplot(212)
		ax2.plot(times, ahums, color = "black", label = "Average", linewidth = 3.0)
		plt.ylabel('Humidity (%)')
		plt.xticks(self.xtickval(times))
		plt.setp(ax2.get_xticklabels(), rotation = -25, ha = "left")
		plt.grid(True)

		if val > 1:
			val -= 1
			plt.suptitle("Temperature and Humidity for " + str(length[val]) + " through " + str(length[0]))

		else:
			plt.suptitle("Temperature and Humidity for " + df.iloc[1]['A'])

		mng = plt.get_current_fig_manager()
		mng.resize(*mng.window.maxsize())

		plt.show()

	def processRb(self):
		if self.v.get() == 1:
			self.prev(1)
		elif self.v.get() == 2:
			self.prev(7)
		elif self.v.get() == 3:
			self.prev(30)


	def live(self):
		import matplotlib.animation as animation

		fig, ax1 = plt.subplots(facecolor='grey')
		ax1.set_facecolor('grey')

		def animate(i):
			date = datetime.datetime.now().strftime("%Y-%m-%d")
			file = os.environ['HOME'] + "/TempHum_Results/" + date + "_results.csv"

			#file = self.newfile()

			df = pd.DataFrame(pd.read_csv(file, sep=',', index_col=1))
			df.set_axis(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], axis = 'columns', inplace = True)

			xar = df.index
			y1ar = df['B']
			y2ar = df['C']

			ax1.clear()
			ax1.plot(xar, y1ar, label = "Average Temperature (*C)")
			ax1.plot(xar, y2ar, label = "Average Humidity (%)")
			plt.xticks(self.xtickval(xar))
			plt.suptitle("Temperature and Humidity for " + df.iloc[1]['A'] + ". \n Please note that live functionality can only continue within the listed day.")
			plt.grid(True)
			plt.legend(loc = 'upper left', borderaxespad = 0)
			plt.setp(ax1.get_xticklabels(), rotation = -25, ha = "left")


		ani = animation.FuncAnimation(fig, animate, interval = 1000)

		mng = plt.get_current_fig_manager()
		mng.resize(*mng.window.maxsize())

		plt.show()


Buttons()
