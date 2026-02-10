"""
MintSense AI - Natural language expense parsing using Gemini.
"""
import google.generativeai as genai
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import json
from app.core.config import settings


# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class ParsedExpense:
    """Structured expense data parsed from natural language"""
    
    def __init__(
        self,
        amount: Decimal,
        description: str,
        category: str,
        participants: List[str],
        date: str
    ):
        self.amount = amount
        self.description = description
        self.category = category
        self.participants = participants
        self.date = date


async def parse_expense_text(
    text: str,
    group_members: List[Dict[str, str]],
    current_date: Optional[datetime] = None
) -> ParsedExpense:
    """
    Use Gemini to extract structured expense data from natural language.
    
    Args:
        text: Natural language expense description
             Example: "Paid 1200 for Sushi with Raj and Amit yesterday"
        group_members: List of group members with 'name' and 'id'
        current_date: Reference date (defaults to today)
    
    Returns:
        ParsedExpense object with structured data
        
    Raises:
        ValueError: If parsing fails or data is invalid
    """
    if current_date is None:
        current_date = datetime.now()
    
    member_names = [m['name'] for m in group_members]
    
    prompt = f"""
Extract expense details from this text: "{text}"

Available group members: {', '.join(member_names)}
Current date: {current_date.strftime('%Y-%m-%d')}

Return ONLY valid JSON with these exact fields:
{{
  "amount": <number without currency symbols>,
  "description": "<brief description of the expense>",
  "category": "<one of: Food, Travel, Entertainment, Shopping, Bills, Other>",
  "participants": ["<names from group members list>"],
  "date": "<ISO date YYYY-MM-DD>"
}}

Rules:
- If "today", use current date
- If "yesterday", use current date minus 1 day
- If specific date like "Dec 25", use that date in current year
- Participants should only include names from the available group members list
- If no participants mentioned, include all group members
- Amount should be a positive number

Return ONLY the JSON, no markdown, no explanation.
"""
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # Clean response text (remove markdown if present)
        response_text = response.text.strip()
        if response_text.startswith('```'):
            # Remove markdown code blocks
            lines = response_text.split('\n')
            response_text = '\n'.join(lines[1:-1] if lines[-1].strip() == '```' else lines[1:])
            if response_text.startswith('json'):
                response_text = response_text[4:].strip()
        
        # Parse JSON
        data = json.loads(response_text)
        
        # Validate and convert types
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        description = str(data['description'])
        category = str(data['category'])
        
        valid_categories = ['Food', 'Travel', 'Entertainment', 'Shopping', 'Bills', 'Other']
        if category not in valid_categories:
            category = 'Other'
        
        # Validate participants
        participants = []
        for name in data.get('participants', []):
            # Find matching member (case-insensitive)
            matched = False
            for member in group_members:
                if member['name'].lower() == name.lower():
                    participants.append(member['name'])
                    matched = True
                    break
            
            if not matched:
                raise ValueError(f"Participant '{name}' not found in group members")
        
        # If no participants, use all members
        if not participants:
            participants = [m['name'] for m in group_members]
        
        # Parse date
        date_str = str(data['date'])
        try:
            parsed_date = datetime.fromisoformat(date_str)
            date_iso = parsed_date.strftime('%Y-%m-%d')
        except:
            # Fallback to today
            date_iso = current_date.strftime('%Y-%m-%d')
        
        return ParsedExpense(
            amount=amount,
            description=description,
            category=category,
            participants=participants,
            date=date_iso
        )
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse AI response as JSON: {e}")
    except KeyError as e:
        raise ValueError(f"Missing required field in AI response: {e}")
    except Exception as e:
        raise ValueError(f"Failed to parse expense: {e}")


def estimate_category(description: str) -> str:
    """
    Simple keyword-based category estimation.
    Used as fallback if AI parsing fails.
    """
    description_lower = description.lower()
    
    food_keywords = ['food', 'dinner', 'lunch', 'breakfast', 'restaurant', 'sushi', 'pizza', 'coffee']
    travel_keywords = ['uber', 'taxi', 'flight', 'hotel', 'gas', 'fuel', 'train', 'bus']
    entertainment_keywords = ['movie', 'concert', 'game', 'party', 'bar', 'club']
    shopping_keywords = ['shopping', 'clothes', 'amazon', 'store']
    bills_keywords = ['bill', 'rent', 'utilities', 'internet', 'phone', 'electricity']
    
    for keyword in food_keywords:
        if keyword in description_lower:
            return 'Food'
    
    for keyword in travel_keywords:
        if keyword in description_lower:
            return 'Travel'
    
    for keyword in entertainment_keywords:
        if keyword in description_lower:
            return 'Entertainment'
    
    for keyword in shopping_keywords:
        if keyword in description_lower:
            return 'Shopping'
    
    for keyword in bills_keywords:
        if keyword in description_lower:
            return 'Bills'
    
    return 'Other'
