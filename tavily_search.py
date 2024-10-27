from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()
from tavily import TavilyClient

# Step 1. Instantiating your TavilyClient
tavily_client = TavilyClient(api_key=os.getenv("TVLY_API_KEY"))

# Step 2. Executing a context search query
context = tavily_client.get_search_context(query="What happened during the Burning Man floods?")

# Step 3. That's it! You now have a context string that you can feed directly into your RAG Application
print(context)