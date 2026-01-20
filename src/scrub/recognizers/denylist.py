"""Custom deny-list recognizer for arbitrary sensitive terms."""

from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class DenyListRecognizer(PatternRecognizer):
    """
    Recognizes terms from a custom deny-list.
    
    Matches exact terms (case-insensitive) from a configured list.
    """
    
    def __init__(
        self,
        deny_list: Optional[List[str]] = None,
        supported_language: str = "en",
    ):
        """
        Initialize the deny-list recognizer.
        
        Args:
            deny_list: List of terms to recognize and redact.
            supported_language: Language code (default: "en").
        """
        deny_list = deny_list or []
        
        # Create patterns for each deny-list term
        patterns = []
        for term in deny_list:
            # Escape special regex characters
            escaped_term = self._escape_regex_special_chars(term)
            
            # Use word boundaries for whole-word matching
            pattern = Pattern(
                name=f"denylist_{term}",
                regex=rf"\b{escaped_term}\b",
                score=1.0,  # High confidence for explicit deny-list
            )
            patterns.append(pattern)
        
        super().__init__(
            supported_entity="DENY_LIST",
            patterns=patterns,
            supported_language=supported_language,
            context=[],  # No specific context needed for deny-list
        )
    
    @staticmethod
    def _escape_regex_special_chars(text: str) -> str:
        """
        Escape special regex characters.
        
        Args:
            text: Text to escape.
            
        Returns:
            str: Escaped text safe for regex pattern.
        """
        import re
        return re.escape(text)
