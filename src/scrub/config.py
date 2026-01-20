"""Configuration loading and management."""

import os
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class Config:
    """Configuration for scrub tool."""
    
    def __init__(
        self,
        company_names: Optional[List[str]] = None,
        domains: Optional[List[str]] = None,
        project_names: Optional[List[str]] = None,
        deny_list: Optional[List[str]] = None,
    ):
        """
        Initialize configuration.
        
        Args:
            company_names: List of company/organization names to redact.
            domains: List of internal domains/URLs to redact.
            project_names: List of project/product names to redact.
            deny_list: List of custom terms to redact.
        """
        self.company_names = company_names or []
        self.domains = domains or []
        self.project_names = project_names or []
        self.deny_list = deny_list or []
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to config file. If None, uses default location.
            
        Returns:
            Config: Loaded configuration object.
        """
        if config_path is None:
            config_path = get_default_config_path()
        
        if not config_path.exists():
            # Return empty config if no config file exists
            return cls()
        
        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
            
            corporate = data.get("corporate", {})
            
            return cls(
                company_names=corporate.get("company_names", []),
                domains=corporate.get("domains", []),
                project_names=corporate.get("project_names", []),
                deny_list=corporate.get("deny_list", []),
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse config file: {e}") from e
        except Exception as e:
            raise ValueError(f"Failed to load config: {e}") from e
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary format."""
        return {
            "corporate": {
                "company_names": self.company_names,
                "domains": self.domains,
                "project_names": self.project_names,
                "deny_list": self.deny_list,
            }
        }


def get_default_config_path() -> Path:
    """
    Get the default configuration file path.
    
    Returns:
        Path: Default config path (~/.config/scrub/config.yaml)
    """
    config_dir = Path.home() / ".config" / "scrub"
    return config_dir / "config.yaml"


def get_config_dir() -> Path:
    """
    Get the configuration directory, creating it if needed.
    
    Returns:
        Path: Config directory path (~/.config/scrub/)
    """
    config_dir = Path.home() / ".config" / "scrub"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def create_example_config(output_path: Optional[Path] = None) -> None:
    """
    Create an example configuration file.
    
    Args:
        output_path: Where to write the example. If None, uses default location.
    """
    if output_path is None:
        output_path = get_default_config_path()
    
    example_config = {
        "corporate": {
            "company_names": [
                "Example Corp",
                "Example Inc",
            ],
            "domains": [
                "example.com",
                "internal.example.io",
            ],
            "project_names": [
                "Project Phoenix",
                "Codename Titan",
            ],
            "deny_list": [
                "confidential-system-name",
                "internal-tool-v2",
            ],
        }
    }
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        yaml.dump(example_config, f, default_flow_style=False, sort_keys=False)
