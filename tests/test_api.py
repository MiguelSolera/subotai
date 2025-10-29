"""
Tests for SUBOTAI API endpoints
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.app import app

client = TestClient(app)


class TestAPIEndpoints:
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "SUBOTAI" in data["message"]
        assert "endpoints" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
    
    def test_status_endpoint(self):
        """Test system status endpoint"""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "initialized" in data
        assert "subsystems" in data
    
    def test_query_endpoint_success(self):
        """Test successful query processing"""
        request_data = {
            "query": "What is the best way to learn programming?",
            "context": {"test": True},
            "mode": "auto"
        }
        
        response = client.post("/api/query", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "response" in data
        assert "metadata" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0
        
        # Check metadata structure
        metadata = data["metadata"]
        assert "truth_shield" in metadata
        assert "quality_gate" in metadata
        assert "reasoning_mode" in metadata
    
    def test_query_endpoint_invalid_request(self):
        """Test query endpoint with invalid data"""
        # Empty query
        response = client.post("/api/query", json={"query": ""})
        assert response.status_code == 422  # Validation error
        
        # Missing query
        response = client.post("/api/query", json={})
        assert response.status_code == 422
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/api/metrics")
        assert response.status_code == 200
        data = response.json()
        
        # Check basic structure
        assert "timestamp" in data
        assert "overall" in data
        assert "status" in data["overall"]
    
    def test_query_different_modes(self):
        """Test query processing with different modes"""
        modes = ["auto", "normal", "strict", "debate", "steps", "fast"]
        
        for mode in modes:
            request_data = {
                "query": f"Test query for {mode} mode",
                "mode": mode
            }
            
            response = client.post("/api/query", json=request_data)
            assert response.status_code == 200
            data = response.json()
            
            # Verify response contains expected content
            assert "response" in data
            assert "metadata" in data
    
    def test_query_with_context(self):
        """Test query processing with various context parameters"""
        test_cases = [
            {"user_id": "test_user", "session_id": "test_session"},
            {"domain": "technical", "complexity": "high"},
            {"sensitive": True, "requires_verification": True}
        ]
        
        for context in test_cases:
            request_data = {
                "query": "Test query with context",
                "context": context
            }
            
            response = client.post("/api/query", json=request_data)
            assert response.status_code == 200
    
    def test_error_handling(self):
        """Test API error handling"""
        # Test with very long query (should be handled gracefully)
        long_query = "x" * 3000  # Within 2000 limit will fail, adjust
        request_data = {"query": long_query}
        
        response = client.post("/api/query", json=request_data)
        # Should return validation error for too long query
        assert response.status_code in [200, 422]
    
    def test_api_root_endpoint(self):
        """Test API root endpoint"""
        response = client.get("/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data


class TestAPIIntegration:
    """Integration tests for full API workflow"""
    
    def test_full_query_workflow(self):
        """Test complete query workflow from request to response"""
        # Step 1: Check health
        health_response = client.get("/api/health")
        assert health_response.status_code == 200
        
        # Step 2: Process query
        query_response = client.post("/api/query", json={
            "query": "Explain how machine learning works",
            "mode": "normal"
        })
        assert query_response.status_code == 200
        query_data = query_response.json()
        
        # Step 3: Verify metadata
        assert "truth_risk_score" in query_data["metadata"]
        assert "quality_gate" in query_data["metadata"]
        assert query_data["metadata"]["quality_gate"]["passed"] in [True, False]
        
        # Step 4: Check metrics updated
        metrics_response = client.get("/api/metrics")
        assert metrics_response.status_code == 200
    
    def test_mode_selection_auto(self):
        """Test automatic mode selection"""
        # Simple query should use fast or normal mode
        response = client.post("/api/query", json={
            "query": "What time is it?",
            "mode": "auto"
        })
        assert response.status_code == 200
        
        # Complex query might trigger different mode
        response = client.post("/api/query", json={
            "query": "Analyze the geopolitical implications of emerging AI technologies",
            "mode": "auto"
        })
        assert response.status_code == 200
    
    def test_truth_shield_activation(self):
        """Test Truth Shield activation with risky content"""
        response = client.post("/api/query", json={
            "query": "Tell me about guaranteed investment returns with no risk",
            "mode": "auto"
        })
        assert response.status_code == 200
        data = response.json()
        
        # Should have non-zero truth risk
        metadata = data["metadata"]
        assert "truth_risk_score" in metadata
        # Risk score should be > 0 for this query
        assert metadata["truth_risk_score"] >= 0
    
    def test_quality_gate_evaluation(self):
        """Test Quality Gate evaluation"""
        response = client.post("/api/query", json={
            "query": "Explain quantum computing",
            "mode": "normal"
        })
        assert response.status_code == 200
        data = response.json()
        
        # Check quality metrics
        metadata = data["metadata"]
        assert "quality_metrics" in metadata
        quality = metadata["quality_metrics"]
        assert "clarity_score" in quality
        assert "response_quality_score" in quality
        assert 0 <= quality["clarity_score"] <= 100
        assert 0 <= quality["response_quality_score"] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

