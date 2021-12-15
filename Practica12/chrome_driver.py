import time
from selenium import webdriver

# Deploy the Chrome diver executed by Selenium
chromedriver_path = r"..\chromedriver_win32\chromedriver"

# Path to the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path)
url = "https://comparador.cnmc.gob.es/"
driver.get(url)

time.sleep(2)
# Click reject cookies button
driver.find_element_by_class_name("cookiesjsr-btn").click()
time.sleep(2)
# Click type of utility select button
driver.find_element_by_id("input-36").click()
time.sleep(2)
# Click on the electricity select item
driver.find_element_by_class_name("v-list-item__content").click()
time.sleep(2)
# Send the form
driver.find_element_by_id("Iniciar").click()
time.sleep(2)
# Input the postal code
postal_code = "28045"
driver.find_element_by_name("codigoPostal").send_keys(postal_code)
time.sleep(2)
# Send the form
driver.find_element_by_id("Continuar").click()
time.sleep(2)

divs = driver.find_elements_by_class_name("InfoFormulario")
print(divs)
# spans = div.find_elements_by_tag_name("span")

for x in range(len(spans)):
    print(spans[x].text)

time.sleep(60)

driver.close()



def store_to_csv(matrix, file_path):
    sleep(2)

