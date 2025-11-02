"""
Hadith Verification Module
Verifies hadith claims and retrieves authentication information
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import requests
from typing import Dict, List, Optional
from config import Config


class HadithVerifier:
    """Verifies hadith claims against authenticated collections"""
    
    # Sunnah.com API base URL
    SUNNAH_BASE_URL = "https://api.sunnah.com/v1"
    
    # HadithAPI.com as backup (free tier)
    HADITH_API_BASE = "https://api.hadithapi.com/public/api"
    
    # Common hadith keywords
    HADITH_KEYWORDS = [
        "hadith", "hadis", "hadiths", "narrated", "reported", "prophet said",
        "messenger said", "allah's messenger", "bukhari", "muslim", "sahih",
        "tirmidhi", "abu dawud", "ibn majah", "nasai", "ahmad"
    ]
    
    def __init__(self):
        """Initialize Hadith verifier"""
        self.api_key = Config.SUNNAH_API_KEY
    
    def detect_hadith_claim(self, text: str) -> bool:
        """
        Detect if text contains a hadith-related claim
        
        Args:
            text: Text to check
        
        Returns:
            True if hadith-related keywords found
        """
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.HADITH_KEYWORDS)
    
    def search_hadith_sunnah_com(self, query: str, collection: Optional[str] = None) -> List[Dict]:
        """
        Search for hadiths using Sunnah.com API
        
        Args:
            query: Search query
            collection: Optional collection filter (bukhari, muslim, etc.)
        
        Returns:
            List of hadith results
        """
        if not self.api_key:
            return []  # API key not available
        
        try:
            url = f"{self.SUNNAH_BASE_URL}/hadiths/search"
            params = {
                "query": query,
                "page": 1,
                "limit": 5
            }
            
            if collection:
                params["collection"] = collection
            
            headers = {
                "X-API-Key": self.api_key
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                hadiths = []
                
                for item in data.get("hadiths", []):
                    hadiths.append({
                        "id": item.get("id"),
                        "text": item.get("body"),
                        "collection": item.get("collection", {}).get("name"),
                        "book": item.get("book", {}).get("name"),
                        "chapter": item.get("chapter", {}).get("name"),
                        "grade": item.get("grade"),
                        "narrator": item.get("narrator"),
                        "isnad": item.get("isnad", [])
                    })
                
                return hadiths
            else:
                return []
        except Exception as e:
            print(f"Error searching Sunnah.com: {e}")
            return []
    
    def search_hadith_hadithapi(self, query: str) -> List[Dict]:
        """
        Search for hadiths using HadithAPI.com (backup, free tier)
        
        Args:
            query: Search query
        
        Returns:
            List of hadith results
        """
        try:
            # HadithAPI.com free tier endpoint
            url = f"{self.HADITH_API_BASE}/hadiths"
            params = {
                "search": query,
                "limit": 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                hadiths = []
                
                for item in data.get("hadiths", []):
                    hadiths.append({
                        "text": item.get("englishText") or item.get("arabicText"),
                        "collection": item.get("collection"),
                        "book": item.get("book"),
                        "number": item.get("hadithNumber"),
                        "grade": item.get("grade", "Unknown")
                    })
                
                return hadiths
            else:
                return []
        except Exception as e:
            print(f"Error searching HadithAPI: {e}")
            return []
    
    def get_hadith_grade(self, hadith_data: Dict) -> str:
        """
        Determine hadith grade from data
        
        Args:
            hadith_data: Hadith data dictionary
        
        Returns:
            Grade: "Sahih", "Hasan", "Da'if", "Mawdu", or "Unknown"
        """
        grade = hadith_data.get("grade", "").lower()
        
        if "sahih" in grade:
            return "Sahih"
        elif "hasan" in grade:
            return "Hasan"
        elif "da'if" in grade or "daif" in grade or "weak" in grade:
            return "Da'if"
        elif "mawdu" in grade or "fabricated" in grade or "maudoo" in grade:
            return "Mawdu"
        else:
            return "Unknown"
    
    def get_confidence_from_grade(self, grade: str) -> float:
        """
        Get confidence score based on hadith grade
        
        Args:
            grade: Hadith grade
        
        Returns:
            Confidence score 0-1
        """
        grade_confidence = {
            "Sahih": 0.95,
            "Hasan": 0.80,
            "Da'if": 0.40,
            "Mawdu": 0.0,
            "Unknown": 0.50
        }
        return grade_confidence.get(grade, 0.50)
    
    def verify_claim(self, claim: str) -> Dict:
        """
        Verify a hadith claim
        
        Args:
            claim: The claim text to verify
        
        Returns:
            Dictionary with verification results
        """
        if not self.detect_hadith_claim(claim):
            return {
                "is_hadith_related": False,
                "hadiths": []
            }
        
        # Try Sunnah.com first if API key available
        hadiths = []
        if self.api_key:
            hadiths = self.search_hadith_sunnah_com(claim)
        
        # Fallback to HadithAPI if no results
        if not hadiths:
            hadiths = self.search_hadith_hadithapi(claim)
        
        # Process and enhance hadith data
        processed_hadiths = []
        for hadith in hadiths:
            grade = self.get_hadith_grade(hadith)
            processed_hadiths.append({
                "text": hadith.get("text", ""),
                "grade": grade,
                "confidence": self.get_confidence_from_grade(grade),
                "collection": hadith.get("collection", "Unknown"),
                "book": hadith.get("book"),
                "chapter": hadith.get("chapter"),
                "number": hadith.get("number") or hadith.get("id"),
                "narrator": hadith.get("narrator"),
                "isnad": hadith.get("isnad", [])
            })
        
        return {
            "is_hadith_related": True,
            "hadiths": processed_hadiths
        }

