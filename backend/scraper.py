import asyncio
import random
import os
import re
import requests
from bs4 import BeautifulSoup
import html2text
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
api = os.getenv("OPENROUTER_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small", 
    api_key=api, 
    base_url="https://openrouter.ai/api/v1"
)

llm = ChatOpenAI(
    model="openrouter/owl-alpha",
    api_key=api,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.5
)
def universal_html_to_markdown(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    
    for element in soup(["script", "style", "nav", "footer", "header", "form", "aside", "noscript"]):
        element.extract()
        
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    
    markdown_text = h.handle(str(soup))
    markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
    return markdown_text.strip()

async def scrape_page(url: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(random.uniform(1.5, 3.5)) 
            
            raw_html = await page.content()
            await browser.close()
            
            return universal_html_to_markdown(raw_html)
    except Exception as e:
        return f"Error scraping the webpage: {str(e)}"

def scrape_page_basic(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return universal_html_to_markdown(response.text)
    except Exception:
        return ""
    
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


async def ask_webpage(url: str, question: str) -> str:
    parsed_markdown = await scrape_page(url)
    
    if len(parsed_markdown) < 200:
        parsed_markdown = scrape_page_basic(url)
        
    if not parsed_markdown or len(parsed_markdown) < 100 or parsed_markdown.startswith("Error"):
        return "Could not access this page cleanly. Context parsing failed."

    splitter=RecursiveCharacterTextSplitter(chunk_size=700,chunk_overlap=150)
    chunks=splitter.create_documents([parsed_markdown])

    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    relevant_docs = await retriever.ainvoke(question)
    context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = PromptTemplate(
        template="""
        You are an expert data analysis assistant.
        Answer the question ONLY using the provided Webpage Markdown Context below.
        If the context does not contain the necessary data to answer, say "I don't know".
        
        WEBPAGE MARKDOWN CONTEXT:
        \"\"\"
        {context}
        \"\"\"
        
        QUESTION: {question}
        """,
        input_variables=['context', 'question']
    )

    parser = StrOutputParser()
    chain = (
        {
            "context": (lambda x: x["question"]) | retriever | format_docs, 
            "question": lambda x: x["question"]
        }
        | prompt 
        | llm 
        | parser
    )

    try:
        return await chain.ainvoke({"context": context_text, "question": question})
    except Exception as e:
        return f"Error executing pipeline generation: {str(e)}"