
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_job_details(job_url):
    response = requests.get(job_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract job description
        description_elem = soup.find('div', {'class': 'show-more-less-html__markup'})
        job_description = description_elem.text.strip() if description_elem else ''
        
        # Extract skills
        skills_elem = soup.find('div', {'class': 'job-criteria__list'})
        skills = [skill.text.strip() for skill in skills_elem.find_all('span', {'class': 'job-criteria__text'})] if skills_elem else []

        return job_description, skills
    else:
        return '', []

url = 'https://www.linkedin.com/jobs/search/?currentJobId=3834896045&f_WT=3%2C1%2C2&geoId=102713980&keywords=power%20bi%20developer&location=&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true&sortBy=R'
response = requests.get(url)

def scrap_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # print("scrapping now")
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('div', {'class':'job-search-card'})
        
        # Initialize lists to store job data
        titles = []
        companies = []
        locations = []
        links = []
        descriptions = []
        skills_list = []

        for job in job_listings:
            title = job.find('h3', {'class': 'base-search-card__title'}).text.strip()
            company = job.find('a', {'class': 'hidden-nested-link'}).text.strip()
            location = job.find('span', {'class': 'job-search-card__location'}).text.strip()
            anchor_tag = job.find('a', class_='base-card__full-link')
            href_link = anchor_tag['href']

            # Fetch job details
            job_description, skills = get_job_details(href_link)
            
            # Append data to lists
            titles.append(title)
            companies.append(company)
            locations.append(location)
            links.append(href_link)
            descriptions.append(job_description)
            skills_list.append(', '.join(skills))

        # Create DataFrame from lists
        df = pd.DataFrame({
            'Title': titles,
            'Company': companies,
            'Location': locations,
            'Job Link': links,
            'Job Description': descriptions,
            'Skills': skills_list
        })

        # Save DataFrame to CSV
        # df.to_csv('output/linkedinjobs.csv', index=False, encoding='utf-8')

        # print("Job listings saved to linkedinjobs.csv")
        return df
    else:
        print("Failed to fetch job listings.")






