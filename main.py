import requests as requests
import csv
from bs4 import BeautifulSoup

URL = "https://ca.indeed.com/jobs?q=Data+Scientist&l=Montr%C3%A9al%2C+QC&radius=0"
page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")
data_file = "data_science_jobs.csv"
#print(soup.prettify())

def data_file_init(data_file):
    try:
        with open(data_file, 'r') as output_file:
            pass  # nothing to do
    except FileNotFoundError:
        # Create an empty file
        open(data_file, 'a+', encoding='utf-8')
    finally:
        pass

def extract_company_name(soup):
    job = []
    for div in soup.find_all(name="div", attrs={"class": "company_location"}):
        for span in div.find_all(name="span", attrs={"class": "companyName"}):
            job.append(span.text)
    return(job)
    #print(job)

def extract_company_location(soup):
    location = []
    for div in soup.find_all(name="div", attrs={"class": "company_location"}):
        for div in div.find_all(name="div", attrs={"class": "companyLocation"}):
            location.append(div.text)
    return(location)
    #print(location)

def extract_company_salary(soup):
    salary = []
    for div in soup.find_all(name="div", attrs={"class": "slider_container"}):
        if ( div.find_all(name="div", attrs={"class": "salary-snippet"}) ):
            for span in div.find_all(name="div", attrs={"class": "salary-snippet"}):
                salary.append(span.text)
        else:
            salary.append("vide")
    return(salary)
    #print(salary)

def extract_job_description(soup):
    description = []
    for div in soup.find_all(name="div", attrs={"class": "slider_container"}):
        for div2 in div.find_all(name="div", attrs={"class": "job-snippet"}):
            #print(div2)
            uls = div2.find("ul")
            if(uls):
                for li in uls.findAll("li"):
                    desc = li
                description.append(desc)
            else:
                description.append(div2.text)
    return(description)
    #print(description)

def write_to_file(csv_file, job_name_list, job_location_list, job_salary_list, job_desc_list):
    with open(csv_file, "a+", encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(job_name_list)):
            content = [job_name_list[i], job_location_list[i], job_salary_list[i], job_desc_list[i]]
            writer.writerow(content)

job_name_list = extract_company_name(soup)
job_location_list = extract_company_location(soup)
job_salary_list = extract_company_salary(soup)
job_desc_list = extract_job_description(soup)
data_file_init(data_file)
write_to_file(data_file, job_name_list, job_location_list, job_salary_list, job_desc_list)
