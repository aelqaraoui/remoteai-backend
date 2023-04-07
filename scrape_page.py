import requests
from bs4 import BeautifulSoup

url = 'https://ai-jobs.net/job/41853-senior-analytics-engineer/'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
div = soup.find('div', class_='head-fluid')
h1 = div.find('h1')

title = h1.text

h3 = div.find('h3')

location = h3.text

print(title, location)

badges = [badge.text for badge in soup.find_all('span', class_='badge')[:3]]

job_type = badges[0]
job_level = badges[1]
salary = badges[2]

print(job_type, job_level, salary)

company = soup.find('h2', class_='h5').text

print(company)

description = soup.find('div', id='job-description').text

print(description)

import json

with open("jobs/" + url.split("/")[-2], "w") as f:

    print(json.dump({
        "url": url,
        "title": title,
        "location": location,
        "jobType": job_type,
        "jobLevel": job_level,
        "salary": salary,
        "company": company,
        "description": description,
    }, f))