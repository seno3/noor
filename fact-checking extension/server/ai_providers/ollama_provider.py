"""
Ollama AI Provider Implementation
Handles local Ollama model interactions
"""
import requests
import json
import time
from typing import Dict, List, Optional
from .base import AIProvider


class OllamaProvider(AIProvider):
    """Ollama local AI provider"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", "mistral")
        self.temperature = config.get("temperature", 0.3)
        self.api_url = f"{self.base_url}/api/chat"
    
    def is_available(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate response using Ollama API
        
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
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature
                    }
                },
                timeout=120
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Ollama API returns response in 'message.content' or directly as 'response'
            if "message" in data and "content" in data["message"]:
                return data["message"]["content"]
            elif "response" in data:
                return data["response"]
            elif "content" in data:
                return data["content"]
            else:
                # Fallback: try to get any text content
                content = str(data)
                print(f"⚠️ Unexpected Ollama response format: {data.keys()}")
                return content
        except requests.exceptions.Timeout:
            raise Exception(f"Ollama API timeout after 120 seconds. Is Ollama running? Try: ollama serve")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Cannot connect to Ollama at {self.base_url}. Make sure Ollama is running: ollama serve")
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
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
        
        prompt_parts.append("\n\nAnalyze this claim using the provided Islamic verification data and evidence. Return your analysis in the JSON format specified in the system prompt.")
        
        prompt = "".join(prompt_parts)
        
        try:
            response_text = self.generate_response(prompt, system_prompt)
            
            # Try to parse JSON response
            try:
                # Extract JSON from response if wrapped in markdown code blocks
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif "```" in response_text:
                    json_start = response_text.find("```") + 3
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                
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
                # If JSON parsing fails, try to extract information from text
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

