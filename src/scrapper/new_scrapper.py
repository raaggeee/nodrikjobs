import requests 
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapper_class import JobAgent

driver = webdriver.Chrome()
base_url = "https://www.naukri.com/"
driver.get(base_url)

input_element = driver.find_element(By.CLASS_NAME, "suggestor-input ")

input_element.send_keys("Data Science")

input_element.send_keys(Keys.RETURN)

input_url = driver.current_url
print(input_url)
driver.get(input_url)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
job_pages = soup.find("div", class_="styles_pages__v1rAK")
print(job_pages)
# job_agent = JobAgent(driver, input_url, soup)

# job_agent.get_naukri_jobs()
# time.sleep(1000)
# job_agent.save_df()
