import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_tool = TavilySearchResults(api_key=TAVILY_API_KEY)

def fetch_web_results(query, num_results=5):
    """
    Fetches web search results using Tavily API.
    """
    try:
        results = tavily_tool.run(tool_input=query, num_results=num_results)
        
        # 🔍 Debugging: Print raw Tavily API response
        print("\nRAW RESULTS FROM TAVILY:\n", results)

        extracted_results = []
        for result in results:
            extracted_results.append({
                "title": result.get("title", f"Result {len(extracted_results)+1}"),  
                "content": result.get("content", "Content not available."),
                "url": result.get("url", "#")
            })


        # 🔍 Debugging: Print extracted results
        print("\n✅ Extracted Results:")
        for i, res in enumerate(extracted_results):
            print(f"{i+1}. {res['title']} - {res['url']}")

        return extracted_results

    except Exception as e:
        print("Error fetching web results:", str(e))
        return []
