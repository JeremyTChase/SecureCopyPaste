"""Core text scrubbing functionality using Presidio."""

from typing import Dict, List, Optional

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from .config import Config
from .recognizers import (
    CorporateNameRecognizer,
    DenyListRecognizer,
    DomainRecognizer,
    UKPhoneRecognizer,
)


class TextScrubber:
    """
    Scrubs PII and corporate information from text using Microsoft Presidio.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the text scrubber.
        
        Args:
            config: Configuration containing corporate terms to redact.
        """
        self.config = config or Config()
        self.analyzer = self._create_analyzer()
        self.anonymizer = AnonymizerEngine()
    
    def _create_analyzer(self) -> AnalyzerEngine:
        """
        Create and configure the Presidio analyzer with custom recognizers.
        
        Returns:
            AnalyzerEngine: Configured analyzer instance.
        """
        # Create NLP engine (using spaCy)
        nlp_configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_lg"}],
        }
        
        provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
        nlp_engine = provider.create_engine()
        
        # Create registry with custom recognizers
        registry = RecognizerRegistry()
        
        # Load default recognizers (email, phone, SSN, credit card, etc.)
        registry.load_predefined_recognizers(nlp_engine=nlp_engine)
        
        # Add custom recognizers for corporate information
        if self.config.company_names:
            corporate_recognizer = CorporateNameRecognizer(
                company_names=self.config.company_names
            )
            registry.add_recognizer(corporate_recognizer)
        
        if self.config.domains:
            domain_recognizer = DomainRecognizer(domains=self.config.domains)
            registry.add_recognizer(domain_recognizer)
        
        if self.config.project_names:
            # Project names can use the corporate recognizer with different entity type
            project_recognizer = CorporateNameRecognizer(
                company_names=self.config.project_names
            )
            # Override entity type
            project_recognizer.supported_entities = ["PROJECT_NAME"]
            registry.add_recognizer(project_recognizer)
        
        if self.config.deny_list:
            denylist_recognizer = DenyListRecognizer(deny_list=self.config.deny_list)
            registry.add_recognizer(denylist_recognizer)
        
        # Add UK phone number recognizer (always enabled)
        uk_phone_recognizer = UKPhoneRecognizer()
        registry.add_recognizer(uk_phone_recognizer)
        
        # Create analyzer with custom registry
        analyzer = AnalyzerEngine(
            registry=registry,
            nlp_engine=nlp_engine,
            supported_languages=["en"],
        )
        
        return analyzer
    
    def scrub(self, text: str, language: str = "en") -> str:
        """
        Scrub PII and corporate information from text.
        
        Args:
            text: The text to scrub.
            language: Language code (default: "en").
            
        Returns:
            str: The scrubbed text with PII replaced by type labels.
        """
        if not text or not text.strip():
            return text
        
        # Analyze text for PII
        results = self.analyzer.analyze(
            text=text,
            language=language,
        )
        
        # Create operators for each entity type to replace with <TYPE> labels
        operators = {}
        for result in results:
            entity_type = result.entity_type
            operators[entity_type] = OperatorConfig("replace", {"new_value": f"<{entity_type}>"})
        
        # If no entities found, return original text
        if not operators:
            return text
        
        # Anonymize with custom operators
        anonymized = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=operators,
        )
        
        return anonymized.text
    
    def analyze(self, text: str, language: str = "en") -> List:
        """
        Analyze text and return detected PII entities without anonymizing.
        
        Useful for dry-run mode to show what would be redacted.
        
        Args:
            text: The text to analyze.
            language: Language code (default: "en").
            
        Returns:
            List: List of detected PII entities.
        """
        if not text or not text.strip():
            return []
        
        return self.analyzer.analyze(text=text, language=language)


def scrub_text(text: str, config: Optional[Config] = None) -> str:
    """
    Convenience function to scrub text with optional configuration.
    
    Args:
        text: The text to scrub.
        config: Optional configuration for corporate terms.
        
    Returns:
        str: The scrubbed text.
    """
    scrubber = TextScrubber(config=config)
    return scrubber.scrub(text)
