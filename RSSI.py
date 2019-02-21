#!/usr/bin/env python
import selenium, time
import signal
import sys
# import rospy
# from std_msgs.msg import Int32MultiArray, String
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np

from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from pandas import *
import pandas

import matplotlib.pyplot as plt
import time

def sigint_handler(signal,frame):
	global RSSI_vals
	np.save('RSSI_vals.npy',np.array(RSSI_vals))
	sys.exit(0)

signal.signal(signal.SIGINT,sigint_handler)

webbrowser=webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
webbrowser.maximize_window()

#try catch if not connected
webbrowser.get("https://192.168.1.1/login.asp")

email_field=webbrowser.find_element_by_id("login-username")
email_field.clear()
email_field.send_keys("martian_comm")
time.sleep(1)
 
password_field=webbrowser.find_element_by_id("password")
password_field.clear()
password_field.send_keys("PoE9316"+Keys.ENTER)
time.sleep(1)

# data_pub=rospy.Publisher("RSSI_data",Int32MultiArray,queue_size=10)
# msg_pub=rospy.Publisher("RSSI_msg",String,queue_size=10)
# rospy.init_node("RSSI", anonymous=True)

#*****Forecasting Code*****

def check_RSSI(history):
	data = history.values
	data = [x for x in data]
	yhat_values = np.array([])
	for i in range(0,3):
		model = ARIMA(data, order=(5,2,0))
		model_fit = model.fit(disp=0)
		output = model_fit.forecast()
		yhat = output[0]
		data.append(yhat)
		print("Predicted Yhat = " + str(yhat))

		yhat_values = np.append(yhat_values, yhat)
		if(yhat < 14):
			print("Stop!")
			# RSSI_msg.publish("Stop")

	# predicted_yhat = yhat_values[2]*0.5+yhat_values[1]*0.3+yhat_values[0]*0.2
	# print("Predicted weighted yhat = " + str(predicted_yhat))
	return yhat_values


RSSI_vals=np.array([])
smooth_RSSI = np.array([])
history = pandas.DataFrame(columns=['RSSI'])
predictions = np.array([])
RSSI_data = np.zeros(2)

##PLotting code
xdata = []
ydata = []
xdata2 = []
ydata2 = []
plt.show()
axes = plt.gca()
axes.set_xlim(0, 150)
axes.set_ylim(0, 80)
axes.set(xlabel='time', ylabel='RSSI', title='Prediction plot')
line, = axes.plot(xdata, ydata, linewidth=2, color='g')
line2, = axes.plot(xdata2, ydata2, '--', linewidth=2, color='b')

##
x = np.arange(0,151,1)
axes.hlines(y=13, xmin=0, xmax=151, linewidth=3, color='r')
axes.fill_between(x, 0, 13, facecolor='tan')

past_value_1 = 0
past_value_2 = 0
past_value_3 = 0

while True:
	iframe = webbrowser.find_element_by_id("mainframe")
	webbrowser.switch_to.frame(iframe)
	elem = webbrowser.find_element_by_xpath('//tbody[@class="striped"]/tr/td[5]')
	value=int(elem.text)
	
	if(not((past_value_1 == past_value_2) and (past_value_2 == past_value_3) and (past_value_3 == value))):
		RSSI_vals = np.append(RSSI_vals,value)
	else:
		webbrowser.refresh()
		time.sleep(2)
		continue

	past_value_1 = past_value_2
	past_value_2 = past_value_3
	past_value_3 = value
	
	if(len(RSSI_vals)<=5):
		smooth_RSSI = np.append(smooth_RSSI, np.mean(RSSI_vals))
	else:
		new_val = (smooth_RSSI[-1]*5 - RSSI_vals[-6] + RSSI_vals[-1])/5
		smooth_RSSI = np.append(smooth_RSSI, new_val)

	# print(history)
	# for t in range(len(test)):
	# model = ARIMA(history, order=(5,2,0))
	# model_fit = model.fit(disp=0)
	# output = model_fit.forecast()
	# yhat = output[0]
	# predictions.append(yhat)
	# obs = smooth_RSSI[-1]

	xdata.append(len(RSSI_vals))
	ydata.append(RSSI_vals[-1])
	line.set_xdata(xdata)
	line.set_ydata(ydata)
	
	history = history.append({'RSSI':smooth_RSSI[-1]}, ignore_index = True)
	
	if (value < 20 and len(RSSI_vals) > 20):
		yhat_values = check_RSSI(history)
		RSSI_len = len(RSSI_vals)
		xdata2 = [RSSI_len+1, RSSI_len+2, RSSI_len+3]
		line2.set_xdata(xdata2)
		line2.set_ydata(yhat_values)

	plt.draw()
	plt.pause(1e-17)

	# RSSI_pub.publish(data=RSSI_data)
	webbrowser.refresh()
	time.sleep(2)