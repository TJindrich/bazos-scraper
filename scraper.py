from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import datetime
import smtplib
import tkinter as tk

root = tk.Tk()
PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
#options.add_argument("headless")
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(10)

odkazy =[]


def ulozLinky(email):
	datums = driver.find_elements_by_class_name("velikost10")
	nazvy = driver.find_elements_by_class_name("nadpis")

	arr = np.array(datums)
	arrr = np.array(nazvy)
	
	arrDatumy = []

	i = len(arr)
	while i > 0:
  		print("inzerat číslo: "+str(i))
  		i -= 1
  		print(arr[i].text + "   " + arrr[i].text)

	char1 = '['
	char2 = ']'
	for y in range(len(arr)):

		mystr = arr[y].text
		finstr = (mystr[mystr.find(char1)+1 : mystr.find(char2)])
		arrDatumy.append(finstr)
		print("Datumy inzerátl: "+finstr)

	x = datetime.datetime.now()
	den = str(x.day)
	mesic = str(x.month)
	rok = str(x.year)

	datum = den+ "."+mesic+ ". "+rok
	print("dnešní datum: "+datum)
	i = 0
	a = 0
	for x in arrDatumy :

		link = driver.find_element_by_link_text(arrr[i].text)
		i=i+1

		if x == datum :
			a = a+1
			link.send_keys(Keys.CONTROL + Keys.RETURN)
			print("click")
			driver.switch_to.window(driver.window_handles[1])
			time.sleep(0.3)

			
			odkazy.append(driver.current_url)
			print("seznam odkazů: "+str(odkazy))
			print("Aktuální stránka: "+driver.current_url)
		
			driver.close()
			driver.switch_to.window(driver.window_handles[0])
			time.sleep(0.3)
	if a == 20 :
		dalsi = driver.find_element_by_link_text("Další")
		dalsi.click()
		time.sleep(0.3)
		ulozLinky(email)
	else :
		sendMail(email,str(odkazy))
		driver.quit()
	

def sendMail(prijemce,odkazy):
	server = smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login("novyinzeratnabazosi@gmail.com", "hlkqqhxzimvmchep")
	subject = "Novy inzerat na bazosi!"
	body = "Dnesni nabidky na vami specifikovany produkt: " + odkazy
	msg = f"Subject: {subject}\n\n{body}"
	server.sendmail("novyinzeratnabazosi@gmail.com", prijemce, msg)
	print("mail odeslan")
	server.quit()
	print("end")

def hledej(mesto, hledej, email):
	
	close_window()
	
	
	
	try:
		driver.get("https://www.bazos.cz")
		lokalita = driver.find_element_by_name("hlokalita")
	except Exception :
		print("Web nebo prvek nenalezen!\n")

	lokalita.send_keys(mesto)
	search = driver.find_element_by_name("hledat")
	search.send_keys(hledej)
	search.send_keys(Keys.RETURN)

	time.sleep(1)

	ulozLinky(email)

	
	
		
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
	kde = E1.get()
	co = E2.get()
	mejl = E3.get()
	hledasKde = kde
	hledasCo = co
	emailAdresa = mejl

	root.mainloop()		

def close_window():
	root.destroy()

okno()


