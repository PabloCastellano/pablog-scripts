#!/usr/bin/env python3
# Obtiene el listado de últimos movimientos de una cuenta de FIARE
# sudo pip3 install selenium
# sudo apt install chromium-chromedriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import sys

USERNAME = input("Username (e.g. FI123456): ")
NIF = input("NIF (e.g. 00000014Z): ")
PASSWORD = getpass("Password (e.g. 1234): ")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = '/usr/bin/chromium-browser'

driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver', chrome_options=chrome_options)
driver.get("https://www.fiarebancaetica.coop/")
button = driver.find_element_by_class_name("client-button")
if button.is_displayed():
    button.click()
else:
    print("No button displayed")
    sys.exit(1)

actions = driver.find_element_by_id("actions")
button = actions.find_element_by_xpath("li/a")
assert(button.text.lower() == "castellano")

button.click()

tabs = driver.window_handles

driver.switch_to.window(driver.window_handles[1])

form = driver.find_element_by_id("form_acceso")
inputs = form.find_elements_by_xpath("form/fieldset/input")

user_field = inputs[0]
user_field.send_keys(USERNAME)
nif_field = inputs[1]
nif_field.send_keys(NIF)
password_field = inputs[2]
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.RETURN)

cuentas_button = driver.find_elements_by_class_name("fondoMenu")[1]
cuentas_button.click()

tabla = driver.find_element_by_id("PORTLET-INPUT").find_element_by_xpath("table")

for row in tabla.find_elements_by_xpath("tbody/tr"):
    print(row.text)

"""
(Pdb) tabla.screenshot_as_png
*** ValueError: No JSON object could be decoded
"""

#driver.get_screenshot_as_file("/tmp/asd.png")
driver.close()
