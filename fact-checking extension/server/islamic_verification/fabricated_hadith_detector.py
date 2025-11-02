import re
from typing import Dict, List, Optional


class FabricatedHadithDetector:
        self.fabricated_patterns = self._load_fabricated_patterns()
    
    def _load_fabricated_patterns(self) -> List[Dict]:
        return [
            {
                "pattern": r".*love.*country.*part.*faith.*",
                "common_text": "Love of one's country is part of faith",
                "fabrication_source": "Ibn Taymiyyah's refutation, classified as fabricated by multiple scholars",
                "key_phrases": ["love of country", "part of faith", "love country faith"]
            },
            {
                "pattern": r".*seek.*knowledge.*china.*",
                "common_text": "Seek knowledge even if it is in China",
                "fabrication_source": "Classified as weak/da'if by hadith scholars",
                "key_phrases": ["seek knowledge", "china", "even in china"]
            },
            {
                "pattern": r".*difference.*opinion.*mercy.*",
                "common_text": "Differences of opinion in my ummah are a mercy",
                "fabrication_source": "Fabricated - attributed to Prophet but not found in authentic collections",
                "key_phrases": ["difference of opinion", "mercy", "ummah mercy"]
            },
            {
                "pattern": r".*my.*companions.*stars.*follow.*any.*",
                "common_text": "My companions are like stars; follow any of them and you will be guided",
                "fabrication_source": "Weak/fabricated according to multiple scholars including Al-Albani",
                "key_phrases": ["companions", "stars", "follow any"]
            },
            {
                "pattern": r".*paradise.*lies.*feet.*mother.*",
                "common_text": "Paradise lies at the feet of mothers",
                "fabrication_source": "Weak - the authentic version mentions 'mothers' in general context, not this exact phrasing",
                "key_phrases": ["paradise", "feet", "mother", "mothers"]
            },
            {
                "pattern": r".*cleanliness.*half.*faith.*",
                "common_text": "Cleanliness is half of faith",
                "fabrication_source": "Weak/da'if - authentic hadith says 'purity is half of faith' (purity = taharah, not general cleanliness)",
                "key_phrases": ["cleanliness", "half", "faith"]
            },
            {
                "pattern": r".*water.*is.*best.*drink.*world.*",
                "common_text": "Water is the best drink in this world and the hereafter",
                "fabrication_source": "Fabricated - not found in any authentic collection",
                "key_phrases": ["water", "best drink", "world", "hereafter"]
            },
            {
                "pattern": r".*whoever.*learns.*science.*time.*paradise.*",
                "common_text": "Whoever learns science in their time, will be in paradise",
                "fabrication_source": "Fabricated - misattributed to Prophet",
                "key_phrases": ["learns science", "time", "paradise"]
            },
            {
                "pattern": r".*marriage.*half.*religion.*",
                "common_text": "Marriage is half of religion",
                "fabrication_source": "Weak/fabricated - not found in authentic collections",
                "key_phrases": ["marriage", "half", "religion"]
            },
            {
                "pattern": r".*modesty.*part.*faith.*",
                "common_text": "Modesty is part of faith",
                "fabrication_source": "Weak - the authentic version is 'modesty brings nothing but good'",
                "key_phrases": ["modesty", "part", "faith"]
            },
            {
                "pattern": r".*world.*prison.*believer.*",
                "common_text": "The world is a prison for the believer and paradise for the disbeliever",
                "fabrication_source": "Fabricated - first part exists but second part is false",
                "key_phrases": ["world", "prison", "believer", "paradise"]
            },
            {
                "pattern": r".*anger.*devil.*",
                "common_text": "Anger is from the devil",
                "fabrication_source": "Fabricated - not found in authentic collections",
                "key_phrases": ["anger", "devil"]
            },
            {
                "pattern": r".*patience.*key.*relief.*",
                "common_text": "Patience is the key to relief",
                "fabrication_source": "Fabricated - not found in authentic collections",
                "key_phrases": ["patience", "key", "relief"]
            },
        ]
    
    def detect_fabrication(self, claim: str) -> Optional[Dict]:
        claim_lower = claim.lower()
        
        for pattern_data in self.fabricated_patterns:
            pattern = pattern_data["pattern"]
            
            if re.search(pattern, claim_lower, re.IGNORECASE):
                key_phrases_found = sum(
                    1 for phrase in pattern_data["key_phrases"]
                    if phrase in claim_lower
                )
                
                if key_phrases_found >= 4:
                    return {
                        "is_fabricated": True,
                        "matched_pattern": pattern_data["common_text"],
                        "fabrication_source": pattern_data["fabrication_source"],
                        "confidence": min(0.95, 0.7 + (key_phrases_found * 0.05)),
                        "warning": f"This appears to be a commonly fabricated hadith: '{pattern_data['common_text']}'"
                    }
                elif key_phrases_found >= 3:
                    return {
                        "is_fabricated": True,
                        "matched_pattern": pattern_data["common_text"],
                        "fabrication_source": pattern_data["fabrication_source"],
                        "confidence": 0.85,
                        "warning": f"Possibly matches fabricated hadith pattern: '{pattern_data['common_text']}'"
                    }
        
        return None
    
    def verify_claim(self, claim: str) -> Dict:
        fabrication_match = self.detect_fabrication(claim)
        
        if fabrication_match:
            return {
                "is_fabricated": True,
                "fabrication_details": fabrication_match,
                "warnings": [fabrication_match["warning"]]
            }
        else:
            return {
                "is_fabricated": False,
                "fabrication_details": None,
                "warnings": []
            }

