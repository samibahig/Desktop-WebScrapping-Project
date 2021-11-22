
from bs4 import BeautifulSoup
import requests

pages_totales = {1:, 2: 10, 3: 20, 4: 30, 5: 40, 6: 50, 7: 60}
pageNo = pages_totales.keys()

def get_data(pageNo):
    headers = {"job_title": "JOB_LOCATION" 	"JOB_SALARY_RANGE"	"JOB_DESCRIPTION"}
    # Request to website and download HTML contents
    URL = "https://ca.indeed.com/jobs?q=Data+Scientist&l=Montr%C3%A9al%2C+QC&radius=0"+"&start=" +str(pages_totales.get('page'))
    # Request to website and download HTML contents
    page = requests.get(URL)
    content = response.text

    # Format the downloaded content into a readable format
    soup = BeautifulSoup(content, "html.parser")

    jobs = []   ### Get Jobs
    location = []  ### get location
    salary = []  ### get salary
    description = []  ### get description

    for d in soup.find_all(name="div", attrs={"class": "company_location"}):
        for span in div.find_all(name="span", attrs={"class": "companyName"}):
            job.append(span.text)
        for div in div.find_all(name="div", attrs={"class": "companyLocation"}):
            location.append(div.text)
    for div in soup.find_all(name="div", attrs={"class": "slider_container"}):
        if (div.find_all(name="div", attrs={"class": "salary-snippet"})):
            for span in div.find_all(name="div", attrs={"class": "salary-snippet"}):
                salary.append(span.text)
        else:
            salary.append("vide")
        for div2 in div.find_all(name="div", attrs={"class": "job-snippet"}):
            #print(div2)
            uls = div2.find("ul")
            if(uls):
                for li in uls.findAll("li"):
                    desc = li
                description.append(desc)
            else:
                description.append(div2.text)
    final_list = jobs + location + salary + description
    return final_list

results = []
for i in range(1, len(pages_totales)+1):
    results.append(get_data(i))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=[   ])
df.to_csv('Datascience_jobs.csv', index=False, encoding='utf-8')


#job_title = scrap.find(id= " ").find("h1".get_text())

# BeautifulSoup(page_response.content, "html.parser")
# page_content.find_all("p")[i].text

### please use a timeout to avoid a too frequent visits to the website or API.

# Version de Sami
# Create a Python web scraper project using Beautiful Soup to extract job title, salary, company, location,
# job type and description from data related to Data science jobs around Montreal on Indeed

# import library