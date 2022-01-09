# Practica 10 - Spider + Scraper
Construct spider and scraper scripts for wikipedia pages of universities around the world

### Future Work Analysis

#### How to escalate
In order to escalate the script to be able to retrieve all the links from all the world universities, it would be necessary to iterate through all the links to all the lists of universities of every country in the countries.csv file

#### Expected issues
Some of the expected issues deriving from the escalation to all the countries pages will be:
- The lists will probably have a different format (eg in Algeria the list is inside a table and in Germany inside of a list), so the code must be changed to take this into account.
- Not all universities will have a wikipedia page, instead the link will reference the universities official webpage so they will be completely different from each other and the scraper will have to be customized for each page.  
- Some wikipedia pages will not be written in English and some may even be written with a different alphabet.
- The number of requests required for the spider and the scraper may be too much even for Wikipedia to handle, causing them to think they are experiencing a DoS attack and blocking our IP.

