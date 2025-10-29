"""
Configuration with Truth Shield AND Quality Gate settings
"""

from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import Dict, Any

load_dotenv()


@dataclass
class TruthShieldConfig:
    """Truth Shield specific configuration"""
    truth_shield_threshold: int = 60
    enable_auto_correction: bool = True
    log_all_assessments: bool = True
    strict_mode_auto_enable: bool = True

    # Template preferences
    preferred_templates: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if not self.preferred_templates:
            self.preferred_templates = {
                'low_risk': 'template_a',
                'medium_risk': 'template_c',
                'high_risk': 'template_c',
                'critical_risk': 'template_d'
            }


@dataclass
class QualityGateConfig:
    """Quality Gate specific configuration"""
    clarity_threshold: float = 70.0
    truth_risk_threshold: float = 40.0
    quality_threshold: float = 75.0
    critical_truth_threshold: float = 60.0
    enable_auto_recovery: bool = True
    max_recovery_attempts: int = 3

    # Metric weights
    metric_weights: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if not self.metric_weights:
            self.metric_weights = {
                'clarity': 0.25,
                'truth_risk': 0.30,
                'execution': 0.20,
                'strategy': 0.25
            }


@dataclass
class SubotaiConfig:
    """Main configuration class with both Truth Shield and Quality Gate"""

    # Truth Shield Configuration
    truth_shield: TruthShieldConfig = field(default_factory=TruthShieldConfig)

    # Quality Gate Configuration
    quality_gate: QualityGateConfig = field(default_factory=QualityGateConfig)

    # Existing configurations
    model_settings: Dict[str, Any] = field(default_factory=dict)
    safety_filters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.model_settings:
            self.model_settings = {
                'max_tokens': 1000,
                'temperature': 0.7
            }

        if not self.safety_filters:
            self.safety_filters = {
                'content_filter': True,
                'fact_checking': False
            }


# Default configuration
DEFAULT_CONFIG = SubotaiConfig()
