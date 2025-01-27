import warnings
from crewai import Agent, Crew, Task
import os
from utils import get_openai_api_key,get_serper_api_key
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["SERPER_API_KEY"] = get_serper_api_key()
warnings.filterwarnings('ignore')


# Initialize the tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Agent 1: Senior Security Code reviewer
Senior_code_reviewer = Agent(
    role="Senior Security Code reviewer",
    goal="Manually inspect and identify possible security issues and vulnerabilities in the given {codebase} with an emphasis on secure coding practices",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "You have a proven track record of performing detailed code review"
        "with a focus on identifying security flaws, bad practices and potential vulnerabilities."
        "With an in-depth understanding of incorporating security throughout the software development lifecycle"
        "and secure coding techniques. You are proficient in multiple programming languages and a strong knowledge of security protocols and standards."
        "With a strong focus on thoroughly examining every part of the code to identify vulnerabilities."
    )
) 

# Agent 2:  Quality Assurance (QA) Specialist
qa_specialist = Agent(
    role="Quality Assurance Specialist",
    goal=" manually validate that the code meets the specified requirements by running tests in a variety of scenarios", 
    verbose=True,
    backstory=(
        "You are an experienced and highly acclaimed QA Specialist with a strong focus on security and quality assurance. With over 10 years of experience, you excel at manual and automated testing, identifying critical security flaws, bad practices, and vulnerabilities. "
    ),
    allow_delegation = True
) 
code_review = Task(
    description="Review the {codebase} aiming to identify as many potential"
    "security vulnerabilities, poor coding practices and performance issues.",
    expected_output="Report on code quality, security issues, and performance bottlenecks, with detailed recommendations and severity ratings formatted as markdown.",
    agent=Senior_code_reviewer
)
qa_task=Task(
    description="Check the identified vulnerabilities by the senior security code review and determine whether they match the {codebase} potential security vulnerabilities. Ensure they match security and best practices posture.",
    expected_output="Comprehensive test results report detailing functional and security issues, including bug descriptions, reproduction steps, severity ratings, and suggested fixes. The report should be formatted clearly in markdown, with a focus on critical issues and actionable feedback for the development team",
    # async_execution=True,
    agent=qa_specialist
)
event_management_crew = Crew(
    agents=[Senior_code_reviewer, 
            qa_specialist],
    
    tasks=[code_review, 
           qa_task],
    
    verbose=True
)
codebase = {
    'codebase': 
"""def check_login(username, password):
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
result = cursor.fetchone()
"""
}
result = event_management_crew.kickoff(inputs=codebase)

