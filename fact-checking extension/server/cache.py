"""
Simple caching system for verified claims
Can be replaced with a proper database later
"""
import json
import os
from typing import Dict, Optional
from datetime import datetime, timedelta
from config import Config


class ClaimCache:
    """Simple file-based cache for verified claims"""
    
    def __init__(self, cache_file: str = "claim_cache.json"):
        """Initialize cache"""
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.duration_days = Config.CACHE_DURATION_DAYS
    
    def _load_cache(self) -> Dict:
        """Load cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    def _is_expired(self, timestamp: str) -> bool:
        """Check if cache entry is expired"""
        try:
            cached_time = datetime.fromisoformat(timestamp)
            expiry = cached_time + timedelta(days=self.duration_days)
            return datetime.now() > expiry
        except:
            return True
    
    def get(self, claim: str) -> Optional[Dict]:
        """
        Get cached result for a claim
        
        Args:
            claim: The claim text
        
        Returns:
            Cached result if found and not expired, None otherwise
        """
        if not Config.ENABLE_CACHING:
            return None
        
        claim_key = claim.lower().strip()
        
        if claim_key in self.cache:
            entry = self.cache[claim_key]
            
            # Check expiration
            if self._is_expired(entry.get("timestamp", "")):
                # Remove expired entry
                del self.cache[claim_key]
                self._save_cache()
                return None
            
            return entry.get("result")
        
        return None
    
    def set(self, claim: str, result: Dict):
        """
        Cache a verification result
        
        Args:
            claim: The claim text
            result: Verification result to cache
        """
        if not Config.ENABLE_CACHING:
            return
        
        claim_key = claim.lower().strip()
        
        self.cache[claim_key] = {
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        
        self._save_cache()
    
    def clear(self):
        """Clear all cache entries"""
        self.cache = {}
        self._save_cache()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = len(self.cache)
        expired = sum(1 for entry in self.cache.values() 
                     if self._is_expired(entry.get("timestamp", "")))
        valid = total - expired
        
        return {
            "total_entries": total,
            "valid_entries": valid,
            "expired_entries": expired,
            "cache_duration_days": self.duration_days
        }


# Global cache instance
_cache_instance: Optional[ClaimCache] = None


def get_cache() -> ClaimCache:
    """Get global cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = ClaimCache()
    return _cache_instance

