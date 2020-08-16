from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
from datetime import date
import smtplib


PATH = "C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(PATH)
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)


driver.get("https://www.bazos.cz")
#driver.minimize_window()

lokalita = driver.find_element_by_name("hlokalita")
lokalita.send_keys("Plzen")
search = driver.find_element_by_name("hledat")
search.send_keys("Jawa 350")
search.send_keys(Keys.RETURN)

time.sleep(1)

datums = driver.find_elements_by_class_name("velikost10")
nazvy = driver.find_elements_by_class_name("nadpis")


arr = np.array(datums)
arrr = np.array(nazvy)


#i = len(arr)
#while i > 0:
#  	print(i)
#  	i -= 1
#  	print(arr[i].text + "   " + arrr[i].text)



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

		server.sendmail("novyinzeratnabazosi@gmail.com", "jindrichtomas@post.cz", msg)
		#print("mail odeslan")
		server.quit()
		print(driver.current_url)
		
		driver.close()
		driver.switch_to.window(driver.window_handles[0]),time.sleep(2)

		
		




	


