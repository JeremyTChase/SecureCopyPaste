"""Internal domain and URL recognizer."""

from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class DomainRecognizer(PatternRecognizer):
    """
    Recognizes internal domains in URLs only (not emails or paths).
    
    This recognizer focuses on URLs to avoid false positives in:
    - File paths (e.g., /Users/name@domain.com/)
    - Email addresses (handled by Presidio's EMAIL_ADDRESS recognizer)
    """
    
    def __init__(
        self,
        domains: Optional[List[str]] = None,
        supported_language: str = "en",
    ):
        """
        Initialize the domain recognizer.
        
        Args:
            domains: List of internal domains to recognize (e.g., "internal.company.com").
            supported_language: Language code (default: "en").
        """
        domains = domains or []
        
        # Create patterns for each domain - URLs only
        patterns = []
        for domain in domains:
            # Escape special regex characters
            escaped_domain = self._escape_domain(domain)
            
            # Only match URLs: https://domain or http://domain
            # This avoids matching emails (already handled) and file paths
            url_pattern = Pattern(
                name=f"internal_url_{domain}",
                regex=rf"https?://{escaped_domain}(?:/[^\s]*)?",
                score=0.9,
            )
            patterns.append(url_pattern)
        
        super().__init__(
            supported_entity="INTERNAL_DOMAIN",
            patterns=patterns,
            supported_language=supported_language,
            context=["url", "http", "https", "www", "visit", "goto"],
        )
    
    @staticmethod
    def _escape_domain(domain: str) -> str:
        """
        Escape special regex characters in domain name.
        
        Args:
            domain: Domain to escape.
            
        Returns:
            str: Escaped domain safe for regex pattern.
        """
        import re
        # Escape dots and other special chars
        return re.escape(domain)

