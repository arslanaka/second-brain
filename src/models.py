from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ThoughtCategory(str, Enum):
    TASK = "TASK"
    IDEA = "IDEA"
    REFERENCE = "REFERENCE"
    PLACE = "PLACE"
    GOAL = "GOAL"
    PERSONAL_NOTE = "PERSONAL_NOTE"
    REMINDER = "REMINDER"
    QUESTION = "QUESTION"
    SOMEDAY_MAYBE = "SOMEDAY_MAYBE"

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class EffortLevel(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class EnergyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Context(str, Enum):
    HOME = "home"
    WORK = "work"
    LAPTOP = "laptop"
    MOBILE = "mobile"
    TRAVEL = "travel"
    ERRANDS = "errands"
    ANYWHERE = "anywhere"

class Timeframe(str, Enum):
    TODAY = "today"
    THIS_WEEK = "this week"
    THIS_MONTH = "this month"
    LATER = "later"

class StructuredItem(BaseModel):
    title: str = Field(..., description="A concise title for the thought")
    description: str = Field(..., description="A detailed description of the thought")
    category: ThoughtCategory = Field(..., description="The category of the thought")
    urgency: UrgencyLevel = Field(..., description="The urgency level of the item")
    importance: int = Field(..., ge=1, le=10, description="Importance score from 1-10")
    energy_level: EnergyLevel = Field(..., description="Energy level required")
    context_tags: List[Context] = Field(default_factory=list, description="Contexts where this applies")
    effort: EffortLevel = Field(..., description="Estimated effort required")
    timeframe: Timeframe = Field(..., description="When this should be addressed")
    dependencies: List[str] = Field(default_factory=list, description="List of dependencies if any")
    clarity_score: int = Field(..., ge=0, le=100, description="Clarity score from 0-100")
    next_step: str = Field(..., description="Recommended immediate next step")

class StructuredOutput(BaseModel):
    items: List[StructuredItem] = Field(..., description="List of structured items derived from the input")
