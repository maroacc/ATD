#%%

# PRÁCTICA 9 - Spider
# María José Medina Hernández

#%%

# Imports
import requests
from bs4 import BeautifulSoup
import csv


# PRIMER NIVEL
# Obtener las URLs de los países

# Download the countries' HTML
url = "https://en.wikipedia.org/wiki/Lists_of_universities_and_colleges_by_country"
response = requests.get(url)


# Parse the countries' HTML
soup = BeautifulSoup(response.content, "html.parser")


# Find the lists
# We start with the universities in Africa (3)
# 9 in total

# Loop the continents (and subcontinents)
navigation_list = soup.find_all("ul")
countries = [] # List of countries
for i in range(3, 12):
    countries_list = navigation_list[i].find_all("li")
    for item in countries_list:
        countries.append([item.text, item.find("a")["href"]])


# Create or open a csv file to write to
file_path = r'countries.csv'
with open(file_path, 'w', newline = "") as f:
    writer = csv.writer(f, delimiter = ";")
    for row in countries:
        writer.writerow(row)


# SEGUNDO NIVEL
# Obtener las URLs de las universidades

# Obtain Germany's URLs


# Load countries.csv in a matrix
with open(file_path, 'r') as f:
    reader = csv.reader(f, delimiter = ";")
    country_matrix = [row for row in reader]


for row in country_matrix:
    if row[0] == 'Germany':
        relative_url = row[1]
        # Download the HTML of German Univeristies
        country = "Germany"
        url = f"https://en.wikipedia.org/{relative_url}"
        response = requests.get(url)

        # Parse the German Universities' HTML
        soup = BeautifulSoup(response.content, "html.parser")


        # Loop the continents (and subcontinents)
        navigation_list = soup.find_all("ul")
        universities = [] # List of countries
        for i in range(3, 12):
            universities_list = navigation_list[i].find_all("li")
            for item in universities_list:
                if ".jpg" not in item.find("a")["href"].lower():
                    universities.append([country, url, item.text, item.find("a")["href"]])


        # Create or open a csv file to write to
        file_path = r'universities.csv'
        with open(file_path, 'w', newline = "") as f:
            writer = csv.writer(f, delimiter = ";")
            for row in universities:
                writer.writerow(row)



