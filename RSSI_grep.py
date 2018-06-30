import selenium, time
import signal
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def sigint_handler(signal,frame):
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



while True:
	iframe = webbrowser.find_element_by_id("mainframe")
	webbrowser.switch_to.frame(iframe)
	elem = webbrowser.find_element_by_xpath('//tbody[@class="striped"]/tr/td[5]')
	print elem.text
	webbrowser.refresh()
	time.sleep(1)
	





