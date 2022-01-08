# PRÁCTICA 7 - Beautifulsoup
# María José Medina Hernández

# Imports
import requests
from bs4 import BeautifulSoup

def print_json(dic, file_path):
    with open(file_path, "w") as output_file:
        json.dump(dic, output_file)

# Get the URLs
#TODO: poner para q lea las url del otro archivo
with open(file_path, 'r') as f:
    reader = csv.reader(f, delimiter = ";")
    country_matrix = [row for row in reader]

# Download the HTML
url = "https://en.wikipedia.org/wiki/Comillas_Pontifical_University"
response = requests.get(url)

# Parse the HTML
soup = BeautifulSoup(response.content, "html.parser")

# Find the info card
# We search by class = "infobox vcard"
target_tables = soup.find_all("table", class_="infobox vcard")

# Check that there's only one element belonging to the class
len(target_tables)

# Get the element belonging to the class that we are aiming for
# (There's only one in this case)
target_table = target_tables[0]


# Data extraction

data = { "seal" : target_table.find("a").find("img")["src"],
         "motto_latin" : target_table.find_all("i")[0].get_text(),
         "motto_english" : target_table.find_all("i")[2].get_text(),
         "motto_spanish" : target_table.find_all("i")[1].get_text(),
         "type" : tds[2].get_text(),
         "established" : tds[3].get_text().replace("\xa0", " ").split("(")[0].strip(),
         "chancellor" : tds[5].get_text(),
         "vice_chancellor" : tds[6].get_text(),
         "rector" : tds[7].get_text(),
         "students" : tds[8].get_text().split("[")[0],
         "location" : tds[9].get_text(),
         "campus" : tds[10].get_text(),
         "colors" : tds[11].get_text(),
         "affiliations" : tds[4].get_text(),
         "website" : tds[12].get_text(),
         "logo" : target_table.find_all("td", class_ = "infobox-full-data")[1].find("img")["src"]
}

# Store data in json file
file_path = r"comillas.json"
print_json(data, file_path)
