"""
AI Service for routine generation and optimization.

Integrates with OpenAI API to generate optimal daily routines.
"""

from app.config import settings
from typing import List, Dict


class AIService:
    """Service for AI-powered routine generation."""
    
    def __init__(self):
        """Initialize AI service with OpenAI configuration."""
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
    
    async def generate_routine_prompt(self, tasks: List[Dict], start_time: str, end_time: str) -> str:
        """
        Generate a prompt for routine generation.
        
        Args:
            tasks: List of tasks to schedule
            start_time: Preferred start time
            end_time: Preferred end time
            
        Returns:
            Prompt string for OpenAI API
        """
        task_descriptions = "\n".join([
            f"- {task['title']} ({task['duration']} min, Priority: {task.get('priority', 'medium')})"
            for task in tasks
        ])
        
        prompt = f"""Create an optimized daily routine schedule with the following tasks:

{task_descriptions}

Requirements:
- Working hours: {start_time} to {end_time}
- Include 15-minute breaks between tasks
- Prioritize high-priority tasks in peak energy hours (usually 9-11 AM)
- Group similar tasks together when possible
- Ensure realistic time allocations

Format the response as a JSON array of time blocks with: startTime, endTime, taskName, duration (minutes).
"""
        return prompt
    
    async def parse_routine_response(self, response_text: str) -> List[Dict]:
        """
        Parse OpenAI response into time blocks.
        
        Args:
            response_text: Response from OpenAI API
            
        Returns:
            List of time blocks
        """
        import json
        import re
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                time_blocks = json.loads(json_match.group())
                return time_blocks
        except (json.JSONDecodeError, AttributeError):
            pass
        
        return []
    
    async def calculate_routine_score(self, tasks: List[Dict], time_blocks: List[Dict]) -> float:
        """
        Calculate a quality score for the generated routine.
        
        Args:
            tasks: Original task list
            time_blocks: Generated time blocks
            
        Returns:
            Score between 0 and 100
        """
        score = 85.0  # Base score
        
        # Check if all high-priority tasks are scheduled
        high_priority_tasks = [t for t in tasks if t.get('priority') == 'high']
        scheduled_high_priority = len([
            tb for tb in time_blocks 
            if any(t['title'] in tb.get('title', '') for t in high_priority_tasks)
        ])
        
        if scheduled_high_priority == len(high_priority_tasks):
            score += 10
        elif scheduled_high_priority > 0:
            score += 5 * (scheduled_high_priority / len(high_priority_tasks))
        
        return min(score, 100.0)
