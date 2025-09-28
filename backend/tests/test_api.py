import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json
import os
import sys

# Add the parent directory to the path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, SAMPLE_ITEM, REVIEWS_DATA

client = TestClient(app)


class TestItemEndpoint:
    """Test the /item endpoint"""
    
    def test_get_item_success(self):
        """Test successful item retrieval"""
        response = client.get("/item")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check main item fields
        assert data["title"] == SAMPLE_ITEM.title
        assert data["price"] == SAMPLE_ITEM.price
        assert data["currency"] == SAMPLE_ITEM.currency
        assert data["stock"] == SAMPLE_ITEM.stock
        assert data["ratings"] == SAMPLE_ITEM.ratings
        assert data["reviews_count"] == SAMPLE_ITEM.reviews_count
        
        # Check seller info
        assert data["seller"]["name"] == SAMPLE_ITEM.seller.name
        assert data["seller"]["reputation"] == SAMPLE_ITEM.seller.reputation
        assert data["seller"]["sales"] == SAMPLE_ITEM.seller.sales
        
        # Check payment methods
        assert len(data["payment_methods"]) == 4
        assert any(method["type"] == "credit_card" for method in data["payment_methods"])
        assert any(method["type"] == "transfer" for method in data["payment_methods"])
        
        # Check images
        assert len(data["images"]) == 6
        assert all(image.startswith("/") for image in data["images"])
    
    def test_get_item_data_types(self):
        """Test that item data has correct types"""
        response = client.get("/item")
        data = response.json()
        
        assert isinstance(data["price"], (int, float))
        assert isinstance(data["stock"], int)
        assert isinstance(data["ratings"], (int, float))
        assert isinstance(data["reviews_count"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["description"], str)


class TestReviewsEndpoint:
    """Test the /reviews endpoint"""
    
    def test_get_reviews_success(self):
        """Test successful reviews retrieval"""
        response = client.get("/reviews")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check main review fields
        assert data["overall_rating"] == REVIEWS_DATA.overall_rating
        assert data["total_reviews"] == REVIEWS_DATA.total_reviews
        
        # Check rating breakdown
        assert data["rating_breakdown"]["five_stars"] == REVIEWS_DATA.rating_breakdown.five_stars
        assert data["rating_breakdown"]["four_stars"] == REVIEWS_DATA.rating_breakdown.four_stars
        
        # Check characteristic ratings
        assert len(data["characteristic_ratings"]) > 0
        for char_rating in data["characteristic_ratings"]:
            assert "name" in char_rating
            assert "rating" in char_rating
            assert isinstance(char_rating["rating"], (int, float))
        
        # Check individual reviews
        assert len(data["reviews"]) > 0
        for review in data["reviews"]:
            assert "id" in review
            assert "text" in review
            assert "rating" in review
            assert "author" in review
    
    def test_reviews_data_consistency(self):
        """Test that reviews data is consistent"""
        response = client.get("/reviews")
        data = response.json()
        
        # Check that total reviews matches breakdown
        breakdown = data["rating_breakdown"]
        total_from_breakdown = (
            breakdown["five_stars"] + 
            breakdown["four_stars"] + 
            breakdown["three_stars"] + 
            breakdown["two_stars"] + 
            breakdown["one_star"]
        )
        assert data["total_reviews"] == total_from_breakdown


class TestSearchEndpoint:
    """Test the /search endpoint"""
    
    @patch('httpx.AsyncClient')
    def test_search_success(self, mock_client_class):
        """Test successful search with Tavily API"""
        # Mock the async client instance
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        # Mock successful Tavily API response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Samsung Galaxy A55 en MercadoLibre",
                    "url": "https://articulo.mercadolibre.com.ar/MLA-123456789",
                    "content": "Samsung Galaxy A55 5G con excelente precio...",
                    "score": 0.95
                },
                {
                    "title": "Galaxy A55 256GB - MercadoLibre Argentina",
                    "url": "https://listado.mercadolibre.com.ar/galaxy-a55",
                    "content": "Encuentra Galaxy A55 en MercadoLibre...",
                    "score": 0.87
                }
            ]
        }
        mock_client.post.return_value = mock_response
        
        response = client.post("/search", json={"query": "samsung galaxy"})
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["results"]) == 2
        assert data["results"][0]["title"] == "Samsung Galaxy A55 en MercadoLibre"
        assert data["results"][0]["url"].startswith("https://")
        assert "content" in data["results"][0]
    
    @patch('httpx.AsyncClient')
    def test_search_api_failure(self, mock_client_class):
        """Test search when Tavily API fails"""
        # Mock the async client instance
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        # Mock API failure
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_client.post.return_value = mock_response
        
        response = client.post("/search", json={"query": "test query"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        response = client.post("/search", json={"query": ""})
        
        assert response.status_code == 200
        data = response.json()
        # Empty query might still return some default results from Tavily
        assert "results" in data
        assert isinstance(data["results"], list)
    
    def test_search_missing_query(self):
        """Test search with missing query field"""
        response = client.post("/search", json={})
        
        assert response.status_code == 422  # Validation error


class TestChatEndpoint:
    """Test the /agent/chat endpoint"""
    
    @patch('main.answer_question')
    def test_chat_success(self, mock_answer_question):
        """Test successful chat response"""
        # Mock successful answer
        mock_answer_question.return_value = {
            "answer": "El Samsung Galaxy A55 tiene una cámara excelente con 50MP.",
            "sources": [
                {"section": "Características del producto", "snippet": "Cámara de 50MP..."}
            ]
        }
        
        response = client.post(
            "/agent/chat", 
            json={"question": "¿Cómo es la cámara del teléfono?"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "sources" in data
        assert data["answer"] == "El Samsung Galaxy A55 tiene una cámara excelente con 50MP."
        assert len(data["sources"]) == 1
    
    @patch('main.answer_question')
    def test_chat_with_openai_key(self, mock_answer_question):
        """Test chat with OpenAI API key"""
        mock_answer_question.return_value = {
            "answer": "Respuesta con GPT-4",
            "sources": []
        }
        
        response = client.post(
            "/agent/chat", 
            json={
                "question": "¿Cuál es la batería?",
                "openai_key": "sk-test123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Respuesta con GPT-4"
    
    def test_chat_missing_question(self):
        """Test chat with missing question"""
        response = client.post("/agent/chat", json={})
        
        assert response.status_code == 422  # Validation error
    
    def test_chat_empty_question(self):
        """Test chat with empty question"""
        response = client.post("/agent/chat", json={"question": ""})
        
        # The endpoint currently accepts empty questions and returns a response
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data


class TestDataConsistency:
    """Test data consistency across endpoints"""
    
    def test_item_reviews_count_consistency(self):
        """Test that item and reviews have consistent review counts"""
        item_response = client.get("/item")
        reviews_response = client.get("/reviews")
        
        item_data = item_response.json()
        reviews_data = reviews_response.json()
        
        assert item_data["reviews_count"] == reviews_data["total_reviews"]
    
    def test_item_ratings_consistency(self):
        """Test that item and reviews have consistent ratings"""
        item_response = client.get("/item")
        reviews_response = client.get("/reviews")
        
        item_data = item_response.json()
        reviews_data = reviews_response.json()
        
        assert item_data["ratings"] == reviews_data["overall_rating"]


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_json_search(self):
        """Test search with invalid JSON"""
        response = client.post("/search", data="invalid json")
        assert response.status_code == 422
    
    def test_invalid_json_chat(self):
        """Test chat with invalid JSON"""
        response = client.post("/agent/chat", data="invalid json")
        assert response.status_code == 422


class TestPriceAndInstallments:
    """Test price and installment calculations"""
    
    def test_main_product_price(self):
        """Test that main product has correct price"""
        response = client.get("/item")
        data = response.json()
        
        assert data["price"] == 972000
    
    def test_payment_methods_installments(self):
        """Test that payment methods show correct installments"""
        response = client.get("/item")
        data = response.json()
        
        payment_methods = data["payment_methods"]
        
        # Check 6x installment
        six_x_method = next(
            (method for method in payment_methods 
             if "6x" in method["description"]), None
        )
        assert six_x_method is not None
        assert "162.000" in six_x_method["description"]
        
        # Check 12x installment
        twelve_x_method = next(
            (method for method in payment_methods 
             if "12x" in method["description"]), None
        )
        assert twelve_x_method is not None
        assert "81.000" in twelve_x_method["description"]
    
    def test_installment_calculations(self):
        """Test that installment calculations are mathematically correct"""
        response = client.get("/item")
        data = response.json()
        
        price = data["price"]
        
        # 6x installments: 972000 / 6 = 162000
        six_x_amount = 162000
        assert price / 6 == six_x_amount
        
        # 12x installments: 972000 / 12 = 81000
        twelve_x_amount = 81000
        assert price / 12 == twelve_x_amount


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
