"""Corporate/organization name recognizer."""

from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CorporateNameRecognizer(PatternRecognizer):
    """
    Recognizes corporate/organization names from a configured list.
    
    Uses case-insensitive matching with word boundaries.
    """
    
    def __init__(
        self,
        company_names: Optional[List[str]] = None,
        supported_language: str = "en",
    ):
        """
        Initialize the corporate name recognizer.
        
        Args:
            company_names: List of company/organization names to recognize.
            supported_language: Language code (default: "en").
        """
        company_names = company_names or []
        
        # Create patterns for each company name with word boundaries
        patterns = []
        for name in company_names:
            # Escape special regex characters and create pattern
            escaped_name = self._escape_regex_special_chars(name)
            pattern = Pattern(
                name=f"corporate_{name}",
                regex=rf"\b{escaped_name}\b",
                score=0.9,
            )
            patterns.append(pattern)
        
        super().__init__(
            supported_entity="CORPORATE_NAME",
            patterns=patterns,
            supported_language=supported_language,
            context=["company", "corp", "inc", "organization", "org"],
        )
    
    @staticmethod
    def _escape_regex_special_chars(text: str) -> str:
        """
        Escape special regex characters but preserve spaces.
        
        Args:
            text: Text to escape.
            
        Returns:
            str: Escaped text safe for regex pattern.
        """
        import re
        # Escape special chars but handle spaces separately
        special_chars = r"\.^$*+?{}[]|()"
        escaped = ""
        for char in text:
            if char in special_chars:
                escaped += "\\" + char
            else:
                escaped += char
        return escaped
