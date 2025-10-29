"""
Integration tests for SUBOTAI system - Simplified
"""

import pytest
from src.core.subotai_core import SubotaiCore, get_subotai_core
from src.core.config import SubotaiConfig


def test_subotai_core_initialization():
    """Test that SubotaiCore initializes correctly"""
    core = SubotaiCore()
    assert core.initialize() == True
    assert core._initialized == True


def test_subotai_core_singleton():
    """Test that get_subotai_core returns singleton instance"""
    core1 = get_subotai_core()
    core2 = get_subotai_core()
    assert core1 is core2


def test_simple_query_processing():
    """Test basic query processing"""
    core = SubotaiCore()
    core.initialize()
    
    result = core.process_query("Hello, how are you?")
    
    assert 'response' in result
    assert 'metadata' in result
    assert isinstance(result['response'], str)
    assert len(result['response']) > 0


def test_query_with_context():
    """Test query processing with context"""
    core = SubotaiCore()
    core.initialize()
    
    context = {'source': 'test', 'user_id': '123'}
    result = core.process_query("Test query", context)
    
    assert 'response' in result
    assert 'metadata' in result


def test_system_status():
    """Test system status retrieval"""
    core = SubotaiCore()
    core.initialize()
    
    status = core.get_system_status()
    
    assert 'status' in status
    assert 'initialized' in status
    assert status['initialized'] == True


def test_health_check():
    """Test health check"""
    core = SubotaiCore()
    core.initialize()
    
    health = core.get_health()
    
    assert 'status' in health
    assert health['status'] == 'healthy'
    assert 'version' in health


def test_clean_output_mode():
    """Test clean output formatting"""
    core = SubotaiCore()
    core.initialize()
    
    context = {'clean_output': True}
    result = core.process_query("Test", context)
    
    assert 'response' in result
    # Response should not contain section tags like [ANALYSIS]
    assert '[ANALYSIS]' not in result['response']
    assert '[STRATEGY]' not in result['response']


def test_metadata_structure():
    """Test that metadata has required structure"""
    core = SubotaiCore()
    core.initialize()
    
    result = core.process_query("Test query")
    metadata = result['metadata']
    
    assert 'reasoning_mode' in metadata
    assert 'truth_shield' in metadata
    assert 'quality_gate' in metadata
    assert 'quality_metrics' in metadata


def test_error_handling():
    """Test error handling"""
    core = SubotaiCore()
    core.initialize()
    
    # Test with empty query
    result = core.process_query("")
    
    assert 'response' in result
    assert 'metadata' in result
