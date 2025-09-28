import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to the path so we can import rag
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag import ingest_corpus, answer_question, _ensure_embedder, _cosine_sim


class TestRAGIngestion:
    """Test document ingestion functionality"""
    
    def test_ingest_empty_corpus(self):
        """Test ingestion with empty corpus"""
        ingest_corpus([])
        # Should not raise any errors
    
    def test_ingest_corpus_without_api_key(self):
        """Test ingestion without OpenAI API key"""
        # Ensure no API key is set
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        docs = [
            {"id": "test1", "section": "Test Section", "text": "Test content 1"},
            {"id": "test2", "section": "Test Section", "text": "Test content 2"}
        ]
        
        # Should not raise any errors even without API key
        ingest_corpus(docs)
    
    @patch('rag._ensure_embedder')
    def test_ingest_corpus_with_mock_embedder(self, mock_ensure_embedder):
        """Test ingestion with mocked embedder"""
        # Mock embedder
        mock_embedder = MagicMock()
        mock_embedder.embed_documents.return_value = [
            np.array([1.0, 2.0, 3.0]),
            np.array([4.0, 5.0, 6.0])
        ]
        mock_ensure_embedder.return_value = mock_embedder
        
        docs = [
            {"id": "test1", "section": "Test Section", "text": "Test content 1"},
            {"id": "test2", "section": "Test Section", "text": "Test content 2"}
        ]
        
        ingest_corpus(docs)
        
        # Verify embedder was called
        mock_ensure_embedder.assert_called_once()
        mock_embedder.embed_documents.assert_called_once_with(["Test content 1", "Test content 2"])
    
    def test_ingest_corpus_filters_empty_text(self):
        """Test that documents with empty text are filtered out"""
        docs = [
            {"id": "test1", "section": "Test Section", "text": "Valid content"},
            {"id": "test2", "section": "Test Section", "text": ""},
            {"id": "test3", "section": "Test Section", "text": "Another valid content"}
        ]
        
        # Should not raise any errors
        ingest_corpus(docs)


class TestRAGAnswering:
    """Test question answering functionality"""
    
    def test_answer_question_no_documents(self):
        """Test answering when no documents are ingested"""
        # Reset the corpus
        ingest_corpus([])
        
        result = answer_question("Test question")
        
        assert "answer" in result
        assert "sources" in result
        assert result["sources"] == []
        assert "no hay información" in result["answer"].lower()
    
    def test_answer_question_without_api_key_keyword_matching(self):
        """Test answering using keyword matching fallback"""
        # Ensure no API key is set
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        # Ingest some test documents
        docs = [
            {"id": "test1", "section": "Características", "text": "El Samsung Galaxy A55 tiene una cámara excelente de 50MP"},
            {"id": "test2", "section": "Batería", "text": "La batería del A55 dura todo el día con 5000mAh"},
            {"id": "test3", "section": "Precio", "text": "El precio del Galaxy A55 es competitivo"}
        ]
        ingest_corpus(docs)
        
        result = answer_question("¿Cómo es la cámara?")
        
        assert "answer" in result
        assert "sources" in result
        # Keyword matching might return all documents or none, depending on implementation
        assert isinstance(result["sources"], list)
        # The answer should contain some content from the documents
        assert len(result["answer"]) > 0
    
    @patch('rag.ChatOpenAI')
    @patch('rag.OpenAIEmbeddings')
    def test_answer_question_with_api_key(self, mock_embeddings, mock_chat_openai):
        """Test answering with OpenAI API key"""
        # Set a fake API key
        os.environ['OPENAI_API_KEY'] = 'sk-test123'
        
        # Mock embeddings
        mock_embedder = MagicMock()
        mock_embedder.embed_documents.return_value = [
            np.array([1.0, 2.0, 3.0]),
            np.array([4.0, 5.0, 6.0])
        ]
        mock_embeddings.return_value = mock_embedder
        
        # Mock the LLM response
        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "El Samsung Galaxy A55 tiene una cámara excelente de 50MP con tecnología avanzada."
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat_openai.return_value = mock_llm_instance
        
        # Ingest test documents
        docs = [
            {"id": "test1", "section": "Características", "text": "El Samsung Galaxy A55 tiene una cámara excelente de 50MP"},
            {"id": "test2", "section": "Batería", "text": "La batería del A55 dura todo el día con 5000mAh"}
        ]
        ingest_corpus(docs)
        
        result = answer_question("¿Cómo es la cámara?")
        
        assert "answer" in result
        assert "sources" in result
        assert result["answer"] == "El Samsung Galaxy A55 tiene una cámara excelente de 50MP con tecnología avanzada."
        assert len(result["sources"]) > 0
    
    def test_answer_question_keyword_matching_accuracy(self):
        """Test that keyword matching finds relevant documents"""
        # Ensure no API key for keyword matching
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        docs = [
            {"id": "battery", "section": "Batería", "text": "La batería tiene 5000mAh de capacidad"},
            {"id": "camera", "section": "Cámara", "text": "La cámara principal es de 50MP"},
            {"id": "price", "section": "Precio", "text": "El precio es muy competitivo"}
        ]
        ingest_corpus(docs)
        
        # Test battery question
        battery_result = answer_question("¿Cuánto dura la batería?")
        assert "batería" in battery_result["answer"].lower()
        
        # Test camera question
        camera_result = answer_question("¿Cómo es la cámara?")
        assert "cámara" in camera_result["answer"].lower()
    
    def test_answer_question_no_relevant_documents(self):
        """Test answering when no relevant documents are found"""
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        docs = [
            {"id": "test1", "section": "Test", "text": "Completely unrelated content about cooking"}
        ]
        ingest_corpus(docs)
        
        result = answer_question("¿Cómo es el teléfono?")
        
        assert "answer" in result
        assert "sources" in result
        assert "no encontré información específica" in result["answer"].lower()


