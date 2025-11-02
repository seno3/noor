"""
Quran Verification Module
Verifies Quranic claims and extracts references
"""
import re
import requests
from typing import Dict, List, Optional


class QuranVerifier:
    """Verifies Quranic claims against AlQuran Cloud API"""
    
    # AlQuran Cloud API - No API key required
    BASE_URL = "https://api.alquran.cloud/v1"
    
    # Mapping of common surah names to numbers
    SURAH_NAMES = {
        "al-fatihah": 1, "fatihah": 1, "al-faatiha": 1,
        "al-baqarah": 2, "baqarah": 2, "baqara": 2,
        "ali-imran": 3, "aal-imran": 3, "imran": 3,
        "an-nisa": 4, "nisa": 4, "an-nisaa": 4,
        "al-maidah": 5, "maidah": 5, "al-maaeda": 5,
        # Add more common mappings as needed
    }
    
    def __init__(self):
        """Initialize Quran verifier"""
        pass
    
    def extract_quran_references(self, text: str) -> List[Dict]:
        """
        Extract all Quranic references from text
        
        Patterns supported:
        - 2:255 (surah:ayah)
        - Surah Al-Baqarah verse 255
        - Surah 2, Ayah 255
        - Al-Baqarah 255
        
        Returns:
            List of extracted references with surah and ayah numbers
        """
        references = []
        
        # Pattern 1: Simple surah:ayah (e.g., 2:255, 2: 255)
        pattern1 = r'(\d+)\s*[:]\s*(\d+)'
        for match in re.finditer(pattern1, text):
            surah = int(match.group(1))
            ayah = int(match.group(2))
            if 1 <= surah <= 114 and ayah > 0:
                references.append({
                    "surah": surah,
                    "ayah": ayah,
                    "match_text": match.group(0)
                })
        
        # Pattern 2: "Surah X verse Y" or "Surah X, Ayah Y"
        pattern2 = r'(?:surah|surat)\s+([\w\s-]+?)\s+(?:verse|ayah|aya|ayah|verse)\s+(\d+)'
        for match in re.finditer(pattern2, text, re.IGNORECASE):
            surah_name = match.group(1).strip().lower()
            ayah = int(match.group(2))
            
            # Try to find surah number from name
            surah_num = self._surah_name_to_number(surah_name)
            if surah_num:
                references.append({
                    "surah": surah_num,
                    "ayah": ayah,
                    "match_text": match.group(0)
                })
        
        # Pattern 3: "Surah 2 verse 255"
        pattern3 = r'(?:surah|surat)\s+(\d+)\s+(?:verse|ayah|aya)\s+(\d+)'
        for match in re.finditer(pattern3, text, re.IGNORECASE):
            surah = int(match.group(1))
            ayah = int(match.group(2))
            if 1 <= surah <= 114 and ayah > 0:
                references.append({
                    "surah": surah,
                    "ayah": ayah,
                    "match_text": match.group(0)
                })
        
        # Remove duplicates (same surah:ayah)
        unique_refs = []
        seen = set()
        for ref in references:
            key = (ref["surah"], ref["ayah"])
            if key not in seen:
                seen.add(key)
                unique_refs.append(ref)
        
        return unique_refs
    
    def _surah_name_to_number(self, name: str) -> Optional[int]:
        """Convert surah name to number"""
        name_lower = name.lower().strip()
        
        # Check direct mapping
        if name_lower in self.SURAH_NAMES:
            return self.SURAH_NAMES[name_lower]
        
        # Try partial matches
        for surah_name, surah_num in self.SURAH_NAMES.items():
            if surah_name in name_lower or name_lower in surah_name:
                return surah_num
        
        return None
    
    def verify_verse(self, surah: int, ayah: int) -> Dict:
        """
        Verify a Quranic verse by fetching it from AlQuran Cloud API
        
        Args:
            surah: Surah number (1-114)
            ayah: Ayah number
        
        Returns:
            Dictionary with verse data or error
        """
        if not (1 <= surah <= 114):
            return {
                "error": f"Invalid surah number: {surah}. Must be between 1 and 114.",
                "valid": False
            }
        
        try:
            # Fetch the verse
            url = f"{self.BASE_URL}/ayah/{surah}:{ayah}/en.asad"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                return {
                    "error": f"Ayah {ayah} not found in Surah {surah}",
                    "valid": False
                }
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 200:
                return {
                    "error": data.get("status", "Unknown error"),
                    "valid": False
                }
            
            verse_data = data.get("data", {})
            
            # Fetch Arabic text
            arabic_url = f"{self.BASE_URL}/ayah/{surah}:{ayah}"
            arabic_response = requests.get(arabic_url, timeout=10)
            arabic_text = ""
            if arabic_response.status_code == 200:
                arabic_data = arabic_response.json()
                if arabic_data.get("code") == 200:
                    arabic_text = arabic_data.get("data", {}).get("text", "")
            
            # Fetch surah info
            surah_url = f"{self.BASE_URL}/surah/{surah}"
            surah_response = requests.get(surah_url, timeout=10)
            surah_name = f"Surah {surah}"
            if surah_response.status_code == 200:
                surah_data = surah_response.json()
                if surah_data.get("code") == 200:
                    surah_info = surah_data.get("data", {})
                    surah_name = surah_info.get("englishName", f"Surah {surah}")
            
            return {
                "valid": True,
                "surah": surah,
                "ayah": ayah,
                "surah_name": surah_name,
                "arabic_text": arabic_text,
                "translation": verse_data.get("text", ""),
                "number": verse_data.get("number", ayah),
                "numberInSurah": verse_data.get("numberInSurah", ayah)
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Error fetching verse: {str(e)}",
                "valid": False
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "valid": False
            }
    
    def verify_claim(self, claim: str) -> Dict:
        """
        Verify a claim for Quranic content
        
        Args:
            claim: The claim text to verify
        
        Returns:
            Dictionary with verification results
        """
        references = self.extract_quran_references(claim)
        
        if not references:
            return {
                "has_quran_reference": False,
                "quran_verses": []
            }
        
        verified_verses = []
        errors = []
        
        for ref in references:
            result = self.verify_verse(ref["surah"], ref["ayah"])
            
            if result.get("valid"):
                verified_verses.append(result)
            else:
                errors.append({
                    "surah": ref["surah"],
                    "ayah": ref["ayah"],
                    "error": result.get("error", "Unknown error")
                })
        
        return {
            "has_quran_reference": True,
            "quran_verses": verified_verses,
            "errors": errors if errors else None
        }

