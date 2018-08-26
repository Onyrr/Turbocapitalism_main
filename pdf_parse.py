import tabula
import requests
import csv, json
from tabula import convert_into
import urllib.request as url_req
from bs4 import BeautifulSoup
import pandas as pd

headers = {
     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
s = requests.session()
url = "http://www.dt.tesoro.it/en/debito_pubblico/emissioni_titoli_di_stato_interni/comunicazioni_emissioni_medio_lungo_termine/"
page = s.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
pdf_link = soup.find_all('a', {'class':'RowDownload _pdf pdf'})[0]['href']
pdf_link = "http://www.dt.tesoro.it" + pdf_link
convert_into(pdf_link, "data.csv", output_format="csv")
my_file =  open("data.csv", 'r')
reader = csv.reader(my_file)
rows = list(reader)
my_dict = {}
dates_header = ["Underwriting Deadline date for the Public", "Deadline date for Presentation of bids in auction strictly prior to 11.00 am", "Submission of bids for the supplementary auction no later than 3.30 pm on", "Settlement date"]
my_dict["dates header"] = dates_header
my_dict["dates"] = rows[2]

my_dict["header row"] = rows[3]
row_num = 1
for i in range(4, len(rows)):
	dict_key = "row " + str(row_num)
	my_dict[dict_key] = rows[i]
	row_num = row_num + 1
with open('data.json', 'w') as fp:
    json.dump(my_dict, fp, ensure_ascii=False)