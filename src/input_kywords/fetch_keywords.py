from langchain_community.chat_models import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.messages import SystemMessage, HumanMessage
import json

# Load and split PDF
pdf = PyPDFLoader("/Volumes/raaggee/RelevantJobs/src/data/Raaggee's Resume-2.pdf")
docs = pdf.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(docs)

system_prompt = """
You are an experienced HR. Your are given a candidate's Resume. 

Think in this way:
1. Look through the entire resume. 
2. Read and Analyze candidate's experience, education, skills and projects.
3. If the candiadate has job/internship experience, look for what relevant contributions they have made.
4. Exclude freelancing experience if any.
5. Analyze the projects, skills. Then ask, what sort of projects the candidate has made. Are they relevant to their skillset.
6. Once analyzed projects, skills and experience, now return what kind of job roles fits to the candidate. It can be existing job roles in which candiate has worked or some experience ones, based on your analysis.

Just look into current docuemnt. Do as I instruct. There should be no information outside the document.

Return the output in following format:
{"Skills": [list of skills separated by commas]}
{"Roles": [list of job roles separated by commas]}

Example:
User: <consider user has given the resume>. Now give a JSON output for the skills and relevant roles from the resume.
Response:  {
    {
    "Skills": ["Python", "C++", "SQl"]   
    },
    {
    "Roles": ["Data Science", "Data Analysis"]
    },
}
"""

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=f"Resume: {split_docs}"),
    HumanMessage(content=f"Here is the given resume. Give me JSON which has skills and relevant roles."),
]

llm = ChatOllama(
    model="llama3.2:latest",
)
result = llm(messages)
candiate_info = result.content

candidate_info_json = json.loads(candiate_info)
print(candiate_info)
job_roles = candidate_info_json["Roles"]
print(job_roles)
