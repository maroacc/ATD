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

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.info("info")

# Get the URLs
country_matrix = load_csv("universities.csv")

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

    # Find the info card
    # We search by class = "infobox vcard"
    target_tables = soup.find_all("table", class_="infobox vcard")

    # Check that there's only one element belonging to the class
    len(target_tables)

    # Get the element belonging to the class that we are aiming for
    # (There's only one in this case)
#     target_table = target_tables[0].find("tbody")
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
        
    data[university] = aux
    
print_json(data, r"universities.json")
#     data = { "seal" : target_table.find("a").find("img")["src"],
#              "motto_latin" : target_table.find_all("i")[0].get_text(),
#              "motto_english" : target_table.find_all("i")[2].get_text(),
#              "motto_spanish" : target_table.find_all("i")[1].get_text(),
#              "type" : tds[2].get_text(),
#              "established" : tds[3].get_text().replace("\xa0", " ").split("(")[0].strip(),
#              "chancellor" : tds[5].get_text(),
#              "vice_chancellor" : tds[6].get_text(),
#              "rector" : tds[7].get_text(),
#              "students" : tds[8].get_text().split("[")[0],
#              "location" : tds[9].get_text(),
#              "campus" : tds[10].get_text(),
#              "colors" : tds[11].get_text(),
#              "affiliations" : tds[4].get_text(),
#              "website" : tds[12].get_text(),
#              "logo" : target_table.find_all("td", class_ = "infobox-full-data")[1].find("img")["src"]
#     }

#     # Store data in json file
#     file_path = r"comillas.json"
#     print_json(data, file_path)
