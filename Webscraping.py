# Version de Sami
# Create a Python web scraper project using Beautiful Soup to extract job title, salary, company, location,
# job type and description from data related to Data science jobs around Montreal on Indeed

# import library
from bs4 import BeautifulSoup
import requests

# Request to website and download HTML contents
URL = "https://ca.indeed.com/jobs?q=Data+Scientist&l=Montr%C3%A9al%2C+QC&radius=0&start=40"
# Request to website and download HTML contents
page = requests.get(URL)
content = response.text

# Format the downloaded content into a readable format
soup = BeautifulSoup(content)
job_title = scrap.find(id= " ").find("h1".get_text())

# BeautifulSoup(page_response.content, "html.parser")
# page_content.find_all("p")[i].text

### please use a timeout to avoid a too frequent visits to the website or API.