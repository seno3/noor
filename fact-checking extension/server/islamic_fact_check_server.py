from duckduckgo_search import DDGS
from typing import Dict, List, Optional
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from ai_providers import create_ai_provider
from islamic_verification import IslamicVerificationEngine
from youtube_handler import YouTubeHandler
from islamic_verification.source_credibility import SourceCredibilityRegistry
from cache import get_cache
from quick_analyzer import QuickAnalyzer
from task_manager import get_task_manager
import asyncio


class IslamicFactChecker:
    
    def __init__(self):
        is_valid, errors = Config.validate()
        if not is_valid:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        print(f"Initializing AI provider: {Config.AI_PROVIDER}")
        self.ai_provider = create_ai_provider()
        
        if not self.ai_provider.is_available():
            raise RuntimeError(f"AI provider {Config.AI_PROVIDER} is not available. Please check configuration.")
        
        self.islamic_engine = IslamicVerificationEngine()
        
        self.youtube_handler = YouTubeHandler()
        
        self.source_registry = SourceCredibilityRegistry()
        
        self.search_engine = DDGS()
        
        print("Loading sentence transformer model...")
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.quick_analyzer = QuickAnalyzer()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.blacklisted_domains = {
            'reddit.com', 'quora.com', 'youtube.com', 'twitter.com', 'x.com',
            'facebook.com', 'instagram.com', 'tiktok.com', 'pinterest.com',
            'tumblr.com', 'medium.com', 'answers.yahoo.com', 'stackoverflow.com',
            'linkedin.com', 'amazon.com', 'ebay.com'
        }
    
    def search_web(self, query: str, prioritize_islamic: bool = True) -> List[Dict]:
        all_results = []
        
        if prioritize_islamic:
            islamic_domains = [
                "site:sunnah.com",
                "site:islamqa.info",
                "site:islamqa.org",
                "site:yaqeeninstitute.org",
                "site:quran.com",
                "site:seekersguidance.org"
            ]
            
            for domain_query in islamic_domains[:3]:
                try:
                    results = list(self.search_engine.text(
                        f"{domain_query} {query}",
                        max_results=2
                    ))
                    all_results.extend(results)
                    time.sleep(0.5)
                except:
                    continue
        
        try:
            regular_results = list(self.search_engine.text(
                query,
                max_results=5
            ))
            all_results.extend(regular_results)
        except:
            pass
        
        scored_results = []
        for result in all_results:
            url = result.get('link') or result.get('href')
            if url:
                credibility = self.source_registry.get_credibility_score(url)
                scored_results.append((result, credibility))
        
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        return [result for result, _ in scored_results[:10]]
    
    def _extract_text_from_url(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            content = ""
            main_content = soup.find(['article', 'main'])
            if main_content:
                content = main_content.get_text(strip=True, separator=' ')
            
            if not content:
                paragraphs = soup.find_all('p')
                content = ' '.join(p.get_text(strip=True) for p in paragraphs)
            
            if not content and soup.body:
                content = soup.body.get_text(strip=True, separator=' ')
            
            content = re.sub(r'\s+', ' ', content).strip()
            return content[:8000] if content else ""
        except:
            return ""
    
    def _summarize_content(self, statement: str, content: str, max_sentences: int = 5) -> str:
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        if not sentences:
            return content
        
        statement_embedding = self.sentence_transformer.encode([statement], show_progress_bar=False)
        sentence_embeddings = self.sentence_transformer.encode(sentences, show_progress_bar=False)
        similarities = cosine_similarity(statement_embedding, sentence_embeddings)[0]
        top_indices = np.argsort(similarities)[-max_sentences:]
        relevant_sentences = [sentences[i] for i in sorted(top_indices)]
        return '. '.join(relevant_sentences) + '.'
    
    def check_islamic_claim(self, claim: str, claim_type: Optional[str] = None) -> Dict:
        print(f"\n{'='*60}")
        print(f"Verifying claim: {claim}")
        print(f"{'='*60}")
        
        cache = get_cache()
        cached_result = cache.get(claim)
        if cached_result:
            print("✓ Using cached result")
            return cached_result
        
        print("\n[1/4] Running Islamic verification...")
        islamic_results = self.islamic_engine.verify_claim(claim)
        islamic_context = islamic_results.get("islamic_context", {})
        
        print("\n[2/4] Searching web for additional evidence...")
        search_results = self.search_web(claim, prioritize_islamic=True)
        
        print("\n[3/4] Processing sources...")
        evidence_sources = []
        processed_domains = set()
        
        for result in search_results[:5]:
            url = result.get('link') or result.get('href')
            if not url:
                continue
            
            domain = urlparse(url).netloc
            if domain in processed_domains:
                continue
            
            processed_domains.add(domain)
            content = self._extract_text_from_url(url)
            
            if content and len(content.strip()) > 100:
                summarized = self._summarize_content(claim, content)
                credibility = self.source_registry.get_credibility_score(url)
                
                evidence_sources.append({
                    "url": url,
                    "domain": domain,
                    "content": summarized,
                    "title": result.get('title', ''),
                    "credibility": credibility
                })
        
        print("\n[4/4] Running AI analysis...")
        ai_result = self.ai_provider.fact_check_claim(
            claim=claim,
            evidence=evidence_sources,
            islamic_context=islamic_context
        )
        
        result = {
            "claim": claim,
            "verdict": ai_result.get("verdict", "Unable to Verify"),
            "confidence": ai_result.get("confidence", 0.5),
            "grade": ai_result.get("grade"),
            "explanation": ai_result.get("explanation", ""),
            "islamic_verification": {
                "quran_verses": islamic_results.get("quran_verification", {}).get("quran_verses", []),
                "hadiths": islamic_results.get("hadith_verification", {}).get("hadiths", []),
                "is_fabricated": islamic_results.get("fabricated_detection", {}).get("is_fabricated", False),
                "fabrication_details": islamic_results.get("fabricated_detection", {}).get("fabrication_details"),
                "fiqh_rulings": islamic_results.get("fiqh_verification", {}).get("fiqh_rulings", [])
            },
            "sources": [
                {
                    "url": src.get("url"),
                    "domain": src.get("domain"),
                    "credibility": src.get("credibility"),
                    "title": src.get("title")
                }
                for src in evidence_sources
            ],
            "warnings": ai_result.get("warnings", [])
        }
        
        if islamic_results.get("fabricated_detection", {}).get("warnings"):
            result["warnings"].extend(islamic_results["fabricated_detection"]["warnings"])
        
        print(f"\n✓ Verification complete. Verdict: {result['verdict']}")
        
        cache.set(claim, result)
        
        return result
    
    def check_youtube_video(self, video_url: str) -> Dict:
        print(f"\nProcessing YouTube video: {video_url}")
        
        video_result = self.youtube_handler.process_video(
            video_url,
            max_claims=Config.MAX_CLAIMS_PER_VIDEO
        )
        
        if not video_result.get("success"):
            return video_result
        
        verified_claims = []
        claims = video_result.get("claims", [])
        
        for i, claim_data in enumerate(claims, 1):
            print(f"\nVerifying claim {i}/{len(claims)}: {claim_data['text'][:50]}...")
            claim_text = claim_data["text"]
            
            verification_result = self.check_islamic_claim(claim_text)
            
            verified_claims.append({
                "claim": claim_text,
                "timestamp": claim_data["timestamp"],
                "timestamp_formatted": claim_data["timestamp_formatted"],
                "verification": verification_result
            })
        
        return {
            "success": True,
            "video_id": video_result.get("video_id"),
            "video_url": video_url,
            "total_claims_processed": len(claims),
            "verified_claims": verified_claims
        }


app = FastAPI(title="Islamic Truth Verifier", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8004", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    import datetime
    start_time = time.time()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if request.url.path not in ["/health", "/docs", "/openapi.json"]:
        print(f"[{timestamp}] {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        elapsed = time.time() - start_time
        
        if elapsed > 1.0 or response.status_code >= 400:
            print(f"   → {response.status_code} in {elapsed:.3f}s")
        
        return response
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"   ❌ Error after {elapsed:.3f}s: {e}")
        raise


try:
    checker = IslamicFactChecker()
    print("✓ Islamic Truth Verifier initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize: {e}")
    checker = None


class ClaimRequest(BaseModel):
    claim: str
    claim_type: Optional[str] = None


class YouTubeRequest(BaseModel):
    video_url: str


@app.get("/health")
async def health_check():
    print(f"\n🏥 HEALTH CHECK ENDPOINT CALLED")
    print(f"   Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if checker is None:
        print("   ❌ Service not initialized")
        return {"status": "error", "message": "Service not initialized"}
    
    ai_status = checker.ai_provider.is_available()
    print(f"   🤖 AI Provider: {Config.AI_PROVIDER}")
    print(f"   ✅ AI Available: {ai_status}")
    print(f"   📊 Status: {'healthy' if ai_status else 'degraded'}")
    print(f"   🔍 Islamic Verification Enabled: {Config.ENABLE_ISLAMIC_VERIFICATION}")
    
    result = {
        "status": "healthy" if ai_status else "degraded",
        "ai_provider": Config.AI_PROVIDER,
        "ai_available": ai_status,
        "islamic_verification_enabled": Config.ENABLE_ISLAMIC_VERIFICATION
    }
    
    print(f"   📤 Returning: {json.dumps(result, indent=2)}")
    return result


async def run_comprehensive_analysis(task_id: str, claim: str, claim_type: Optional[str]):
    task_manager = get_task_manager()
    task_manager.update_task(task_id, status="processing")
    
    try:
        print(f"\n[BACKGROUND TASK {task_id}] Starting comprehensive analysis...")
        result = checker.check_islamic_claim(claim, claim_type)
        task_manager.update_task(task_id, result=result)
        print(f"[BACKGROUND TASK {task_id}] ✅ Comprehensive analysis completed")
    except Exception as e:
        error_msg = str(e)
        print(f"[BACKGROUND TASK {task_id}] ❌ Error: {error_msg}")
        task_manager.update_task(task_id, error=error_msg)


@app.post("/check-islamic-claim-quick")
async def check_islamic_claim_quick_endpoint(request: ClaimRequest):
    import time
    start_time = time.time()
    
    try:
        if checker is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        if not request.claim.strip():
            raise HTTPException(status_code=400, detail="Claim cannot be empty")
        
        quick_start = time.time()
        quick_result = checker.quick_analyzer.quick_authenticity_check(request.claim)
        quick_time = time.time() - quick_start
        
        if quick_result.get("verdict") == "Not Islamic Content":
            return {
                "quick_result": {
                    "verdict": "Not Islamic Content",
                    "confidence": quick_result["confidence"],
                    "quick_analysis": "No Islamic content detected. Skipping verification.",
                    "reasoning": "non_islamic",
                    "skip_processing": True
                },
                "task_id": None,
                "status": "skipped",
                "message": "Non-Islamic content - no verification needed."
            }
        
        task_start = time.time()
        task_manager = get_task_manager()
        task_id = task_manager.create_task(request.claim)
        task_time = time.time() - task_start
        
        try:
            asyncio.create_task(run_comprehensive_analysis(task_id, request.claim, request.claim_type))
        except Exception as bg_error:
            print(f"⚠️ Background task creation failed (non-critical): {bg_error}")
        
        total_time = time.time() - start_time
        
        result = {
            "quick_result": {
                "verdict": quick_result["verdict"],
                "confidence": quick_result["confidence"],
                "quick_analysis": quick_result["quick_analysis"],
                "reasoning": quick_result.get("reasoning", "")
            },
            "task_id": task_id,
            "status": "quick_complete",
            "message": "Quick analysis complete. Comprehensive analysis in progress."
        }
        
        print(f"⚡ Quick check completed in {total_time:.3f}s (analysis: {quick_time:.3f}s, task: {task_time:.3f}s)")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Error in quick check after {elapsed:.3f}s: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/check-islamic-claim-result/{task_id}")
async def get_comprehensive_result_endpoint(task_id: str):
    print(f"\n{'='*60}")
    print(f"🔍 /check-islamic-claim-result/{task_id} ENDPOINT CALLED")
    print(f"{'='*60}")
    
    task_manager = get_task_manager()
    task = task_manager.get_task(task_id)
    
    if not task:
        print(f"   ❌ Task not found: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found")
    
    status = task.get("status")
    
    if status == "completed":
        result = task.get("result")
        print(f"   ✅ Task completed, returning comprehensive result")
        print(f"   📊 Verdict: {result.get('verdict', 'Unknown')}")
        print(f"{'='*60}\n")
        return {
            "status": "completed",
            "result": result,
            "task_id": task_id
        }
    elif status == "error":
        error = task.get("error", "Unknown error")
        print(f"   ❌ Task failed: {error}")
        print(f"{'='*60}\n")
        return {
            "status": "error",
            "error": error,
            "task_id": task_id
        }
    else:
        print(f"   ⏳ Task still processing (status: {status})")
        print(f"{'='*60}\n")
        return {
            "status": "processing",
            "message": "Comprehensive analysis in progress...",
            "task_id": task_id
        }


@app.post("/check-islamic-claim")
async def check_islamic_claim_endpoint(request: ClaimRequest):
    print(f"\n{'='*60}")
    print(f"🔍 /check-islamic-claim ENDPOINT CALLED")
    print(f"{'='*60}")
    print(f"📝 Claim: {request.claim[:200]}{'...' if len(request.claim) > 200 else ''}")
    print(f"📏 Claim length: {len(request.claim)} characters")
    print(f"🏷️  Claim type: {request.claim_type or 'Auto-detect'}")
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if checker is None:
        print("   ❌ ERROR: Service not initialized!")
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    if not request.claim.strip():
        print("   ❌ ERROR: Empty claim!")
        raise HTTPException(status_code=400, detail="Claim cannot be empty")
    
    try:
        print(f"   ✅ Starting verification process...")
        result = checker.check_islamic_claim(request.claim, request.claim_type)
        
        print(f"\n   📊 VERIFICATION RESULT:")
        print(f"      Verdict: {result.get('verdict', 'Unknown')}")
        print(f"      Confidence: {result.get('confidence', 0):.2%}")
        print(f"      Grade: {result.get('grade', 'N/A')}")
        
        if result.get('islamic_verification'):
            iv = result['islamic_verification']
            print(f"      Quran verses found: {len(iv.get('quran_verses', []))}")
            print(f"      Hadiths found: {len(iv.get('hadiths', []))}")
            print(f"      Is fabricated: {iv.get('is_fabricated', False)}")
        
        print(f"      Warnings: {len(result.get('warnings', []))}")
        print(f"      Sources: {len(result.get('sources', []))}")
        
        print(f"   ✅ Verification complete!")
        print(f"{'='*60}\n")
        
        return result
    except Exception as e:
        print(f"\n   ❌ EXCEPTION OCCURRED:")
        print(f"      Error: {str(e)}")
        print(f"      Type: {type(e).__name__}")
        import traceback
        print(f"\n   📜 Full traceback:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check-youtube-video")
async def check_youtube_video_endpoint(request: YouTubeRequest):
    if checker is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    if not request.video_url.strip():
        raise HTTPException(status_code=400, detail="Video URL cannot be empty")
    
    try:
        result = checker.check_youtube_video(request.video_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check")
async def check_statement_legacy(request: ClaimRequest):
    print(f"\n{'='*60}")
    print(f"🔄 /check (LEGACY) ENDPOINT CALLED")
    print(f"{'='*60}")
    print(f"📝 Claim: {request.claim[:200]}{'...' if len(request.claim) > 200 else ''}")
    print(f"📏 Claim length: {len(request.claim)} characters")
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if checker is None:
        print("   ❌ ERROR: Service not initialized!")
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        print(f"   ✅ Processing via legacy endpoint...")
        result = checker.check_islamic_claim(request.claim, request.claim_type)
        
        legacy_result = {
            "statement": result["claim"],
            "result": result["verdict"],
            "explanation": result["explanation"]
        }
        
        print(f"   📊 LEGACY RESULT:")
        print(f"      Result: {legacy_result['result']}")
        print(f"      Explanation length: {len(legacy_result['explanation'])} chars")
        print(f"   ✅ Legacy conversion complete!")
        print(f"{'='*60}\n")
        
        return legacy_result
    except Exception as e:
        print(f"\n   ❌ EXCEPTION OCCURRED:")
        print(f"      Error: {str(e)}")
        print(f"      Type: {type(e).__name__}")
        import traceback
        print(f"\n   📜 Full traceback:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Islamic Truth Verifier Server")
    print("="*60)
    print(f"AI Provider: {Config.AI_PROVIDER}")
    print(f"Server starting on http://0.0.0.0:8004")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8004)

