"""
Configuration management for Islamic Truth Verifier
Loads settings from environment variables with sensible defaults
"""
import os
from typing import Literal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration management"""
    
    # AI Provider Settings
    AI_PROVIDER: Literal["ollama", "openai"] = os.getenv("AI_PROVIDER", "ollama").lower()
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
    
    # Islamic API Keys
    SUNNAH_API_KEY: str = os.getenv("SUNNAH_API_KEY", "")
    ISLAMQA_API_KEY: str = os.getenv("ISLAMQA_API_KEY", "")
    
    # System Settings
    AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.3"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    MAX_CLAIMS_PER_VIDEO: int = int(os.getenv("MAX_CLAIMS_PER_VIDEO", "10"))
    CACHE_DURATION_DAYS: int = int(os.getenv("CACHE_DURATION_DAYS", "30"))
    
    # Feature Flags
    ENABLE_ISLAMIC_VERIFICATION: bool = os.getenv("ENABLE_ISLAMIC_VERIFICATION", "true").lower() == "true"
    ENABLE_YOUTUBE_PROCESSING: bool = os.getenv("ENABLE_YOUTUBE_PROCESSING", "true").lower() == "true"
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    ENABLE_FABRICATED_HADITH_DETECTION: bool = os.getenv("ENABLE_FABRICATED_HADITH_DETECTION", "true").lower() == "true"
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate configuration settings
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        
        if cls.AI_PROVIDER not in ["ollama", "openai"]:
            errors.append(f"Invalid AI_PROVIDER: {cls.AI_PROVIDER}. Must be 'ollama' or 'openai'")
        
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when AI_PROVIDER=openai")
        
        if cls.AI_TEMPERATURE < 0 or cls.AI_TEMPERATURE > 1:
            errors.append(f"AI_TEMPERATURE must be between 0 and 1, got {cls.AI_TEMPERATURE}")
        
        if cls.CONFIDENCE_THRESHOLD < 0 or cls.CONFIDENCE_THRESHOLD > 1:
            errors.append(f"CONFIDENCE_THRESHOLD must be between 0 and 1, got {cls.CONFIDENCE_THRESHOLD}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def get_ai_config(cls) -> dict:
        """Get AI-specific configuration"""
        if cls.AI_PROVIDER == "ollama":
            return {
                "base_url": cls.OLLAMA_BASE_URL,
                "model": cls.OLLAMA_MODEL,
                "temperature": cls.AI_TEMPERATURE
            }
        else:
            return {
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL,
                "temperature": cls.OPENAI_TEMPERATURE
            }

