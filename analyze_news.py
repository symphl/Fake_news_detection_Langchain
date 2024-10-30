from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_community.tools import TavilySearchResults
from langchain.chains import LLMChain
import os
import getpass
from dotenv import load_dotenv
load_dotenv ()

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant",
    temperature=0.1)

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")

def fetch_news(query: str) -> str:
    resp = TavilySearchResults(max_results=10, 
                               search_depth="advanced", 
                               include_answer=True, 
                               include_raw_content=True).invoke({"query":f'{query}'})
    news_head = ''
    for headlines in range(len(resp)):
        news_head+= f'{headlines+1}) ' + resp[headlines]['content'] + '\n'
    
    return f'The following are the Top Headlines regarding the Topic\n {news_head}'

news_verification_template = PromptTemplate(
    input_variables=["query", "headlines"],
    template="""You are an expert fact-checker tasked with determining the veracity of news headlines. Analyze the following information carefully:

Query: {query}

Top Headlines:
{headlines}

Based on the query and the provided headlines, please determine if the news is likely true or false. Follow these steps:

1. Analyze the consistency of information across multiple headlines.
2. Check for reputable sources among the headlines.
3. Look for any conflicting information or red flags that might indicate false news.
4. Consider the plausibility of the news in the context of current events and known facts.
5. Evaluate the language used in the headlines for sensationalism or bias.

After your analysis, provide a conclusion on whether the news is likely true or false, and explain your reasoning. Your response should be structured as follows:

Conclusion: [True/False/Inconclusive]

Reasoning:
1. [First point supporting your conclusion]
2. [Second point supporting your conclusion]
3. [Third point supporting your conclusion]

Confidence Level: [High/Medium/Low]

Additional Notes: [Any other relevant observations or caveats]

Remember, it's important to maintain objectivity and base your conclusion on the available evidence. If there isn't enough information to make a definitive judgment, state that the veracity is inconclusive and explain why."""
)

news_verification_chain = LLMChain(llm=llm, prompt=news_verification_template)

def analyse_news(query):
    headlines = fetch_news(query)
    result = news_verification_chain.run(query=query, headlines=headlines)
    
    return result
