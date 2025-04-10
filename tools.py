from langchain_core.tools import tool
from typing import List, Dict, Any
from database import hura_info

@tool
def get_privacy_features() -> Dict[str, Any]:
    """Get information about Hura's privacy features and how they work"""
    return hura_info['privacy_features']

@tool
def get_decentralization_explanation() -> Dict[str, Any]:
    """Get detailed explanation of how Hura's decentralization works"""
    return hura_info['decentralization']

@tool
def get_company_info() -> Dict[str, Any]:
    """Get information about Secure Intelligent, the company behind Hura"""
    return hura_info['company_info']

@tool
def get_encryption_details() -> Dict[str, Any]:
    """Get technical details about Hura's encryption methodology"""
    return hura_info['encryption_details']

@tool
def get_federated_learning_explanation() -> Dict[str, Any]:
    """Get explanation of how federated learning works in Hura"""
    return hura_info['federated_learning']

@tool
def get_ai_ethics_principles() -> List[Dict[str, Any]]:
    """Get Hura's AI ethics principles and guidelines"""
    return hura_info['ai_ethics']

@tool
def get_comparison_with_centralized_models() -> Dict[str, Any]:
    """Get comparison between Hura and centralized AI models"""
    return hura_info['model_comparison']

@tool
def get_terminology() -> Dict[str, str]:
    """Get Hura terminology dictionary"""
    return hura_info['terminology']

@tool
def search_terminology(term: str) -> Dict[str, str]:
    """
    Search for a specific term in Hura's terminology dictionary
    Args:
        term (str): Term to search for
    """
    results = {}
    for key, value in hura_info['terminology'].items():
        if term.lower() in key.lower():
            results[key] = value
    return results


tools = [
    get_privacy_features,
    get_decentralization_explanation,
    get_company_info,
    get_encryption_details,
    get_federated_learning_explanation,
    get_ai_ethics_principles,
    get_comparison_with_centralized_models,
    get_terminology,
    search_terminology
]
