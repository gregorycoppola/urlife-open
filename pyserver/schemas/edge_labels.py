from typing import Dict, List
from pydantic import BaseModel

# Define the edge labels structure based on the Rust code
EDGE_LABELS: Dict[str, List[str]] = {
    "Goal": [
        "Parts",
        "Effects",
        "History"
    ],
    "Decision": [
        "Context",
        "Feelings",
        "Objectives",
        "Options",
        "Analysis",
        "Decision"
    ],
    "Plan": [
        "Parts",
        "Outcomes"
    ],
    "Policy": [
        "Context",
        "Objectives",
        "Response",
        "Experiences"
    ],
    "Review": [
        "Outcomes",
        "Policies",
        "Learnings"
    ],
    "Supply": [
        "Context",
        "Options",
        "Experiences"
    ],
    "Period": [
        "Context",
        "Objectives",
        "Policies",
        "Events"
    ],
    "Person": [
        "Context",
        "Objectives",
        "Policies",
        "Events",
        "Feelings",
        "Experiences"
    ],
    "Event": [
        "Feelings",
        "Outcomes"
    ],
    "State": [
        "Parts",
        "Evaluation",
        "Options"
    ],
    "Expense": [
        "Payments"
    ]
}

# Add base labels that apply to all nodes
BASE_LABELS = ["Notes", "Related"]

# Add additional labels that apply to all nodes
ADDITIONAL_LABELS = {
    "all": BASE_LABELS
}

# Define the object type mappings
OBJECT_TYPE_MAPPINGS: Dict[tuple[str, str], list[str]] = {
    # Single-specified
    ("*", "Notes"): ["Thought"],
    ("*", "Outline"): ["Link"],
    ("*", "Objectives"): ["State"],
    ("*", "Outcomes"): ["State"],
    ("*", "Policies"): ["Policy"],
    ("*", "Parts"): ["*"],  # Use base type
    ("*", "Evaluation"): ["Feeling"],
    ("*", "Events"): ["Meeting"],
    ("*", "Context"): ["State"],
    ("*", "Response"): ["Plan"],
    ("*", "Feelings"): ["Feeling"],
    ("*", "Learnings"): ["Review"],
    ("*", "Effects"): ["State"],
    
    # Double-specified
    ("Supply", "Options"): ["Goal"],
    ("Decision", "Options"): ["Plan"],
    ("State", "Options"): ["Plan"],
    ("Goal", "History"): ["Goal", "Reminder", "Track", "Decision"]
}

# Combine all the data into a single structure
EDGE_LABELS_CONFIG = {
    "node_types": EDGE_LABELS,
    "base_labels": {"all": BASE_LABELS},
    "additional_labels": ADDITIONAL_LABELS
}

# Define the response models
class EdgeLabelsResponse(BaseModel):
    node_types: Dict[str, List[str]]
    base_labels: Dict[str, List[str]]
    additional_labels: Dict[str, List[str]]

class ObjectTypesResponse(BaseModel):
    object_types: List[str]
