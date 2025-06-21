import requests 
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin

class JobAgent:
    def __init__(self, driver, base_url, soup):
        self.df = pd.DataFrame()
        self.driver = driver
        self.base_url = base_url
        self.job_title_lst = []
        self.job_href_lst = []
        self.company_name_lst = []
        self.company_link_lst = []
        self.job_exp_lst = []
        self.job_loc_lst = []
        self.soup = soup
        self.count = 0

    def find_job_data(self, jobs):
        for job in jobs:
            job_title_row = job.find("div", class_="row1")
            job_title = job_title_row.find("a", class_="title")
            print(f"{count}")
            print(f"{job_title.text}")
            self.job_title_lst.append(job_title.text)
            self.job_href_lst.append(job_title["href"])
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


            self.company_name_lst.append(job_poster_title)
            self.company_link_lst.append(job_poster_link)

            #get the exp and location
            try:
                job_exp = job.find("span", class_="expwdth")
                if job_exp:
                    job_experience = job_exp["title"]
                else:
                    job_experience = "NA"
            except NoSuchElementException:
                job_experience = "NA"

            self.job_exp_lst.append(job_experience)

            try:
                job_loc = job.find("span", class_="locWdth")
                if job_loc:
                    job_location = job_loc["title"]
                else:
                    job_location = "NA"

            except NoSuchElementException:
                job_location = "NA"

            self.job_loc_lst.append(job_location)

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

            new_df =  pd.DataFrame({"Job Title": self.job_title_lst,
                        "Job Link": self.job_href_lst,
                        "Company": self.company_name_lst,
                        "Company Link": self.company_link_lst,
                        "Experience Required": self.job_exp_lst,
                        "Location": self.job_loc_lst})

        return new_df


    def get_naukri_jobs(self):
        job_pages = self.soup.find("div", class_="styles_pagination__oIvXh")
        page_next_button = job_pages.find_all("a", class_=["styles_btn-secondary__2AsIP"])
        while page_next_button[1]["href"] and count < 20:
            relative_url = page_next_button[1]["href"]
            print(relative_url)
            relative_url = f"{relative_url}"
            new_url = urljoin(self.base_url, relative_url)

            self.driver.get(new_url)
            time.sleep(5)

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

            job_data = self.find_job_data(job_cards, self.df)
            self.df = pd.concat([self.df, job_data], ignore_index=True)

            job_pages = soup.find("div", class_="styles_pagination__oIvXh")
            page_next_button = job_pages.find_all("a", class_=["styles_btn-secondary__2AsIP"])
            relative_url = page_next_button[1]["href"]
            count += 1

    def save_df(self):
        self.df.to_csv("job_data.csv", index=False)





    
    
