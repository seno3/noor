"""
Islamic Verification Engine
Main entry point for all Islamic verification modules
"""
from .quran_verifier import QuranVerifier
from .hadith_verifier import HadithVerifier
from .fabricated_hadith_detector import FabricatedHadithDetector
from .fiqh_verifier import FiqhVerifier
from .source_credibility import SourceCredibilityRegistry


class IslamicVerificationEngine:
    """Main Islamic verification engine that coordinates all modules"""
    
    def __init__(self):
        """Initialize all verification modules"""
        self.quran_verifier = QuranVerifier()
        self.hadith_verifier = HadithVerifier()
        self.fabricated_detector = FabricatedHadithDetector()
        self.fiqh_verifier = FiqhVerifier()
        self.source_registry = SourceCredibilityRegistry()
    
    def verify_claim(self, claim: str) -> dict:
        """
        Comprehensive Islamic verification of a claim
        
        Args:
            claim: The claim text to verify
        
        Returns:
            Comprehensive verification results
        """
        results = {
            "claim": claim,
            "quran_verification": None,
            "hadith_verification": None,
            "fabricated_detection": None,
            "fiqh_verification": None
        }
        
        # Quran verification
        quran_result = self.quran_verifier.verify_claim(claim)
        results["quran_verification"] = quran_result
        
        # Hadith verification
        hadith_result = self.hadith_verifier.verify_claim(claim)
        results["hadith_verification"] = hadith_result
        
        # Fabricated hadith detection
        fabrication_result = self.fabricated_detector.verify_claim(claim)
        results["fabricated_detection"] = fabrication_result
        
        # Fiqh verification
        fiqh_result = self.fiqh_verifier.verify_claim(claim)
        results["fiqh_verification"] = fiqh_result
        
        # Compile Islamic context for AI
        islamic_context = self._compile_islamic_context(results)
        results["islamic_context"] = islamic_context
        
        return results
    
    def _compile_islamic_context(self, results: dict) -> dict:
        """
        Compile Islamic verification data into context for AI
        
        Args:
            results: Full verification results
        
        Returns:
            Compiled context dictionary
        """
        context = {
            "quran_verses": [],
            "hadiths": [],
            "is_fabricated": False,
            "fiqh_rulings": [],
            "warnings": []
        }
        
        # Extract Quran verses
        if results.get("quran_verification", {}).get("has_quran_reference"):
            context["quran_verses"] = results["quran_verification"].get("quran_verses", [])
        
        # Extract Hadiths
        if results.get("hadith_verification", {}).get("is_hadith_related"):
            context["hadiths"] = results["hadith_verification"].get("hadiths", [])
        
        # Check for fabrication
        if results.get("fabricated_detection", {}).get("is_fabricated"):
            context["is_fabricated"] = True
            context["warnings"].extend(
                results["fabricated_detection"].get("warnings", [])
            )
        
        # Extract Fiqh rulings
        if results.get("fiqh_verification", {}).get("is_fiqh_related"):
            context["fiqh_rulings"] = [
                ruling.get("note", "") 
                for ruling in results["fiqh_verification"].get("fiqh_rulings", [])
            ]
            if results["fiqh_verification"].get("detected_madhabs"):
                context["warnings"].append(
                    f"Rulings may vary by madhab: {', '.join(results['fiqh_verification']['detected_madhabs'])}"
                )
        
        return context

