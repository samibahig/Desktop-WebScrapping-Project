import requests as requests
import csv
import re
from bs4 import BeautifulSoup
import datetime

url_start = "https://ca.indeed.com/jobs?q=Data+Scientist"
url_query = "/jobs?q=Data+Scientist"
url_base = "https://ca.indeed.com"
page = requests.get(url_start)
soup = BeautifulSoup(page.text, "html.parser")
data_file = "data_science_jobs.csv"


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup


def data_file_init(data_file):
    try:
        with open(data_file, 'r') as output_file:
            pass  # nothing to do
    except FileNotFoundError:
        # Create an empty file
        open(data_file, 'a+', encoding='utf-8')
        headers = ['job_title', 'JOB_LOCATION', 'JOB_SALARY_RANGE', 'JOB_DESCRIPTION', 'POSTING_DATE', 'SCRAPING_DATE']
        with open(data_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
    finally:
        pass


def get_job_listing_pagination(soup, url_query):
    pagination = [url_query]
    for div in soup.find_all(name="div", attrs={"class": "pagination"}):
        for li in div.find_all("li"):
            for a in li.find_all('a', href=True):
                if a['href']:
                    uri = a['href']
                    pagination.append(uri)
    return pagination


def clean_html_tag(html_data):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_data)


def extract_company_name(soup):
    job = []
    for div in soup.find_all(name="div", attrs={"class": "company_location"}):
        if div.find_all(name="span", attrs={"class": "companyName"}):
            for span in div.find_all(name="span", attrs={"class": "companyName"}):
                job.append(span.text)
        else:
            job.append("vide")
    return job


def extract_company_location(soup):
    location = []
    for div in soup.find_all(name="div", attrs={"class": "company_location"}):
        for div in div.find_all(name="div", attrs={"class": "companyLocation"}):
            location.append(div.text)
    return location


def extract_company_salary(soup):
    salary = []
    for div in soup.find_all(name="div", attrs={"class": "slider_container"}):
        if div.find_all(name="div", attrs={"class": "salary-snippet"}):
            for span in div.find_all(name="div", attrs={"class": "salary-snippet"}):
                salary.append(span.text)
        else:
            salary.append("vide")
    return salary


def extract_job_description(soup):
    description = []
    for div in soup.find_all(name="div", attrs={"class": "slider_container"}):
        for div2 in div.find_all(name="div", attrs={"class": "job-snippet"}):
            # print(div2)
            uls = div2.find("ul")
            if uls:
                for li in uls.findAll("li"):
                    desc = str(li)
                description.append(clean_html_tag(desc))
            else:
                description.append(div2.text)
    return description


def extract_job_posting_date(soup):
    date = []
    for div in soup.find_all(name="div", attrs={"class": "result-footer"}):
        for span in div.find_all(name="span", attrs={"class": "date"}):
            date.append(span.text)
    return date


def write_to_file(csv_file, job_name_list, job_location_list, job_salary_list, job_desc_list, job_posting_date):
    with open(csv_file, "a+", encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(job_name_list)):
            now = datetime.datetime.now()
            content = [job_name_list[i], job_location_list[i], job_salary_list[i], job_desc_list[i],
                       job_posting_date[i], now.strftime("%Y-%m-%d %H:%M:%S")]
            writer.writerow(content)


data_file_init(data_file)
first_soup = get_soup(url_start)
pagination = get_job_listing_pagination(soup, url_query)
for page in range(len(pagination)):
    active_page = url_base + pagination[page]
    soup = get_soup(active_page)
    job_name_list = extract_company_name(soup)
    job_location_list = extract_company_location(soup)
    job_salary_list = extract_company_salary(soup)
    job_desc_list = extract_job_description(soup)
    job_post_date = extract_job_posting_date(soup)
    write_to_file(data_file, job_name_list, job_location_list, job_salary_list, job_desc_list, job_post_date)
