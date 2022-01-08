# Practica 13 - BORME
# María José Medina Hernández

# Imports
import sys
import requests
import time
import logging
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from os import makedirs
from os.path import exists

def format_date(date):
    """
    Formats "YYYYMMDD" date into "DD/MM/YYYY" date.
    
    Params
    -------
    date : string
        The date string "YYYYMMDD".

    Return
    -------
    f_date : string
        Formatted date "DD/MM/YYYY".
    """
    date = date.strip()
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    f_date = f"{day}/{month}/{year}"
    return f_date

def download_pdf(driver):
    """
    Dowloads the the PDF files.
    
    Params
    -------
    driver : selenium.webdriver.chrome.webdriver.WebDriver
        The web driver.
    """
    # Get all h4 titles after the second section title
    titles = driver.find_elements_by_xpath("//h3[contains(text(),\'SEGUNDA')]/following-sibling::h4")
    # Iterate through the titles
    for element in titles:
        # Get the directory name
        subdirectory = f"{directory}/{element.text}"
        # Create directory
        if not exists(subdirectory):
            makedirs(subdirectory)
        # Find the pdfs after the title
        pdfs = element.find_element_by_xpath("./following-sibling::ul").find_elements_by_xpath(".//li[@class = 'puntoPDF']/a")
        for pdf in pdfs:
    #         print(pdf.get_attribute('href'))
            URL = pdf.get_attribute('href')
            file_name = URL.split("/")[-1]
            logging.info(f"{subdirectory} ----- {URL}")
            # Using response in stead of clicking to control the directory the pdfs are downloaded into
            response = requests.get(URL)  
            with open(f"{subdirectory}/{file_name}", "wb") as output_file:
                output_file.write(response.content)
            time.sleep(2)
            
def spider(driver):
    """
    Retrieves all the XML links.
    Params
    -------
    driver : selenium.webdriver.chrome.webdriver.WebDriver
        The web driver.

    Return
    -------
    links : list
        Matrix with columns for directory folder and link.
    """
    links = []
    # Get all h4 titles after the second section title
    titles = driver.find_elements_by_xpath("//h3[contains(text(),\'SEGUNDA')]/following-sibling::h4")
    # Iterate through the titles
    for element in titles:
        # Get the directory name
        subdirectory = f"{directory}/{element.text}"
        # Create directory
        if not exists(subdirectory):
            makedirs(subdirectory)
        # Find the pdfs after the title
        other_formats = element.find_element_by_xpath("./following-sibling::ul").find_elements_by_xpath(".//li[@class = 'puntoHTML']/a")
        for other_format in other_formats:
            links.append([element.text, other_format.get_attribute("href")])
    return links

def download_xml(driver, links):
    """
    Dowloads the the xml file in each link.
    
    Params
    -------
    driver : selenium.webdriver.chrome.webdriver.WebDriver
        The web driver.
    links : list
        Matrix with columns for directory folder and link.

    """
    for link in links:
        subdirectory = f"{directory}/{link[0]}"
        url = link[1]
        driver.get(url)
        URL = driver.find_element_by_xpath(".//li[@class = 'puntoXML']/a").get_attribute('href')
        # Get file name from query string
        file_name = URL.split("=")[-1]
        logging.info(f"{subdirectory} ----- {URL}")
        # Using response in stead of clicking to control the directory the pdfs are downloaded into
        response = requests.get(URL)  
        with open(f"{subdirectory}/{file_name}.xml", "wb") as output_file:
            output_file.write(response.content)
        time.sleep(2)


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.info("info")

# Get desired date

if (len(sys.argv) == 2):
    boletin = sys.argv[1]
else:
    print ("Usage: python Practica13-BORME.py YYYYMMDD")
    print ("Example: python 20201201")
    exit (1)
    
# Create directory for the PDFs
directory = f"Boletin-{boletin}"
if not exists(directory):
    makedirs(directory)
    
date = format_date(boletin)
print(date)

# Deploy the Chrome diver executed by Selenium
chromedriver_path = r"..\chromedriver_win32\chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver_path)
url = "https://www.boe.es/diario_borme/"
driver.get(url)
time.sleep(2)

# Input the desired date in the calendar
# try:
#     driver.find_element_by_id("fechaBORME").send_keys(date)
#     divs = driver.find_element_by_name("acc").click()
# except:
#     logging.error(f"No existe boletín para la fecha {date}")

# print("YAZZZ")

driver.find_element_by_id("fechaBORME").send_keys(date)
acc = driver.find_element_by_name("acc").click()

try:
    # Move to second section
    id = driver.find_element_by_xpath("//h3[contains(text(),\'SEGUNDA')]").get_attribute("id")
    ActionChains(driver).move_to_element(driver.find_element_by_id(id)).perform()
    # Download the pdfs
    download_pdf(driver)
    # Download xmls
    links = spider(driver)
    download_xml(driver, links)
    driver.quit()
except:
    logging.error(f"No existe boletín para la fecha {date}")
    driver.quit()
    exit(1)
    

