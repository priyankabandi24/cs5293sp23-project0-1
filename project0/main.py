import urllib.request
import PyPDF2
import re
import os
import sqlite3
from datetime import datetime
import argparse

def download_pdf(url):
    """Downloads a PDF file from a URL and returns the filename."""
    now = datetime.now()
    filename = f"{now:%Y-%m-%d}_daily_incident_summary.pdf"
    urllib.request.urlretrieve(url, filename)
    if os.path.exists(filename):
        print("File downloaded successfully.")
        return filename
    else:
        raise Exception("Error downloading file.")

def extract_info_from_pdf(filename):
    """Extracts incident information from a PDF file using regular expressions."""
    with open(filename, "rb") as f:
        p = PyPDF2.PdfReader(f)
        info = []
        for page in p.pages:
            page_text = page.extract_text()
            if not page_text:
                continue
            lines = page_text.split("\n")
            for line in lines:
                date_time_match = re.search(r"\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{2}", line)
                if date_time_match:
                    date_time = date_time_match.group()
                    line = re.sub(date_time, "", line)
                incident_number_match = re.search(r"\d{4}-\d{8}", line)
                if incident_number_match:
                    incident_number = incident_number_match.group()
                    line = re.sub(incident_number, "", line)
                nature_match = re.search(r"[A-Z][a-z]+(?:[/ ][A-Za-z]+\s)?", line)
                if nature_match:
                    nature = nature_match.group().strip()
                    line = re.sub(nature, "", line)
                words = line.split()
                if len(words) > 1:
                    ori = words[-1]
                    location = "".join(words[:-1])
                    info.append({
                        "date_time": date_time if date_time_match else "",
                        "incident_number": incident_number if incident_number_match else "",
                        "nature": nature if nature_match else "",
                        "location": location,
                        "origin": ori
                    })
        return info

def insert_info_to_db(info):
    print('Connected')
    conn = sqlite3.connect('incidents.db')
    cursor = conn.cursor()
    cursor.execute('drop table if exists incidents')
    cursor.execute('''CREATE TABLE incidents
                 (date_time text, incident_number text, nature text, location text, origin text)''')
    for incident in info:
        cursor.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)",(incident['date_time'], incident['incident_number'], incident['nature'], incident['location'], incident['origin']))
    conn.commit()
    cursor.execute('SELECT nature, COUNT() FROM incidents GROUP BY nature ORDER BY COUNT() DESC')
    results = cursor.fetchall()
    for row in results:
        print(row[0], "|", row[1])
    #filename = download_pdf(url)
    #info = extract_info_from_pdf(filename)

if __name__ == "__main__":
    #url = "https://www.normanok.gov/sites/default/files/documents/2022-10/2022-10-06_daily_incident_summary.pdf"
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        #main(args.incidents)
        filename = download_pdf(args.incidents)
        info = extract_info_from_pdf(filename)
 #       for i, incident in enumerate(info):
  #          print(f"Incident {i+1}:")
   #         for k, v in incident.items():
    #            print(f"  {k}: {v}")
        insert_info_to_db(info)
