"""
OpenAI AI Provider Implementation
Handles OpenAI API interactions
"""
import json
from typing import Dict, List, Optional
from openai import OpenAI
from .base import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI API provider"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = config.get("model", "gpt-4")
        self.temperature = config.get("temperature", 0.3)
    
    def is_available(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            # Simple check - try to list models
            self.client.models.list()
            return True
        except:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate response using OpenAI API
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
        
        Returns:
            Generated response text
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                response_format={"type": "json_object"}  # Request JSON format
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def fact_check_claim(
        self,
        claim: str,
        evidence: Optional[List[Dict]] = None,
        islamic_context: Optional[Dict] = None
    ) -> Dict:
        """
        Fact-check a claim with Islamic verification context
        
        Args:
            claim: The claim to verify
            evidence: Optional evidence sources
            islamic_context: Optional Islamic verification data
        
        Returns:
            Structured fact-check result
        """
        system_prompt = self.get_islamic_system_prompt()
        
        # Build the prompt with context
        prompt_parts = [f"Claim to verify: \"{claim}\"\n\n"]
        
        if islamic_context:
            prompt_parts.append("ISLAMIC VERIFICATION DATA:\n")
            
            if islamic_context.get("quran_verses"):
                prompt_parts.append("Quranic References Found:\n")
                for verse in islamic_context["quran_verses"]:
                    prompt_parts.append(f"- Surah {verse.get('surah_name')} {verse.get('ayah')}: {verse.get('text')}\n")
            
            if islamic_context.get("hadiths"):
                prompt_parts.append("\nHadith References Found:\n")
                for hadith in islamic_context["hadiths"]:
                    prompt_parts.append(f"- Grade: {hadith.get('grade', 'Unknown')}\n")
                    prompt_parts.append(f"  Text: {hadith.get('text', 'N/A')}\n")
                    if hadith.get("collection"):
                        prompt_parts.append(f"  Collection: {hadith.get('collection')}\n")
            
            if islamic_context.get("is_fabricated"):
                prompt_parts.append("\n⚠️ WARNING: This claim matches patterns of commonly fabricated hadiths!\n")
            
            if islamic_context.get("fiqh_rulings"):
                prompt_parts.append("\nFiqh Rulings Found:\n")
                for ruling in islamic_context["fiqh_rulings"]:
                    prompt_parts.append(f"- {ruling}\n")
            
            prompt_parts.append("\n")
        
        if evidence:
            prompt_parts.append("ADDITIONAL EVIDENCE FROM WEB SEARCH:\n")
            for i, source in enumerate(evidence[:5], 1):  # Limit to top 5
                prompt_parts.append(f"\nSource {i} ({source.get('domain', 'Unknown')}):\n")
                prompt_parts.append(f"{source.get('content', '')}\n")
        
        prompt_parts.append("\n\nAnalyze this claim using the provided Islamic verification data and evidence. Return your analysis as a JSON object with the structure specified in the system prompt.")
        
        prompt = "".join(prompt_parts)
        
        try:
            response_text = self.generate_response(prompt, system_prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response_text)
                
                # Ensure all required fields are present
                return {
                    "verdict": result.get("verdict", "Unable to Verify"),
                    "confidence": float(result.get("confidence", 0.5)),
                    "grade": result.get("grade"),
                    "explanation": result.get("explanation", "No explanation provided"),
                    "sources": result.get("sources", []),
                    "warnings": result.get("warnings", [])
                }
            except json.JSONDecodeError:
                return {
                    "verdict": "Unable to Verify",
                    "confidence": 0.3,
                    "grade": None,
                    "explanation": f"Could not parse AI response as JSON. Raw response: {response_text[:500]}",
                    "sources": [],
                    "warnings": ["AI response format error"]
                }
        except Exception as e:
            return {
                "verdict": "Unable to Verify",
                "confidence": 0.0,
                "grade": None,
                "explanation": f"Error during AI analysis: {str(e)}",
                "sources": [],
                "warnings": [f"AI provider error: {str(e)}"]
            }

