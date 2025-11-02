"""
Task Manager for Background Comprehensive Analysis
Tracks async fact-checking tasks and their results
"""
import uuid
import time
from typing import Dict, Optional
from datetime import datetime, timedelta
import threading


class TaskManager:
    """Manages background comprehensive analysis tasks"""
    
    def __init__(self, cleanup_interval: int = 300):
        """
        Initialize task manager
        
        Args:
            cleanup_interval: Seconds between cleanup runs (default 5 minutes)
        """
        self.tasks: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()
        
        # Start cleanup thread
        self._start_cleanup_thread()
    
    def create_task(self, claim: str) -> str:
        """
        Create a new task for comprehensive analysis
        
        Args:
            claim: The claim text being analyzed
        
        Returns:
            Task ID string
        """
        task_id = str(uuid.uuid4())
        
        with self.lock:
            self.tasks[task_id] = {
                "task_id": task_id,
                "claim": claim,
                "status": "pending",
                "created_at": time.time(),
                "result": None,
                "error": None
            }
        
        return task_id
    
    def update_task(self, task_id: str, status: str = None, result: Dict = None, error: str = None):
        """
        Update task status and results
        
        Args:
            task_id: Task ID to update
            status: New status (pending, processing, completed, error)
            result: Comprehensive analysis result
            error: Error message if failed
        """
        with self.lock:
            if task_id in self.tasks:
                if status:
                    self.tasks[task_id]["status"] = status
                if result:
                    self.tasks[task_id]["result"] = result
                    self.tasks[task_id]["status"] = "completed"
                if error:
                    self.tasks[task_id]["error"] = error
                    self.tasks[task_id]["status"] = "error"
                    self.tasks[task_id]["completed_at"] = time.time()
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """
        Get task information
        
        Args:
            task_id: Task ID to retrieve
        
        Returns:
            Task dictionary or None if not found
        """
        with self.lock:
            return self.tasks.get(task_id)
    
    def get_result(self, task_id: str) -> Optional[Dict]:
        """
        Get completed task result
        
        Args:
            task_id: Task ID to retrieve result for
        
        Returns:
            Result dictionary if completed, None otherwise
        """
        task = self.get_task(task_id)
        if task and task["status"] == "completed":
            return task.get("result")
        return None
    
    def is_complete(self, task_id: str) -> bool:
        """
        Check if task is completed
        
        Args:
            task_id: Task ID to check
        
        Returns:
            True if completed, False otherwise
        """
        task = self.get_task(task_id)
        return task is not None and task["status"] in ["completed", "error"]
    
    def _cleanup_old_tasks(self):
        """Remove tasks older than 5 minutes"""
        current_time = time.time()
        cutoff_time = current_time - 300  # 5 minutes
        
        with self.lock:
            to_remove = [
                task_id for task_id, task_data in self.tasks.items()
                if task_data.get("created_at", 0) < cutoff_time
            ]
            
            for task_id in to_remove:
                del self.tasks[task_id]
            
            if to_remove:
                print(f"Cleaned up {len(to_remove)} old task(s)")
    
    def _start_cleanup_thread(self):
        """Start background thread for periodic cleanup"""
        def cleanup_loop():
            while True:
                time.sleep(self.cleanup_interval)
                self._cleanup_old_tasks()
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()
    
    def cleanup_now(self):
        """Manually trigger cleanup"""
        self._cleanup_old_tasks()


# Global task manager instance
_task_manager_instance: Optional[TaskManager] = None


def get_task_manager() -> TaskManager:
    """Get global task manager instance"""
    global _task_manager_instance
    if _task_manager_instance is None:
        _task_manager_instance = TaskManager()
    return _task_manager_instance
