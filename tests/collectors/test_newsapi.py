import pytest
import aiohttp
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from core.data.collectors.news.newsapi import NewsAPICollector

@pytest.fixture
def collector_config():
    return {
        "api_key": "test_api_key",
        "keywords": ["crypto", "blockchain"],
        "language": "en",
        "max_articles": 10
    }

@pytest.fixture
def mock_response():
    return {
        "status": "ok",
        "totalResults": 2,
        "articles": [
            {
                "source": {"id": "test", "name": "Test Source"},
                "author": "Test Author",
                "title": "Test Title 1",
                "description": "Test Description 1",
                "url": "https://test.com/1",
                "urlToImage": "https://test.com/image1.jpg",
                "publishedAt": "2024-01-27T12:00:00Z",
                "content": "Test content 1 " * 20
            },
            {
                "source": {"id": "test", "name": "Test Source"},
                "author": "Test Author",
                "title": "Test Title 2",
                "description": "Test Description 2",
                "url": "https://test.com/2",
                "urlToImage": "https://test.com/image2.jpg",
                "publishedAt": "2024-01-27T13:00:00Z",
                "content": "Test content 2 " * 20
            }
        ]
    }

@pytest.mark.asyncio
async def test_connect_success(collector_config):
    """Test successful API connection"""
    
    async def mock_get(*args, **kwargs):
        mock_resp = AsyncMock()
        mock_resp.status = 200
        return mock_resp
    
    with patch("aiohttp.ClientSession.get", new=mock_get):
        collector = NewsAPICollector(collector_config)
        assert await collector.connect() is True

@pytest.mark.asyncio
async def test_connect_failure(collector_config):
    """Test failed API connection"""
    
    async def mock_get(*args, **kwargs):
        raise aiohttp.ClientError()
    
    with patch("aiohttp.ClientSession.get", new=mock_get):
        collector = NewsAPICollector(collector_config)
        assert await collector.connect() is False

@pytest.mark.asyncio
async def test_collect_success(collector_config, mock_response):
    """Test successful article collection"""
    
    async def mock_get(*args, **kwargs):
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_response)
        return mock_resp
    
    with patch("aiohttp.ClientSession.get", new=mock_get):
        collector = NewsAPICollector(collector_config)
        articles = await collector.collect()
        
        assert len(articles) == 2
        assert articles[0]["title"] == "Test Title 1"
        assert articles[1]["title"] == "Test Title 2"
        assert "collected_at" in articles[0]
        assert "metadata" in articles[0]

@pytest.mark.asyncio
async def test_collect_with_params(collector_config, mock_response):
    """Test article collection with parameters"""
    
    async def mock_get(*args, **kwargs):
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=mock_response)
        return mock_resp
    
    params = {
        "start_date": "2024-01-27",
        "end_date": "2024-01-28",
        "sort_by": "relevancy"
    }
    
    with patch("aiohttp.ClientSession.get", new=mock_get):
        collector = NewsAPICollector(collector_config)
        articles = await collector.collect(params)
        
        assert len(articles) == 2
        assert all("collected_at" in article for article in articles)

@pytest.mark.asyncio
async def test_validate_articles(collector_config):
    """Test article validation"""
    
    collector = NewsAPICollector(collector_config)
    
    test_articles = [
        {
            # Valid article
            "title": "Test Title",
            "content": "Test content " * 20,
            "url": "https://test.com",
            "published_at": "2024-01-27T12:00:00Z"
        },
        {
            # Invalid - missing content
            "title": "Test Title",
            "url": "https://test.com",
            "published_at": "2024-01-27T12:00:00Z"
        },
        {
            # Invalid - content too short
            "title": "Test Title",
            "content": "Short",
            "url": "https://test.com",
            "published_at": "2024-01-27T12:00:00Z"
        },
        {
            # Invalid - invalid date
            "title": "Test Title",
            "content": "Test content " * 20,
            "url": "https://test.com",
            "published_at": "invalid-date"
        }
    ]
    
    validated = await collector.validate(test_articles)
    assert len(validated) == 1
    assert validated[0]["title"] == "Test Title"
    assert len(validated[0]["content"]) >= 100 