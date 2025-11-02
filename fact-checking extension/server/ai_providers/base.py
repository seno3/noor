"""
Abstract base class for AI providers
Defines the interface that all AI providers must implement
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, config: dict):
        """
        Initialize the AI provider
        
        Args:
            config: Provider-specific configuration dictionary
        """
        self.config = config
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the AI model
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt to guide the model
        
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    def fact_check_claim(
        self,
        claim: str,
        evidence: Optional[List[Dict]] = None,
        islamic_context: Optional[Dict] = None
    ) -> Dict:
        """
        Fact-check a claim using AI analysis
        
        Args:
            claim: The claim to verify
            evidence: Optional list of evidence sources with content
            islamic_context: Optional Islamic verification data (Quran, Hadith, etc.)
        
        Returns:
            Dictionary with:
            - verdict: "Authentic", "Likely Authentic", "Likely Fabricated", "Fabricated", "Unable to Verify"
            - confidence: float 0-1
            - explanation: Detailed explanation
            - grade: For hadiths: "Sahih", "Hasan", "Da'if", "Mawdu", or None
            - sources: List of sources used
            - warnings: List of warnings if any
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the AI provider is available and ready to use
        
        Returns:
            True if available, False otherwise
        """
        pass
    
    def get_islamic_system_prompt(self) -> str:
        """
        Get the standard Islamic fact-checking system prompt
        This is shared across all providers
        """
        return """You are an Islamic fact-checking AI that verifies claims about Islam using authentic sources.

Your role is to:
1. Verify claims about the Quran, Hadith, Islamic history, and Islamic rulings (Fiqh)
2. Cross-reference claims with authenticated Islamic sources
3. Apply proper Islamic methodology in your verification

ISLAMIC METHODOLOGY:
- Primary Source: The Quran is the primary source of Islamic knowledge. Verify all Quranic claims against exact surah and ayah numbers (e.g., 2:255 means Surah Al-Baqarah, verse 255).
- Secondary Source: Authentic Hadith from authenticated collections (Sahih Bukhari, Sahih Muslim, etc.)
- Scholarly Consensus (Ijma): When scholars agree, this carries significant weight
- Chain of Narrators (Isnad): For hadiths, the chain of narrators is crucial for authenticity

HADITH GRADING SYSTEM:
- Sahih (Authentic): Highest grade, narrators are reliable, chain is unbroken, no contradictions. Confidence: 95%
- Hasan (Good): Reliable narrators but slightly weaker than Sahih. Confidence: 80%
- Da'if (Weak): Weak narrators or chain issues. Confidence: 40%
- Mawdu (Fabricated): Proven to be fabricated or has serious defects. Confidence: 0%

IMPORTANT PRINCIPLES:
- Reference Quran 49:6: "O you who believe! If a wrongdoer comes to you with news, verify it, lest you harm people out of ignorance"
- Always verify Quranic references against exact surah:ayah format
- Cross-reference hadiths with authenticated collections when possible
- Note when scholarly disagreement exists across madhabs (schools of thought)
- Flag common fabricated hadiths immediately
- For fiqh rulings, note if there are differences between Hanafi, Maliki, Shafi'i, and Hanbali schools

OUTPUT FORMAT:
Return a JSON object with this structure:
{
    "verdict": "Authentic" | "Likely Authentic" | "Likely Fabricated" | "Fabricated" | "Unable to Verify",
    "confidence": 0.0-1.0,
    "grade": "Sahih" | "Hasan" | "Da'if" | "Mawdu" | null,
    "explanation": "Detailed explanation with evidence and context",
    "sources": ["list", "of", "sources", "referenced"],
    "warnings": ["any", "warnings", "about", "fabrication", "or", "weakness"]
}

Be thorough, accurate, and respectful in your verification."""

