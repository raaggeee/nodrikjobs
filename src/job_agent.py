from selenium import webdriver
from scrapper.scrapper_class import JobAgent
from langchain.agents import Tool, initialize_agent
from langchain_ollama.llms import OllamaLLM
from bs4 import BeautifulSoup
import time

def scrape_jobs(job_url: str="https://www.naukri.com/data-science-jobs-in-delhi?k=data%20science&l=delhi&experience=1", base_url: str = "https://www.naukri.com/") -> str:
    driver = webdriver.Chrome()
    driver.get(job_url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    job_agent = JobAgent(driver, base_url, soup)

    job_agent.get_naukri_jobs()
    job_agent.save_df()
    
    driver.quit()

    return "job_data.cav"

tools = [
    Tool(
        name="JobScrapper",
        func=scrape_jobs,
        description="This is used to scrape multiple data science jobs from naukri"
    )
]


agent = initialize_agent(
    tools,
    llm = OllamaLLM(model="llama3.2:latest"),
    agent= "zero-shot-react-description",
    verbose=True
)

agent.run("https://www.naukri.com/data-science-jobs-in-delhi?k=data%20science&l=delhi&experience=1")


