# PRÁCTICA 7 - Beautifulsoup
# María José Medina Hernández

# Imports
import logging
import csv
import json
import requests
from bs4 import BeautifulSoup

def print_json(dic, file_path):
    with open(file_path, "w") as output_file:
        json.dump(dic, output_file)
        
def load_csv(file_path):
    with open(file_path, "r") as input_file:
        reader = csv.reader(input_file, delimiter = ";")
        matrix = [row for row in reader]
    return matrix

def print_json(dic, file_path):
    with open(file_path, "w") as output_file:
        json.dump(dic, output_file)
        
def find_university_data(soup, university, url):
    """
    Finds the data of the universitie from the url provided.
    
    Params
    -------
    soup : BeautifulSoup.soup
    
    university: string
        name of the university
    
    url: string
        url to the wikipedia page of the university

    Return
    -------
    data : dic
        The dictionary with the data of the universities.
    """
    # Find the info card
    # We search by class = "infobox vcard"
    target_tables = soup.find_all("table", class_="infobox vcard")

    aux = {}
    try:
        target_table = target_tables[0]
        tds = target_table.find_all("td")

        # Data extraction
        for element in target_table.descendants:
            try:
                text = element.get_text()
                # Delete parenthesis and annotations
#                 text = re.sub(r"\([^()]*\)", "", text)

                if "motto" in text.lower():
                    if "english" in text.lower():
                        aux["motto english"] = element.nextSibling.get_text()
                    elif "latin" in text.lower():
                        aux["motto latin"] = element.nextSibling.get_text()
                    else:
                        aux["motto"] = element.nextSibling.get_text()

                elif "type" in text.lower():
                    aux["type"] = element.nextSibling.get_text()

                elif "established" in text.lower():
                    aux["established"] = element.nextSibling.get_text()

                elif "chancellor" in text.lower():
                    aux["chancellor"] = element.nextSibling.get_text()

                elif "vice-chancellor" in text.lower():
                    aux["chancellor"] = element.nextSibling.get_text()

                elif "rector" in text.lower():
                    aux["rector"] = element.nextSibling.get_text()

                elif "students" in text.lower():
                    aux["students"] = element.nextSibling.get_text()

                elif "location" in text.lower():
                    aux["location"] = element.nextSibling.get_text()

                elif "campus" in text.lower():
                    aux["campus"] = element.nextSibling.get_text()

                elif "colors" in text.lower():
                    aux["colors"] = element.nextSibling.get_text()

                elif "affiliations" in text.lower():
                    aux["affiliations"] = element.nextSibling.get_text()

                elif "website" in text.lower():
                    aux["website"] = element.nextSibling.find("a")["href"]

                aux["logo"] = target_table.find("img")["src"]
            except:
                pass
    except:
        logging.warning(f"Cannot retrieve data from {university} at {url}")
    
    return aux

def find_all_data(country_matrix):
    """
    Finds the data of all the universities of all the countries from the links provided.
    
    Params
    -------
    country_matrix : list
        Matrix containing the following columns:
            country
            link: link to a list of all the universities of the country

    Return
    -------
    data : dic
        The dictionary with the data of all the universities.
    """

    # Dict to store the data of the universities
    data = {}
    for row in country_matrix:
        # Download the HTML
        university = row[2].strip()
        relative_url = row[3]
        url = f"https://en.wikipedia.org/{relative_url}"

        response = requests.get(url)
        logging.debug(f"Accessing {university} at {url}")

        # Parse the HTML
        soup = BeautifulSoup(response.content, "html.parser")

        aux = find_university_data(soup, university, url)

        data[university] = aux
    return data

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.info("info")

# Get the URLs
country_matrix = load_csv("universities.csv")
    
data = find_all_data(country_matrix)
print_json(data, r"universities.json")
