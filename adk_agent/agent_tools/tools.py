from pydantic import BaseModel
from typing import Optional
# from utils.competitor_scrapper import find_competitors, analyze_sentiment
# from utils.Scraper_Engine import save_scraped_content, Scraper
from fastapi import HTTPException
from pydantic import HttpUrl, field_validator
from typing import List
from urllib.parse import urlparse
from tavily import TavilyClient
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import os

# loading new env varibles
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")

# Define the request body as a Pydantic model
class CompetitorRequest(BaseModel):
    company_name: str
    industry: str
    use_cases: str
    location: Optional[str] = None  # Optional field

# Endpoint to accept user input and return competitors

# def get_competitors(
#     company_name: str,
#     industry: str,
#     use_cases: str,
#     location: Optional[str] = None

# ):
#     """
#     get competitors function to find competitors based on user input.
#     Args:
#         request (CompetitorRequest): The request object containing company_name, industry, use_cases, and location.

#     Returns:
#         dict: A dictionary containing the list of competitors and their sentiment analysis.

#     """
#     # Extract data from the request

#     # Get the list of competitors based on input data
#     competitors = find_competitors(industry, use_cases,location)

#     # Analyze sentiment for each competitor (for demonstration)
#     for competitor in competitors:
#         competitor['sentiment'] = analyze_sentiment(competitor['name'])

#     return {"competitors": competitors}



# # Unified Payload
# class ScrapperClass(BaseModel):
#     """
#     class to represent the payload for scraping URLs.
#     Args:
#         user_id (str): The user ID.
#         timestamp (str): The timestamp of the request.
#         s3_urls (Optional[List[str]]): List of S3 URLs to scrape.
#         web_urls (Optional[List[HttpUrl]]): List of web URLs to scrape.

#     Attributes:
#         user_id (str): The user ID.
#         timestamp (str): The timestamp of the request.
#         s3_urls (Optional[List[str]]): List of S3 URLs to scrape.
#         web_urls (Optional[List[HttpUrl]]): List of web URLs to scrape.
#     """
#     user_id: str
#     timestamp: str
#     s3_urls: Optional[List[str]] = []
#     web_urls: Optional[List[HttpUrl]] = []

#     @field_validator("s3_urls", mode="before")
#     @classmethod
#     def clean_s3_urls(cls, v):
#         return [url for url in v or [] if url and url.strip()]

#     @field_validator("web_urls", mode="before")
#     @classmethod
#     def clean_and_validate_web_urls(cls, v):
#         cleaned = []
#         for url in v or []:
#             url = url.strip()
#             if url:
#                 parsed = urlparse(url)
#                 if parsed.scheme and parsed.netloc:
#                     cleaned.append(url)
#         return cleaned

# def scrape_urls(
#     user_id: str,
#     timestamp: str,
#     s3_urls: Optional[List[str]] = [],
#     web_urls: Optional[List[str]] = []  # Changed from HttpUrl to str
# ):
#     """
#     scrape_urls function to scrape content from provided URLs.
#     Args:
#         user_id (str): The user ID.
#         timestamp (str): The timestamp of the request.
#         s3_urls (Optional[List[str]]): List of S3 URLs to scrape.
#         web_urls (Optional[List[str]]): List of web URLs to scrape.

#     Returns:
#         dict: A dictionary containing the status of the scraping process.
#     """
#     try:
#         # Clean s3_urls (formerly in ScrapperClass.clean_s3_urls)
#         s3_urls = [url for url in s3_urls or [] if url and url.strip()]
        
#         # Clean and validate web_urls (formerly in ScrapperClass.clean_and_validate_web_urls)
#         cleaned_web_urls = []
#         for url in web_urls or []:
#             url = str(url).strip()
#             if url:
#                 parsed = urlparse(url)
#                 if parsed.scheme and parsed.netloc:
#                     cleaned_web_urls.append(url)
#         web_urls = cleaned_web_urls
        
#         print(f"Received parameters - user_id: {user_id}, timestamp: {timestamp}, web_urls: {web_urls}, s3_urls: {s3_urls}")

#         if not web_urls:
#             raise ValueError("No input provided. Provide at least one Web URL.")

#         all_text = ""
#         scraped_file = None

#         # Handle Web URLs
#         if web_urls:
#             results = []
#             for url in web_urls:
#                 try:
#                     scraper = Scraper(str(url))
#                     scraper.scrape()
#                     content = scraper.get_html_content()

#                     if content == 'error':
#                         results.append({
#                             "url": str(url),
#                             "status": "error",
#                             "message": "Failed to scrape URL"
#                         })
#                     elif not content:
#                         results.append({
#                             "url": str(url),
#                             "status": "error",
#                             "message": "No content found"
#                         })
#                     else:
#                         results.append({
#                             "url": str(url),
#                             "status": "success",
#                             "content": content
#                         })

#                 except Exception as e:
#                     results.append({
#                         "url": str(url),
#                         "status": "error",
#                         "message": str(e)
#                     })

#             # Save and extract scraped content
#             scraped_file = save_scraped_content(results)
#             text = extract_text_from_file(scraped_file)
#             if text.strip():
#                 all_text += text + "\n"

#         if not all_text.strip():
#             raise Exception("No text extracted from any source.")

#         return {
#             "status": "done"
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

def search_tavily(query: str):
    """Search Tavily for a specific query.

    e.g Market rates for plumbing services in Victoria, BC
    
    Args:
        query (str): The query to search for.

    Returns:
        dict: The response from Tavily.
    """
    
    tavily_client = TavilyClient(api_key=tavily_api_key)
    response = tavily_client.search(query=query, search_depth="advanced")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

    return response
        
# get_competitors_tool = FunctionTool(func=get_competitors)
# scrape_urls_tool = FunctionTool(func=scrape_urls)
tavily_tool = FunctionTool(func=search_tavily)

tools = [tavily_tool]