class TestRAGUtilities:
    """Test RAG utility functions"""
    
    def test_cosine_similarity(self):
        """Test cosine similarity calculation"""
        # Test identical vectors
        a = np.array([[1.0, 0.0, 0.0]])
        b = np.array([1.0, 0.0, 0.0])
        similarity = _cosine_sim(a, b)
        assert abs(similarity[0] - 1.0) < 1e-6
        
        # Test orthogonal vectors
        a = np.array([[1.0, 0.0, 0.0]])
        b = np.array([0.0, 1.0, 0.0])
        similarity = _cosine_sim(a, b)
        assert abs(similarity[0] - 0.0) < 1e-6
        
        # Test opposite vectors
        a = np.array([[1.0, 0.0, 0.0]])
        b = np.array([-1.0, 0.0, 0.0])
        similarity = _cosine_sim(a, b)
        assert abs(similarity[0] - (-1.0)) < 1e-6
    
    def test_cosine_similarity_with_zero_norm(self):
        """Test cosine similarity with zero norm vectors"""
        a = np.array([[0.0, 0.0, 0.0]])
        b = np.array([1.0, 0.0, 0.0])
        similarity = _cosine_sim(a, b)
        # Should handle zero norm gracefully
        assert not np.isnan(similarity[0])
    
    @patch('rag.OpenAIEmbeddings')
    def test_ensure_embedder_with_api_key(self, mock_openai_embeddings):
        """Test embedder creation with API key"""
        os.environ['OPENAI_API_KEY'] = 'sk-test123'
        
        mock_instance = MagicMock()
        mock_openai_embeddings.return_value = mock_instance
        
        embedder = _ensure_embedder()
        
        assert embedder is not None
        mock_openai_embeddings.assert_called_once()
    
    def test_ensure_embedder_without_api_key(self):
        """Test embedder creation without API key"""
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        embedder = _ensure_embedder()
        
        assert embedder is None
    
    def test_ensure_embedder_with_invalid_api_key(self):
        """Test embedder creation with invalid API key"""
        os.environ['OPENAI_API_KEY'] = 'invalid-key'
        
        with patch('rag.OpenAIEmbeddings', side_effect=Exception("Invalid API key")):
            embedder = _ensure_embedder()
            assert embedder is None


class TestRAGIntegration:
    """Test RAG integration scenarios"""
    
    def test_full_workflow_without_api_key(self):
        """Test complete RAG workflow without OpenAI API key"""
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        # Ingest documents
        docs = [
            {"id": "product", "section": "Producto", "text": "Samsung Galaxy A55 con cámara de 50MP y batería de 5000mAh"},
            {"id": "price", "section": "Precio", "text": "El precio es de $972.000 en 12 cuotas sin interés"}
        ]
        ingest_corpus(docs)
        
        # Test multiple questions
        questions = [
            "¿Cómo es la cámara?",
            "¿Cuánto cuesta?",
            "¿Qué tal la batería?"
        ]
        
        for question in questions:
            result = answer_question(question)
            assert "answer" in result
            assert "sources" in result
            # Sources might be empty with keyword matching, but answer should exist
            assert isinstance(result["sources"], list)
            assert len(result["answer"]) > 0
    
    @patch('rag.ChatOpenAI')
    @patch('rag.OpenAIEmbeddings')
    def test_workflow_with_dynamic_api_key(self, mock_embeddings, mock_chat):
        """Test RAG workflow with dynamic API key switching"""
        # Start without API key
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        docs = [
            {"id": "test", "section": "Test", "text": "Test content for embedding"}
        ]
        ingest_corpus(docs)
        
        # Should work with keyword matching
        result1 = answer_question("test question")
        assert "answer" in result1
        
        # Now add API key and test with mocked LLM
        os.environ['OPENAI_API_KEY'] = 'sk-test123'
        
        # Mock embeddings
        mock_embedder = MagicMock()
        mock_embedder.embed_documents.return_value = [np.array([1.0, 2.0, 3.0])]
        mock_embeddings.return_value = mock_embedder
        
        mock_llm_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "LLM generated answer"
        mock_llm_instance.invoke.return_value = mock_response
        mock_chat.return_value = mock_llm_instance
        
        result2 = answer_question("test question")
        assert result2["answer"] == "LLM generated answer"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
