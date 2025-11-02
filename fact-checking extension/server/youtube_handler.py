"""
YouTube Transcript Handler
Extracts and processes YouTube video transcripts
"""
import re
from typing import Dict, List, Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


class YouTubeHandler:
    """Handles YouTube video transcript extraction and processing"""
    
    # Islamic keywords for filtering relevant claims
    ISLAMIC_KEYWORDS = [
        "allah", "god", "islam", "islamic", "muslim", "quran", "koran", "hadith",
        "hadis", "prophet", "muhammad", "pbuh", "saw", "rasul", "messenger",
        "surah", "ayah", "verse", "bukhari", "muslim", "sahih", "tirmidhi",
        "abu dawud", "ibn majah", "nasai", "imam", "scholar", "fatwa",
        "halal", "haram", "fiqh", "sunnah", "shariah", "islamic law",
        "ummah", "caliph", "sahabah", "companions", "iman", "faith"
    ]
    
    def __init__(self):
        """Initialize YouTube handler"""
        pass
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract YouTube video ID from various URL formats
        
        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        
        Args:
            url: YouTube URL
        
        Returns:
            Video ID or None if invalid
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_transcript(self, video_id: str, languages: List[str] = None) -> List[Dict]:
        """
        Get transcript for a YouTube video
        
        Args:
            video_id: YouTube video ID
            languages: Preferred languages (default: ['en', 'ar', 'ur'])
        
        Returns:
            List of transcript segments with text and timestamps
        """
        if languages is None:
            languages = ['en', 'ar', 'ur', 'tr', 'id']  # English, Arabic, Urdu, Turkish, Indonesian
        
        try:
            # Try to get transcript in preferred languages
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try each language
            for lang in languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    data = transcript.fetch()
                    return data
                except:
                    continue
            
            # If no preferred language found, try auto-generated
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
                data = transcript.fetch()
                return data
            except:
                pass
            
            # Last resort: get any available transcript
            for transcript in transcript_list:
                data = transcript.fetch()
                return data
            
            return []
            
        except TranscriptsDisabled:
            return []
        except NoTranscriptFound:
            return []
        except Exception as e:
            print(f"Error getting transcript: {e}")
            return []
    
    def tokenize_into_claims(self, transcript: List[Dict]) -> List[Tuple[str, float]]:
        """
        Tokenize transcript into individual claims/sentences
        
        Args:
            transcript: List of transcript segments
        
        Returns:
            List of (claim_text, timestamp) tuples
        """
        claims = []
        current_sentence = []
        current_start_time = None
        
        for segment in transcript:
            text = segment.get('text', '').strip()
            start_time = segment.get('start', 0)
            
            if not current_start_time:
                current_start_time = start_time
            
            current_sentence.append(text)
            
            # Check for sentence endings
            if text.endswith(('.', '!', '?', '.', '!', '?')):
                sentence_text = ' '.join(current_sentence).strip()
                if len(sentence_text) > 20:  # Minimum length filter
                    claims.append((sentence_text, current_start_time))
                
                current_sentence = []
                current_start_time = None
        
        # Add remaining sentence
        if current_sentence:
            sentence_text = ' '.join(current_sentence).strip()
            if len(sentence_text) > 20:
                claims.append((sentence_text, current_start_time or 0))
        
        return claims
    
    def filter_islamic_claims(self, claims: List[Tuple[str, float]]) -> List[Tuple[str, float, float]]:
        """
        Filter and rank claims by Islamic relevance
        
        Args:
            claims: List of (claim_text, timestamp) tuples
        
        Returns:
            List of (claim_text, timestamp, relevance_score) tuples, sorted by relevance
        """
        scored_claims = []
        
        for claim_text, timestamp in claims:
            claim_lower = claim_text.lower()
            
            # Calculate relevance score
            relevance = 0.0
            keyword_matches = 0
            
            for keyword in self.ISLAMIC_KEYWORDS:
                if keyword in claim_lower:
                    keyword_matches += 1
                    # More specific keywords get higher weight
                    if keyword in ['quran', 'hadith', 'sahih', 'bukhari', 'muslim']:
                        relevance += 3.0
                    elif keyword in ['prophet', 'muhammad', 'allah', 'islam']:
                        relevance += 2.0
                    else:
                        relevance += 1.0
            
            # Normalize by length (shorter claims with keywords are more relevant)
            if len(claim_text) > 0:
                relevance = relevance / (len(claim_text) / 100)  # Normalize
            
            # Only include if has at least one Islamic keyword
            if keyword_matches > 0:
                scored_claims.append((claim_text, timestamp, relevance))
        
        # Sort by relevance (highest first)
        scored_claims.sort(key=lambda x: x[2], reverse=True)
        
        return scored_claims
    
    def process_video(self, video_url: str, max_claims: int = 10) -> Dict:
        """
        Process a YouTube video and extract Islamic claims
        
        Args:
            video_url: YouTube video URL
            max_claims: Maximum number of claims to return
        
        Returns:
            Dictionary with video info and claims
        """
        video_id = self.extract_video_id(video_url)
        
        if not video_id:
            return {
                "success": False,
                "error": "Invalid YouTube URL or video ID not found"
            }
        
        # Get transcript
        transcript = self.get_transcript(video_id)
        
        if not transcript:
            return {
                "success": False,
                "error": "No transcript available for this video. The video may not have captions enabled."
            }
        
        # Tokenize into claims
        all_claims = self.tokenize_into_claims(transcript)
        
        # Filter for Islamic claims
        islamic_claims = self.filter_islamic_claims(all_claims)
        
        # Limit to top N claims
        top_claims = islamic_claims[:max_claims]
        
        # Format results
        formatted_claims = []
        for claim_text, timestamp, relevance in top_claims:
            formatted_claims.append({
                "text": claim_text,
                "timestamp": timestamp,
                "timestamp_formatted": self._format_timestamp(timestamp),
                "relevance_score": relevance
            })
        
        return {
            "success": True,
            "video_id": video_id,
            "video_url": video_url,
            "total_segments": len(transcript),
            "total_claims": len(all_claims),
            "islamic_claims_found": len(islamic_claims),
            "claims": formatted_claims
        }
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp in MM:SS format"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

