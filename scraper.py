from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
from datetime import date
import smtplib
import tkinter as tk

root = tk.Tk()
def hledej(mesto, hledej,email):
	
	close_window()

	PATH = "C:\Program Files (x86)\chromedriver.exe"
	options = webdriver.ChromeOptions()
	#options.add_argument("headless")
	driver = webdriver.Chrome(PATH, options=options)

	driver.get("https://www.bazos.cz")

	lokalita = driver.find_element_by_name("hlokalita")
	lokalita.send_keys(mesto)
	search = driver.find_element_by_name("hledat")
	search.send_keys(hledej)
	search.send_keys(Keys.RETURN)

	time.sleep(1)

	datums = driver.find_elements_by_class_name("velikost10")
	nazvy = driver.find_elements_by_class_name("nadpis")

	arr = np.array(datums)
	arrr = np.array(nazvy)

	i = len(arr)
	while i > 0:
  		print(i)
  		i -= 1
  		print(arr[i].text + "   " + arrr[i].text)

	today = str(date.today())
	dnes = today[8:11]
	char1 = '['
	char2 = '.'
	for y in range(20):
		mystr = arr[y].text
		finstr = (mystr[mystr.find(char1)+1 : mystr.find(char2)])
		link = driver.find_element_by_link_text(arrr[y].text)

		if finstr == dnes:
			link.send_keys(Keys.CONTROL + Keys.RETURN)
			print("click")
			driver.switch_to.window(driver.window_handles[1]),time.sleep(2)

			server = smtplib.SMTP("smtp.gmail.com",587)
			server.ehlo()
			server.starttls()
			server.ehlo()

			server.login("novyinzeratnabazosi@gmail.com", "hlkqqhxzimvmchep")

			subject = "Novy inzerat na bazosi!"

			body = "Pro zobrazeni kliknete na nasledujici odkaz: " + driver.current_url

			msg = f"Subject: {subject}\n\n{body}"

			server.sendmail("novyinzeratnabazosi@gmail.com", email, msg)
			#print("mail odeslan")
			server.quit()
			print(driver.current_url)
		
			driver.close()
			driver.switch_to.window(driver.window_handles[0]),time.sleep(2)

	driver.close()

def okno():

	root.geometry("320x120")
	root.resizable(False,False)
	L1 = tk.Label(root, text="Zadejte lokalitu: ")
	L1.place(x = 1, y = 1)
	L2 = tk.Label(root, text="Zadejte produkt: ")
	L2.place(x = 1, y = 45)
	E1 = tk.Entry(root, bd=5)
	E1.place(x = 100, y = 1)
	E2 = tk.Entry(root, bd=5)
	E2.place(x = 100, y =45)
	L3 = tk.Label(root, text="Zadejte email: ")
	L3.place(x = 1, y = 90)
	E3 = tk.Entry(root, bd=5)
	E3.place(x = 100, y =90)
	Button=tk.Button(root,text = "HLEDEJ",height = 7, width = 11,state = "normal",command = lambda:hledej(E1.get(),E2.get(),E3.get()))
	Button.place(x = 230, y = 1)

	root.mainloop()		
	#hledej(lokalita, item)

def close_window():
	root.destroy()

okno()