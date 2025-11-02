"""
Source Credibility Registry
Maintains registry of trusted Islamic sources with credibility scores
"""
from typing import Dict, Optional
from urllib.parse import urlparse


class SourceCredibilityRegistry:
    """Registry of trusted Islamic sources with credibility scores"""
    
    def __init__(self):
        """Initialize source registry"""
        self.trusted_sources = self._load_trusted_sources()
    
    def _load_trusted_sources(self) -> Dict[str, Dict]:
        """
        Load registry of trusted Islamic sources
        
        Returns:
            Dictionary mapping domains to source metadata
        """
        return {
            # Hadith Databases (Highest credibility)
            "sunnah.com": {
                "credibility": 95,
                "category": "Hadith Database",
                "description": "Authenticated hadith collections with grading"
            },
            "hadithapi.com": {
                "credibility": 85,
                "category": "Hadith Database",
                "description": "Comprehensive hadith database"
            },
            
            # Quran Sources
            "quran.com": {
                "credibility": 95,
                "category": "Quran",
                "description": "Official Quran text and translations"
            },
            "alquran.cloud": {
                "credibility": 95,
                "category": "Quran API",
                "description": "AlQuran Cloud API"
            },
            
            # Fatwa and Fiqh Sources
            "islamqa.info": {
                "credibility": 90,
                "category": "Fatwa/Fiqh",
                "description": "Scholarly fatwa database"
            },
            "islamqa.org": {
                "credibility": 90,
                "category": "Fatwa/Fiqh",
                "description": "Islamic Q&A with scholarly answers"
            },
            
            # Research and Educational Institutions
            "yaqeeninstitute.org": {
                "credibility": 90,
                "category": "Research/Education",
                "description": "Yaqeen Institute for Islamic Research"
            },
            "seekersguidance.org": {
                "credibility": 85,
                "category": "Education",
                "description": "SeekersGuidance Islamic education platform"
            },
            "islamicstudies.info": {
                "credibility": 80,
                "category": "Education",
                "description": "Islamic studies resources"
            },
            
            # General Islamic Websites
            "islamweb.net": {
                "credibility": 75,
                "category": "General",
                "description": "General Islamic website"
            },
            "onislah.com": {
                "credibility": 70,
                "category": "General",
                "description": "General Islamic content"
            },
        }
    
    def get_credibility_score(self, url: str) -> int:
        """
        Get credibility score for a source URL
        
        Args:
            url: Source URL
        
        Returns:
            Credibility score (0-100), 50 if unknown
        """
        try:
            domain = urlparse(url).netloc.lower()
            
            # Remove www. prefix
            if domain.startswith("www."):
                domain = domain[4:]
            
            # Check exact match
            if domain in self.trusted_sources:
                return self.trusted_sources[domain]["credibility"]
            
            # Check subdomain matches (e.g., api.quran.com)
            for known_domain, data in self.trusted_sources.items():
                if domain.endswith(f".{known_domain}") or known_domain in domain:
                    return data["credibility"]
            
            # Default for unknown sources
            return 50
        except:
            return 50
    
    def get_source_info(self, url: str) -> Optional[Dict]:
        """
        Get full source information
        
        Args:
            url: Source URL
        
        Returns:
            Source metadata dictionary or None
        """
        try:
            domain = urlparse(url).netloc.lower()
            
            # Remove www. prefix
            if domain.startswith("www."):
                domain = domain[4:]
            
            # Check exact match
            if domain in self.trusted_sources:
                info = self.trusted_sources[domain].copy()
                info["domain"] = domain
                return info
            
            # Check subdomain matches
            for known_domain, data in self.trusted_sources.items():
                if domain.endswith(f".{known_domain}") or known_domain in domain:
                    info = data.copy()
                    info["domain"] = domain
                    return info
            
            return None
        except:
            return None
    
    def is_trusted(self, url: str, threshold: int = 70) -> bool:
        """
        Check if source is trusted (above threshold)
        
        Args:
            url: Source URL
            threshold: Minimum credibility score (default 70)
        
        Returns:
            True if source is trusted
        """
        return self.get_credibility_score(url) >= threshold

