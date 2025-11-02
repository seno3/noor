"""
AI Provider Factory
Creates the appropriate AI provider based on configuration
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base import AIProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider
from config import Config


def create_ai_provider() -> AIProvider:
    """
    Factory function to create the appropriate AI provider
    
    Returns:
        Initialized AI provider instance
    """
    config = Config.get_ai_config()
    
    if Config.AI_PROVIDER == "ollama":
        return OllamaProvider(config)
    elif Config.AI_PROVIDER == "openai":
        return OpenAIProvider(config)
    else:
        raise ValueError(f"Unknown AI provider: {Config.AI_PROVIDER}")

