"""
Unit tests for Brain module with multilingual support.
Tests cover: language switching, prompt generation, LLM responses, error handling.
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from brain import Brain, LANGUAGE_PROMPTS


class TestBrainMultilingual:
    """Test suite for multilingual Brain functionality"""
    
    @pytest.fixture
    def brain(self):
        """Create a Brain instance for testing"""
        memory = {'language': 'ru'}
        return Brain(memory)
    
    def test_brain_initialization(self):
        """Test Brain initialization with default language"""
        memory = {'language': 'ru'}
        brain = Brain(memory)
        assert brain.language == 'ru'
        assert brain.conversation_history == []
        assert brain.client is None
    
    def test_set_language_russian(self, brain):
        """Test setting language to Russian"""
        brain.set_language('ru')
        assert brain.language == 'ru'
    
    def test_set_language_yakut(self, brain):
        """Test setting language to Yakut (Sakha)"""
        brain.set_language('sah')
        assert brain.language == 'sah'
    
    def test_set_language_english(self, brain):
        """Test setting language to English"""
        brain.set_language('en')
        assert brain.language == 'en'
    
    def test_set_language_invalid(self, brain):
        """Test setting invalid language falls back to Russian"""
        brain.set_language('invalid_lang')
        assert brain.language == 'ru'
    
    def test_get_prompt_russian(self, brain):
        """Test getting Russian prompts"""
        brain.language = 'ru'
        prompt = brain._get_prompt('system')
        assert 'IDA OS' in prompt
        assert 'русском' in prompt
    
    def test_get_prompt_yakut(self, brain):
        """Test getting Yakut prompts"""
        brain.language = 'sah'
        prompt = brain._get_prompt('system')
        assert 'IDA OS' in prompt
    
    def test_get_prompt_english(self, brain):
        """Test getting English prompts"""
        brain.language = 'en'
        prompt = brain._get_prompt('system')
        assert 'IDA OS' in prompt
        assert 'English' in prompt
    
    def test_get_prompt_with_formatting(self, brain):
        """Test prompt formatting with parameters"""
        brain.language = 'ru'
        prompt = brain._get_prompt('thought', input='test input')
        assert 'test input' in prompt
    
    def test_generate_thought(self, brain):
        """Test thought generation"""
        with patch.object(brain, '_get_llm_response', return_value='Test thought'):
            thought = brain.generate_thought('test input')
            assert thought == 'Test thought'
    
    def test_add_to_history(self, brain):
        """Test adding conversation to history"""
        brain.add_to_history('Hello', 'Hi there')
        assert len(brain.conversation_history) == 1
        assert brain.conversation_history[0]['user'] == 'Hello'
        assert brain.conversation_history[0]['response'] == 'Hi there'
    
    def test_add_multiple_to_history(self, brain):
        """Test adding multiple conversations to history"""
        brain.add_to_history('Q1', 'A1')
        brain.add_to_history('Q2', 'A2')
        brain.add_to_history('Q3', 'A3')
        assert len(brain.conversation_history) == 3
    
    @patch('brain.OpenAI')
    def test_get_client_success(self, mock_openai, brain):
        """Test successful OpenAI client initialization"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            client = brain._get_client()
            assert client is not None
    
    @patch('brain.OpenAI', side_effect=Exception('API Error'))
    def test_get_client_failure(self, mock_openai, brain):
        """Test OpenAI client initialization failure"""
        client = brain._get_client()
        assert client is None
    
    @patch.object(Brain, '_get_client')
    def test_generate_response_no_client(self, mock_client, brain):
        """Test response generation when client is missing"""
        mock_client.return_value = None
        response = brain.generate_response('test')
        assert 'missing' in response.lower() or 'API' in response
    
    @patch.object(Brain, '_get_client')
    def test_generate_response_with_client(self, mock_client, brain):
        """Test response generation with valid client"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='Test response'))]
        
        mock_api_client = Mock()
        mock_api_client.chat.completions.create.return_value = mock_response
        mock_client.return_value = mock_api_client
        
        response = brain.generate_response('test input')
        assert response == 'Test response'
    
    @patch.object(Brain, '_get_llm_response')
    @patch.object(Brain, '_get_client')
    def test_generate_response_empty_fallback(self, mock_client, mock_llm, brain):
        """Test response generation with empty response fallback"""
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=''))]
        
        mock_api_client = Mock()
        mock_api_client.chat.completions.create.return_value = mock_response
        mock_client.return_value = mock_api_client
        mock_llm.return_value = 'Fallback response'
        
        response = brain.generate_response('test input')
        assert response == 'Fallback response'
    
    def test_decide_tool_weather(self, brain):
        """Test tool decision for weather query"""
        with patch.object(brain, '_get_llm_response', return_value='{"tool": "weather", "arg": "Moscow"}'):
            tool, arg = brain.decide_tool('What is the weather in Moscow?')
            assert tool == 'weather'
            assert arg == 'Moscow'
    
    def test_decide_tool_calculator(self, brain):
        """Test tool decision for calculator"""
        with patch.object(brain, '_get_llm_response', return_value='{"tool": "calculator", "arg": "2+2"}'):
            tool, arg = brain.decide_tool('Calculate 2+2')
            assert tool == 'calculator'
            assert arg == '2+2'
    
    def test_decide_tool_none(self, brain):
        """Test tool decision when no tool is needed"""
        with patch.object(brain, '_get_llm_response', return_value='{"tool": null, "arg": null}'):
            tool, arg = brain.decide_tool('Hello')
            assert tool is None
            assert arg is None
    
    def test_decide_tool_invalid_json(self, brain):
        """Test tool decision with invalid JSON response"""
        with patch.object(brain, '_get_llm_response', return_value='invalid json'):
            tool, arg = brain.decide_tool('test')
            assert tool is None
            assert arg is None
    
    def test_language_prompts_completeness(self):
        """Test that all languages have all required prompt keys"""
        required_keys = {'system', 'thought', 'tool_decision', 'api_error', 'llm_error', 'empty_response', 'news_fallback'}
        for lang, prompts in LANGUAGE_PROMPTS.items():
            assert set(prompts.keys()) == required_keys, f"Language '{lang}' missing required prompts"
    
    def test_multilingual_consistency(self):
        """Test that all languages have non-empty prompts"""
        for lang, prompts in LANGUAGE_PROMPTS.items():
            for key, value in prompts.items():
                assert isinstance(value, str), f"Language '{lang}' prompt '{key}' is not a string"
                assert len(value) > 0, f"Language '{lang}' prompt '{key}' is empty"


class TestBrainIntegration:
    """Integration tests for Brain module"""
    
    def test_full_conversation_flow(self):
        """Test complete conversation flow"""
        memory = {'language': 'ru'}
        brain = Brain(memory)
        
        # Add multiple exchanges
        brain.add_to_history('Hello', 'Hi')
        brain.add_to_history('How are you?', 'I am fine')
        
        assert len(brain.conversation_history) == 2
        assert brain.language == 'ru'
    
    def test_language_switching_mid_conversation(self):
        """Test switching language during conversation"""
        memory = {'language': 'ru'}
        brain = Brain(memory)
        
        brain.add_to_history('Привет', 'Привет')
        assert brain.language == 'ru'
        
        brain.set_language('en')
        assert brain.language == 'en'
        
        brain.add_to_history('Hello', 'Hi')
        assert len(brain.conversation_history) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
