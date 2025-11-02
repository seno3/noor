"""
Fiqh (Islamic Jurisprudence) Verification Module
Identifies and verifies Islamic rulings and legal matters
"""
import re
from typing import Dict, List, Optional


class FiqhVerifier:
    """Verifies fiqh rulings and identifies madhab-specific differences"""
    
    # Fiqh-related keywords
    FIQH_KEYWORDS = [
        "halal", "haram", "permissible", "forbidden", "prohibited", "allowed",
        "makruh", "mustahabb", "sunnah", "obligatory", "fard", "wajib",
        "ruling", "fatwa", "fiqh", "jurisprudence", "legal", "islamic law"
    ]
    
    # Madhab keywords
    MADHAB_KEYWORDS = {
        "hanafi": ["hanafi", "hanafiyah"],
        "maliki": ["maliki", "malikiyah"],
        "shafi": ["shafi'i", "shafii", "shafi'ee", "shafi"],
        "hanbali": ["hanbali", "hanbaliyah"]
    }
    
    def __init__(self):
        """Initialize Fiqh verifier"""
        pass
    
    def detect_fiqh_claim(self, text: str) -> bool:
        """
        Detect if text contains fiqh-related content
        
        Args:
            text: Text to check
        
        Returns:
            True if fiqh-related keywords found
        """
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.FIQH_KEYWORDS)
    
    def detect_madhabs(self, text: str) -> List[str]:
        """
        Detect which madhabs (schools of thought) are mentioned
        
        Args:
            text: Text to analyze
        
        Returns:
            List of detected madhabs
        """
        text_lower = text.lower()
        detected_madhabs = []
        
        for madhab, keywords in self.MADHAB_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_madhabs.append(madhab.capitalize())
        
        return detected_madhabs
    
    def verify_claim(self, claim: str) -> Dict:
        """
        Verify a fiqh-related claim
        
        Args:
            claim: The claim text to verify
        
        Returns:
            Dictionary with fiqh verification results
        """
        if not self.detect_fiqh_claim(claim):
            return {
                "is_fiqh_related": False,
                "fiqh_rulings": []
            }
        
        madhabs = self.detect_madhabs(claim)
        
        # Extract key terms
        ruling_terms = []
        for keyword in self.FIQH_KEYWORDS:
            if keyword in claim.lower():
                ruling_terms.append(keyword)
        
        rulings = []
        
        # If specific madhabs mentioned, note that
        if madhabs:
            for madhab in madhabs:
                rulings.append({
                    "madhab": madhab,
                    "note": f"Claim mentions {madhab} school of thought. Rulings may vary between madhabs.",
                    "requires_scholarly_consultation": True
                })
        else:
            # General fiqh claim
            rulings.append({
                "note": "This appears to be a fiqh (Islamic jurisprudence) matter. Complex fiqh issues may vary by school of thought (madhab) and require scholarly consultation.",
                "requires_scholarly_consultation": True
            })
        
        return {
            "is_fiqh_related": True,
            "fiqh_rulings": rulings,
            "detected_madhabs": madhabs,
            "ruling_terms": ruling_terms
        }

