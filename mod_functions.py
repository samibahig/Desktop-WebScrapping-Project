import csv
import datetime
import re
from bs4 import BeautifulSoup
import requests as requests


# Les paramètres globaux du projet
base_url = "https://ca.indeed.com"
base_query = "/jobs?q=Data+Scientist&start="
data_file = "data_science_jobs.csv"
sleep_time = 3600


# Connexion et récupération des données.
def get_soup(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36'}
    response = requests.get(url, headers=headers, timeout=50)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")


# Vérification si une
def is_captcha_page(soup):
    title = soup.find('title')
    if title.string == "hCaptcha solve page":
        return True
    else:
        return False


# Initialisation du fichier CSV
def data_file_init(file_name=data_file):
    try:
        with open(file_name, 'r') as output_file:
            pass  # nothing to do
    except FileNotFoundError:
        # Create an empty file with a date
        open(file_name, 'a+', encoding='utf-8')
        headers = ['JOB_TITLE', 'JOB_LOCATION', 'JOB_SALARY_RANGE', 'JOB_DESCRIPTION', 'POSTING_DATE', 'SCRAPING_DATE']
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
    finally:
        pass


# Nettoyage du contenu des tag HTML
def clean_html_tag(html_data):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_data)


# Extraction du nom de la compagnie qui recrute
def extract_company_name(soup):
    job = []
    for div in soup.find_all(name="div", attrs={"class": "company_location"}):
        if div.find_all(name="span", attrs={"class": "companyName"}):
            for span in div.find_all(name="span", attrs={"class": "companyName"}):
                job.append(span.text)
        else:
            job.append("vide")
    return job


# Extraction de la localisation de l'offre d'emploi
def extract_company_location(soup):
    location = []
    for div in soup.find_all(name="div", attrs={"class": "company_location"}):
        for div2 in div.find_all(name="div", attrs={"class": "companyLocation"}):
            location.append(div2.text)
    return location


# Extraction du salaire de l'offre si disponible
def extract_company_salary(soup):
    salary = []
    for div in soup.find_all(name="div", attrs={"class": "slider_container"}):
        if div.find_all(name="div", attrs={"class": "salary-snippet"}):
            for span in div.find_all(name="div", attrs={"class": "salary-snippet"}):
                salary.append(span.text)
        else:
            salary.append("vide")
    return salary


# Extraction de la courte description d'eomploi.
def extract_job_description(soup):
    description = []
    for div in soup.find_all(name="div", attrs={"class": "slider_container"}):
        for div2 in div.find_all(name="div", attrs={"class": "job-snippet"}):
            uls = div2.find("ul")
            if uls:
                for li in uls.findAll("li"):
                    desc = str(li)
                description.append(clean_html_tag(desc))
            else:
                description.append(div2.text)
    return description


# Extraction de l'ancienneté de la publication
def extract_job_posting_date(soup):
    date = []
    for div in soup.find_all(name="div", attrs={"class": "result-footer"}):
        for span in div.find_all(name="span", attrs={"class": "date"}):
            date.append(span.text)
    return date


# Écriture dans le fichier CSV
def write_to_file(csv_file, job_name_list, job_location_list, job_salary_list, job_desc_list, job_posting_date):
    with open(csv_file, "a+", encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(job_name_list)):
            now = datetime.datetime.now()
            content = [job_name_list[i], job_location_list[i], job_salary_list[i], job_desc_list[i],
                       job_posting_date[i], now.strftime("%Y-%m-%d %H:%M:%S")]
            writer.writerow(content)


# Vérification du status de la prochaine page à scraper
def check_next_page_status(page_url, query):
    soup = get_soup(page_url)
    result = False
    for div in soup.find_all(name="div", attrs={"class": "pagination"}):
        for li in div.find_all("li"):
            for a in li.find_all('a', href=True):
                if a['href'] and a['href'] == query:
                    result = True
                    break
                else:
                    result = False
    return result
