# Imports
import pdftotext
import re
import json

def load_pdf(pdf_path):
    with open(pdf_path, "rb") as input_file:
        pdf = pdftotext.PDF(input_file)
    return pdf

def extract_data_from_pdf(pdf):
    """
    Extracts the data for each company of the Registered Acts of the First Section of the Mercantile Gazette (BORME pdf).
    
    Params
    -------
    pdf : pdftotext.PDF
        The pdf containing the Registered Acts of the First Section of the Mercantile Gazette.

    Return
    -------
    data : dict
        Dictionary containing the data for each company.
    """
    data = {}
    for page in pdf:
        paragraph = ""
        old_id = None
        aux = {}
        for line in page.splitlines():
            # Gets the first word of each line and checks whether it is an ID
            new_id = line.strip().split(" ")[0]
            if new_id.isdigit():
                if old_id:
                    # Remove multiple spaces
                    paragraph = re.sub(' +', ' ', paragraph)
                    ceses, nombramientos, ampliacion, domicilio, objeto, otros, registrales = extract_concepts(paragraph)
                    if ceses:
                        aux["ceses"] = ceses
                    if nombramientos:
                        aux["nombramientos"] = nombramientos
                    if ampliacion:
                        aux["ampliacion"] = ampliacion
                    if domicilio:
                        aux["domicilio"] = domicilio
                    if objeto:
                        aux["objeto"] = objeto
                    if otros:
                        aux["otros"] = otros
                    if registrales:
                        aux["registrales"] = registrales
                    data[name] = aux
                paragraph = ""
                aux = {}
                name = line.split("-")[1].strip().split(".")[0]
                aux["id"] = new_id
                old_id = new_id
            else:
                paragraph =  f"{paragraph}{line}"
    return data

def extract_concepts(paragraph):
    """
    Extracts the different concepts from an entry of the BORME pdf.
    
    Params
    -------
    paragraph : string
        The paragraph of each entry (eg. Otros conceptos: Declaración de insolvencia total por importe de 11.137,78 euros. Datos registrales. T 982, L 746, F 66, S 8, H AB
26079, I/A 2 (25.11.19).).

    Return
    -------
    ceses : string
        Termination of a position (eg. Adm. Unico: LLORENTE MERINO RAFAEL.).
    """
    # Declare variables
    ceses = ""
    nombramientos = ""
    ampliacion = ""
    domicilio = ""
    objeto = ""
    otros = ""
    registrales = ""
    
    if "Ceses/Dimisiones." in paragraph:
        ceses = paragraph.split("Ceses/Dimisiones.")[1].split("Nombramientos.")[0].split("Ampliación de capital.")[0].split("Cambio de domicilio social.")[0].split("Cambio de objeto social.")[0].split("Otros conceptos:")[0].split("Datos registrales.")[0]
    if "Nombramientos." in paragraph:
        nombramientos = paragraph.split("Nombramientos.")[1].split("Ampliación de capital.")[0].split("Cambio de domicilio social.")[0].split("Cambio de objeto social.")[0].split("Otros conceptos:")[0].split("Datos registrales.")[0]
    if "Ampliación de capital." in paragraph:
        ampliacion = paragraph.split("Ampliación de capital.")[1].split("Cambio de domicilio social.")[0].split("Cambio de objeto social.")[0].split("Otros conceptos:")[0].split("Datos registrales.")[0]
    if "Cambio de domicilio social." in paragraph:
        domicilio = paragraph.split("Cambio de domicilio social.")[1].split("Cambio de objeto social.")[0].split("Otros conceptos:")[0].split("Datos registrales.")[0]
    if "Cambio de objeto social." in paragraph:
        objeto = paragraph.split("Cambio de objeto social.")[1].split("Otros conceptos:")[0].split("Datos registrales.")[0]
    if "Otros conceptos:" in paragraph:
        otros = paragraph.split("Otros conceptos:")[1].split("Datos registrales.")[0]
    if "Datos registrales." in paragraph:
        registrales = paragraph.split("Datos registrales.")[1]
    return ceses, nombramientos, ampliacion, domicilio, objeto, otros, registrales

def print_json(dic, file_path):
    with open(file_path, "w") as output_file:
        json.dump(dic, output_file)
        

# Load a pdf of the Registered Acts of the First Section of the Mercantile Gazette
pdf = load_pdf("BORME-A-2019-232-02.pdf")

# Load the data of the pdf into a python dictionary
data = extract_data_from_pdf(pdf)

# Save the data into a json file
print_json(data, "datos_empresas.json")
