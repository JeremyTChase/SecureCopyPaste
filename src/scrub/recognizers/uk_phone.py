"""UK phone number recognizer."""

from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class UKPhoneRecognizer(PatternRecognizer):
    """
    Recognizes UK phone numbers in various formats.
    
    Supports:
    - 07xxx xxxxxx (mobile)
    - 01xx xxx xxxx (landline)
    - 02x xxxx xxxx (London, etc.)
    - +44 variations
    - With/without spaces, dashes, parentheses
    """
    
    PATTERNS = [
        Pattern(
            name="uk_mobile",
            regex=r"\b(?:\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}\b",
            score=0.85,
        ),
        Pattern(
            name="uk_landline",
            regex=r"\b(?:\+44\s?[12]\d{2,3}|\(?0[12]\d{2,3}\)?)\s?\d{3,4}\s?\d{4}\b",
            score=0.85,
        ),
        Pattern(
            name="uk_phone_with_plus",
            regex=r"\+44\s?\d{2,4}\s?\d{3,4}\s?\d{4}",
            score=0.9,
        ),
    ]
    
    def __init__(self, supported_language: str = "en"):
        """
        Initialize UK phone recognizer.
        
        Args:
            supported_language: Language code (default: "en").
        """
        super().__init__(
            supported_entity="UK_PHONE_NUMBER",
            patterns=self.PATTERNS,
            supported_language=supported_language,
            context=["phone", "mobile", "tel", "call", "contact"],
        )
