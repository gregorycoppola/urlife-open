from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from fastapi import HTTPException

class QuestionType(str, Enum):
    CHECKBOX = "checkbox"
    RADIO = "radio"
    NUMBER = "number"

class CheckboxQuestion(BaseModel):
    caption: str
    key_name: str

class RadioOption(BaseModel):
    label: str
    value: str

class RadioQuestion(BaseModel):
    caption: str
    key_name: str
    options: List[RadioOption]

class NumberQuestion(BaseModel):
    caption: str
    key_name: str
    default: int
    min_value: int
    max_value: int

class DateQuestion(BaseModel):
    caption: str
    key_name: str
    has_date: bool
    has_time: bool

class ExtraProperties(BaseModel):
    checkbox_questions: List[CheckboxQuestion]
    radio_questions: List[RadioQuestion]
    number_questions: List[NumberQuestion]
    date_questions: List[DateQuestion]
    edge_labels: List[str]

class GoalCheckboxQuestions:
    FILTER_KEY = "PROCESSING"
    SOON = "Soon"
    CRITICAL = "Critical"
    URGENT = "Urgent"
    PROMISE = "Promise"
    NEEDS_DECISION = "Needs Decision"
    ACTIVE = "Active"

    @classmethod
    def all_keys(cls) -> List[str]:
        return [
            cls.URGENT,
            cls.CRITICAL,
            cls.NEEDS_DECISION,
            cls.ACTIVE,
        ]

    @classmethod
    def checkbox_question_vector(cls) -> List[CheckboxQuestion]:
        return [
            CheckboxQuestion(
                caption=key,
                key_name=key
            )
            for key in cls.all_keys()
        ]

def get_empty_extra_properties() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[],
        date_questions=[],
        edge_labels=[]
    )

def get_extra_properties_for_goal() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=GoalCheckboxQuestions.checkbox_question_vector(),
        radio_questions=[
            RadioQuestion(
                caption="Status",
                key_name="status",
                options=[
                    RadioOption(label="Open", value="open"),
                    RadioOption(label="Closed", value="closed"),
                    RadioOption(label="In Progress", value="in_progress")
                ]
            ),
            RadioQuestion(
                caption="Priority",
                key_name="priority",
                options=[
                    RadioOption(label="Low", value="low"),
                    RadioOption(label="Medium", value="medium"),
                    RadioOption(label="High", value="high")
                ]
            )
        ],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Parts",
            "Effects",
            "History",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_event() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[
            RadioQuestion(
                caption="Evaluation",
                key_name="evaluation",
                options=[
                    RadioOption(label="Positive", value="positive"),
                    RadioOption(label="Negative", value="negative"),
                    RadioOption(label="Neutral", value="neutral")
                ]
            ),
            RadioQuestion(
                caption="Event Size",
                key_name="event_size",
                options=[
                    RadioOption(label="Small", value="small"),
                    RadioOption(label="Medium", value="medium"),
                    RadioOption(label="Large", value="large")
                ]
            )
        ],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Feelings",
            "Outcomes",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_fact_like() -> ExtraProperties:
    return get_empty_extra_properties()

def get_extra_properties_for_state() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[
            NumberQuestion(
                caption="Polarity",
                key_name="polarity",
                default=0,
                min_value=-100,
                max_value=100
            ),
            NumberQuestion(
                caption="Probability",
                key_name="probability",
                default=0,
                min_value=0,
                max_value=100
            )
        ],
        date_questions=[],
        edge_labels=[
            "Parts",
            "Evaluation",
            "Options",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_policy() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[
            RadioQuestion(
                caption="Activity",
                key_name="activity",
                options=[
                    RadioOption(label="Active", value="active"),
                    RadioOption(label="Inactive", value="inactive")
                ]
            )
        ],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Context",
            "Objectives",
            "Response",
            "Experiences",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_decision() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Context",
            "Feelings",
            "Objectives",
            "Options",
            "Analysis",
            "Decision",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_plan() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Parts",
            "Outcomes",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_review() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Outcomes",
            "Policies",
            "Learnings",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_supply() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Context",
            "Options",
            "Experiences",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_period() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Context",
            "Objectives",
            "Policies",
            "Events",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_person() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Context",
            "Objectives",
            "Policies",
            "Events",
            "Feelings",
            "Experiences",
            "Notes",
            "Related"
        ]
    )

def get_extra_properties_for_expense() -> ExtraProperties:
    return ExtraProperties(
        checkbox_questions=[],
        radio_questions=[],
        number_questions=[],
        date_questions=[],
        edge_labels=[
            "Payments",
            "Notes",
            "Related"
        ]
    )

def make_priority_question() -> NumberQuestion:
    return NumberQuestion(
        caption="Attention",
        key_name="attention",
        default=0,
        min_value=0,
        max_value=100
    )

def get_extra_properties_for_type(type_name: str) -> ExtraProperties:
    base_types = {
        "GOAL": get_extra_properties_for_goal(),
        "REMINDER": get_extra_properties_for_goal(),
        "MEETING": get_extra_properties_for_goal(),
        "DECISION": get_extra_properties_for_decision(),
        "PLAN": get_extra_properties_for_plan(),
        "POLICY": get_extra_properties_for_policy(),
        "REVIEW": get_extra_properties_for_review(),
        "SUPPLY": get_extra_properties_for_supply(),
        "PERIOD": get_extra_properties_for_period(),
        "PERSON": get_extra_properties_for_person(),
        "EVENT": get_extra_properties_for_event(),
        "INSIGHT": get_extra_properties_for_event(),
        "VISION": get_extra_properties_for_event(),
        "STATE": get_extra_properties_for_state(),
        "EXPENSE": get_extra_properties_for_expense(),
        "THOUGHT": get_empty_extra_properties()
    }.get(type_name.upper(), get_empty_extra_properties())

    # Add priority question for all types except THOUGHT
    if type_name.upper() != "THOUGHT":
        base_types.number_questions.insert(0, make_priority_question())

    return base_types

def get_field_names_for_type(type_name: str) -> List[str]:
    extra = get_extra_properties_for_type(type_name)
    return [q.key_name for q in extra.radio_questions]

from functools import lru_cache

@lru_cache(maxsize=1)
def get_type_properties_registry() -> dict[str, ExtraProperties]:
    """
    Returns a mapping of all known type names to their configured ExtraProperties.
    This is cached once per process run.
    """
    types = [
        "GOAL", "REMINDER", "MEETING", "DECISION", "PLAN", "POLICY", "REVIEW",
        "SUPPLY", "PERIOD", "PERSON", "EVENT", "INSIGHT", "VISION",
        "STATE", "EXPENSE", "THOUGHT"
    ]
    return {type_name: get_extra_properties_for_type(type_name) for type_name in types}
