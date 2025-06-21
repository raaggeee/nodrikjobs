import requests 
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin


driver = webdriver.Chrome()
base_url = "https://www.naukri.com/"
driver.get("https://www.naukri.com/data-science-jobs-in-delhi?k=data%20science&l=delhi&experience=1")

time.sleep(5)

# print(job_cards[0])

def get_job_data(jobs, df):
    "this function takes the job_card and return it into dataframe"
    job_title_lst = []
    job_href_lst = []
    company_name_lst = []
    company_link_lst = []
    job_exp_lst = []
    job_loc_lst = []
    count = 0


    for job in jobs:
        job_title_row = job.find("div", class_="row1")
        job_title = job_title_row.find("a", class_="title")
        print(f"{count}")
        print(f"{job_title.text}")
        job_title_lst.append(job_title.text)
        job_href_lst.append(job_title["href"])
        print(f"{job_title["href"]}")

        #to get the company name
        job_poster_row = job.find("a", class_=[" comp-name",  "mw-25"])
        if job_poster_row:
            if job_poster_row["title"]:
                job_poster_title = job_poster_row["title"]

            else:
                job_poster_title = "NA"

            if job_poster_row["href"]:
                job_poster_link = job_poster_row["href"]

            else:
                job_poster_link = "NA"

        else:
            job_poster_title = "NA"
            job_poster_link = "NA"


        company_name_lst.append(job_poster_title)
        company_link_lst.append(job_poster_link)

        #get the exp and location
        try:
            job_exp = job.find("span", class_="expwdth")
            if job_exp:
                job_experience = job_exp["title"]
            else:
                job_experience = "NA"
        except NoSuchElementException:
            job_experience = "NA"

        job_exp_lst.append(job_experience)

        try:
            job_loc = job.find("span", class_="locWdth")
            if job_loc:
                job_location = job_loc["title"]
            else: 
                job_location = "NA"

        except NoSuchElementException:
            job_location = "NA"

        job_loc_lst.append(job_location)

        #get tags
        job_tags = job.find("ul", class_="tags-gt")
        if job_tags:
            job_tags_li = job_tags.find_all("li")
            job_tags_names=[]
            for tags in job_tags_li:
                job_tags_names.append(tags.text)
        else:
            job_tags = "NA"

        print(f"added {job_title["title"]}")
        count += 1
        print(f"\n")

    new_df =  pd.DataFrame({"Job Title": job_title_lst,
                        "Job Link": job_href_lst,
                        "Company": company_name_lst,
                        "Company Link": company_link_lst,
                        "Experience Required": job_exp_lst,
                        "Location": job_loc_lst})

    return new_df
    
# job_data = get_job_data(job_cards)

# print(job_data)
df = pd.DataFrame()
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
job_pages = soup.find("div", class_="styles_pagination__oIvXh")
page_next_button = job_pages.find_all("a", class_=["styles_btn-secondary__2AsIP"])
print(page_next_button[1]["href"])
count = 0

while page_next_button[1]["href"] and count < 20:
    relative_url = page_next_button[1]["href"]
    print(relative_url)
    relative_url = f"{relative_url}"
    new_url = urljoin(base_url, relative_url)

    driver.get(new_url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

    job_data = get_job_data(job_cards, df)
    df = pd.concat([df, job_data], ignore_index=True)

    job_pages = soup.find("div", class_="styles_pagination__oIvXh")
    page_next_button = job_pages.find_all("a", class_=["styles_btn-secondary__2AsIP"])
    relative_url = page_next_button[1]["href"]
    count += 1

df.to_csv("job_data.csv", index=False)

