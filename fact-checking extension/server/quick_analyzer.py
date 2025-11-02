import re
from typing import Dict, Optional, List
from islamic_verification.fabricated_hadith_detector import FabricatedHadithDetector
from islamic_verification.quran_verifier import QuranVerifier
from islamic_verification.hadith_verifier import HadithVerifier


class QuickAnalyzer:
    
    def __init__(self):
        self.fabricated_detector = FabricatedHadithDetector()
        self.quran_verifier = QuranVerifier()
        self.hadith_verifier = HadithVerifier()
        
        self.high_confidence_fabricated = [
            r'\b(seek\s+knowledge.*china)\b',
            r'\b(love.*country.*part.*faith)\b',
            r'\b(difference.*opinion.*mercy.*ummah)\b',
            r'\b(companions.*stars.*follow.*any)\b',
        ]
        
        self.hadith_narration_patterns = [
            r'\b(abu|ibn|bin|bint|umar|ali|aisha|abdullah|abdurrahman)\s+\w+.*(narrated|reported|said)\b',
            r'\b(narrated|reported|transmitted).*(abu|ibn|bin|bint)\s+\w+\b',
            r'\b(sahih|authentic).*(bukhari|muslim|tirmidhi|abu\s+dawud|ibn\s+majah)\b',
        ]
        
        self.factual_claim_patterns = [
            r'\b(prophet|messenger|rasul|muhammad).*(said|stated|taught|commanded|forbade|mentioned)\b',
            r'\b(allah|god).*(said|revealed|commanded|forbade)\b',
            r'\b(according\s+to|in|from).*(hadith|sunnah|quran|islam)\b',
            r'\b(it\s+is\s+obligatory|it\s+is\s+forbidden|halal|haram|wajib|mustahabb)\b',
        ]
        
        self.inaccuracy_red_flags = [
            r'\b(quran.*says|quran.*states).*(but|however|actually|really)\b',
            r'\b(prophet.*never|prophet.*did\s+not|prophet.*didnt)\b',
            r'\b(false.*hadith|fake.*hadith|wrong.*hadith|incorrect.*hadith)\b',
            r'\b(not\s+in|not\s+found\s+in|doesn\'?t\s+exist\s+in).*(bukhari|muslim|authentic)\b',
        ]
        
        self.islamic_context_keywords = [
            r'\b(prophet|messenger|rasul|muhammad|pbuh)\b',
            r'\b(hadith|sunna|sunnah|ahadith)\b',
            r'\b(quran|qur\'?an|surah|ayah|verse)\b',
            r'\b(allah|god|subhanallah|inshallah|alhamdulillah)\b',
            r'\b(companions|sahaba|sahabah)\b',
        ]
    
    def quick_authenticity_check(self, claim: str) -> Dict:
        claim_lower = claim.lower()
        claim_original = claim.strip()
        
        has_islamic_context = any(
            re.search(pattern, claim_lower, re.IGNORECASE) 
            for pattern in self.islamic_context_keywords
        )
        
        if not has_islamic_context:
            return {
                "verdict": "Not Islamic Content",
                "confidence": 0.9,
                "quick_analysis": "No Islamic keywords detected. Skipping verification.",
                "reasoning": "non_islamic",
                "needs_verification": False
            }
        
        fabrication_result = self.fabricated_detector.detect_fabrication(claim_original)
        if fabrication_result and fabrication_result.get("confidence", 0) >= 0.90:
            return {
                "verdict": "Likely Inaccurate",
                "confidence": fabrication_result.get("confidence", 0.90),
                "quick_analysis": fabrication_result.get("warning", "Matches known fabricated hadith pattern."),
                "reasoning": "very_high_confidence_fabrication",
                "needs_verification": True,
                "issue_type": "fabricated_hadith"
            }
        
        inaccuracy_flags = sum(
            1 for pattern in self.inaccuracy_red_flags 
            if re.search(pattern, claim_lower, re.IGNORECASE)
        )
        
        if inaccuracy_flags >= 4:
            return {
                "verdict": "Possible Inaccuracy",
                "confidence": 0.75,
                "quick_analysis": f"Contains {inaccuracy_flags} strong red flags suggesting factual inaccuracies. Comprehensive verification strongly recommended.",
                "reasoning": "multiple_inaccuracy_flags",
                "needs_verification": True,
                "issue_type": "factual_inaccuracy"
            }
        
        quran_refs = self.quran_verifier.extract_quran_references(claim_original)
        has_quran_ref = len(quran_refs) > 0
        
        has_hadith_keywords = self.hadith_verifier.detect_hadith_claim(claim_original)
        has_hadith_structure = any(
            re.search(pattern, claim_lower, re.IGNORECASE) 
            for pattern in self.hadith_narration_patterns
        )
        
        factual_claims = sum(
            1 for pattern in self.factual_claim_patterns 
            if re.search(pattern, claim_lower, re.IGNORECASE)
        )
        
        needs_verification = False
        issue_type = None
        confidence = 0.5
        
        
        if needs_verification:
            if confidence >= 0.90:
                verdict = "Likely Inaccurate"
            elif confidence >= 0.75:
                verdict = "Possible Inaccuracy"
            else:
                verdict = "Requires Comprehensive Check"
        elif has_quran_ref:
            verdict = "Quran Reference Found"
            confidence = 0.8
        elif has_hadith_structure:
            verdict = "Proper Hadith Structure"
            confidence = 0.7
        else:
            verdict = "Requires Comprehensive Check"
            confidence = 0.5
        
        explanation_parts = []
        
        if needs_verification:
            if issue_type == "fabricated_hadith":
                explanation_parts.append("Matches pattern of known fabricated hadiths")
            elif issue_type == "factual_inaccuracy":
                explanation_parts.append("Contains indicators of factual inaccuracies")
            elif issue_type == "unstructured_hadith_claim":
                explanation_parts.append("Hadith claim lacks proper narration structure")
            
            explanation_parts.append("Comprehensive verification recommended")
        
        if has_quran_ref:
            explanation_parts.append(f"Contains {len(quran_refs)} Quran reference(s)")
        
        if has_hadith_structure:
            explanation_parts.append("Proper Hadith narration structure detected")
        
        if factual_claims > 0:
            explanation_parts.append(f"Contains {factual_claims} factual claim(s) requiring verification")
        
        if not explanation_parts:
            explanation_parts.append("Islamic content detected. Comprehensive verification in progress.")
        
        quick_analysis = ". ".join(explanation_parts) + "."
        
        reasoning_parts = []
        if has_quran_ref:
            reasoning_parts.append("quran_ref")
        if has_hadith_keywords:
            reasoning_parts.append("hadith_claim")
        if has_hadith_structure:
            reasoning_parts.append("proper_structure")
        if factual_claims > 0:
            reasoning_parts.append(f"factual_claims({factual_claims})")
        if inaccuracy_flags > 0:
            reasoning_parts.append(f"red_flags({inaccuracy_flags})")
        
        return {
            "verdict": verdict,
            "confidence": round(confidence, 2),
            "quick_analysis": quick_analysis,
            "reasoning": "_".join(reasoning_parts) if reasoning_parts else "islamic_content",
            "needs_verification": needs_verification,
            "issue_type": issue_type,
            "indicators": {
                "quran_reference": has_quran_ref,
                "quran_refs_count": len(quran_refs),
                "hadith_keywords": has_hadith_keywords,
                "hadith_structure": has_hadith_structure,
                "factual_claims": factual_claims,
                "inaccuracy_flags": inaccuracy_flags,
                "is_islamic_content": True
            }
        }
