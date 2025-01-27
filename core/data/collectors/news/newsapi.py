from typing import Any, Dict, List, Optional
import aiohttp
import asyncio
from datetime import datetime, timedelta

from ..base import BaseCollector

class NewsAPICollector(BaseCollector):
    """
    NewsAPI collector implementation.
    Collects news articles from NewsAPI.org.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the NewsAPI collector.
        
        Args:
            config: Configuration dictionary containing:
                - api_key: NewsAPI API key
                - keywords: List of keywords to track
                - language: Language of articles (default: en)
                - max_articles: Maximum number of articles per request
        """
        super().__init__(config)
        self.base_url = "https://newsapi.org/v2"
        self.api_key = config["api_key"]
        self.keywords = config.get("keywords", [])
        self.language = config.get("language", "en")
        self.max_articles = config.get("max_articles", 100)

    async def connect(self) -> bool:
        """
        Test connection to NewsAPI.
        
        Returns:
            bool: True if connection successful
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"X-Api-Key": self.api_key}
                async with session.get(
                    f"{self.base_url}/top-headlines",
                    headers=headers,
                    params={"language": self.language, "pageSize": 1}
                ) as response:
                    return response.status == 200
        except Exception as e:
            self.logger.error(f"Failed to connect to NewsAPI: {str(e)}")
            return False

    async def collect(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Collect news articles from NewsAPI.
        
        Args:
            params: Optional parameters including:
                - start_date: Start date for articles
                - end_date: End date for articles
                - sort_by: Sorting method (relevancy, popularity, publishedAt)
                
        Returns:
            List of collected articles
        """
        try:
            # Prepare parameters
            search_params = {
                "language": self.language,
                "pageSize": self.max_articles,
                "q": " OR ".join(self.keywords) if self.keywords else None,
                "sortBy": params.get("sort_by", "publishedAt")
            }
            
            if params and "start_date" in params:
                search_params["from"] = params["start_date"]
            if params and "end_date" in params:
                search_params["to"] = params["end_date"]
            
            # Remove None values
            search_params = {k: v for k, v in search_params.items() if v is not None}
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                headers = {"X-Api-Key": self.api_key}
                async with session.get(
                    f"{self.base_url}/everything",
                    headers=headers,
                    params=search_params
                ) as response:
                    if response.status != 200:
                        raise Exception(f"API request failed with status {response.status}")
                    
                    data = await response.json()
                    articles = data.get("articles", [])
                    
                    # Transform to standard format
                    return [
                        {
                            "id": f"newsapi_{i}",
                            "source": article["source"]["name"],
                            "title": article["title"],
                            "content": article["content"],
                            "url": article["url"],
                            "published_at": article["publishedAt"],
                            "collected_at": datetime.utcnow().isoformat(),
                            "metadata": {
                                "author": article.get("author"),
                                "description": article.get("description"),
                                "url_to_image": article.get("urlToImage")
                            }
                        }
                        for i, article in enumerate(articles)
                    ]
                    
        except Exception as e:
            self.logger.error(f"Failed to collect news: {str(e)}")
            return []

    async def validate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate collected articles.
        
        Args:
            data: List of collected articles
            
        Returns:
            List of validated articles
        """
        validated_articles = []
        
        for article in data:
            # Basic validation
            if not all(k in article for k in ["title", "content", "url", "published_at"]):
                continue
                
            # Content length validation
            if not article["content"] or len(article["content"]) < 100:
                continue
                
            # Date validation
            try:
                datetime.fromisoformat(article["published_at"].replace("Z", "+00:00"))
            except ValueError:
                continue
                
            validated_articles.append(article)
            
        return validated_articles 