import uuid
from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum


class ConstraintTypes(str, Enum):
    default = "Default"
    temporal = "TemporalConstraint"
    venue = "VenueConstraint"
    team = "TeamConstraint"
    general = "GeneralConstraint"

class TemporalConstraints(str, Enum):
    default = "Default"
    back_to_back = "BackToBackConstraint"
    rest_days = "RestDaysConstraint"
    days_of_week = "DaysOfWeekConstraint"
    date_range = "DateRangeConstraint"

class VenueConstraints(str, Enum):
    default = "Default"
    home_away = "HomeAwayConstraint"
    travel_considerations = "TravelConsiderationsConstraint"
    venue_availability = "VenueAvailabilityConstraint"
    venue_capacity = "VenueCapacityConstraint"

class TeamConstraints(str, Enum):
    default = "Default"
    team_preferences = "TeamPreferencesConstraint"
    rivalries = "RivalriesConstraint"
    competitive_balance = "CompetitiveBalanceConstraint"
    team_availability = "TeamAvailabilityConstraint"

class GeneralConstraints(str, Enum):
    default = "Default"
    game_frequency_limit = "GameFrequencyLimitConstraint"
    season_structure = "SeasonStructureConstraint"


class Constraint(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier for the constraint")
    type: ConstraintTypes = Field(
        default=ConstraintTypes.default,
        description="Type of the constraint, must be one of 'temporal', 'venue', 'team', or 'general'"
    )
    scope: list[str] = Field(
        default_factory=list,
        description="Scope of the temporal constraint, includes teams, and games affected by the constraint"
    )
    priority: Literal["hard", "soft"] = Field(
        default="hard",
        description="Priority of the constraint, can be 'hard' or 'soft'"
    )
    confidence: float = Field(
        default=-1.0,
        description="Confidence level of the constraint, indicating how strongly it should be enforced"

    )

class StructuredOutput(BaseModel):
    constraints: list[Constraint] = Field(
        default_factory=list,
        description="List of constraints to be applied to the scheduling process"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Additional metadata related to the scheduling process"
    )
class Parameters(BaseModel):
    restriction_value:str = Field(
        default="",
        description="Value of the restriction, such as a specific date or number of days"
    )
class TemporalParameters(Parameters):
    back_to_back: bool = Field(
        default=False,
        description="Indicates if back-to-back games are allowed"
    )
    rest_days: int = Field(
        default=5,
        description="Number of rest days required between games"
    )
    days_of_week: list[str] = Field(
        default_factory=list,
        description="Specific day of the week for scheduling games"
    )
    date_range: tuple[str, str] = Field(
        default=("", ""),
        description="Start and end dates for the scheduling period"
    )

class VenueParameters(Parameters):
    home_away: bool = Field(
        default=False,
        description="Indicates if home and away games are required"
    )
    travel_considerations: bool = Field(
        default=False,
        description="Indicates if travel considerations should be taken into account"
    )
    venue_availability: list[str] = Field(
        default_factory=list,
        description="List of available venues for scheduling"
    )
    venue_capacity: int = Field(
        default=0,
        description="Capacity of the venue for scheduling purposes"
    )
class TeamParameters(Parameters):
    team_preferences: dict = Field(
        default_factory=dict,
        description="Preferences of teams for scheduling, such as preferred days or times"
    )
    rivalries: list[str] = Field(
        default_factory=list,
        description="List of rivalries to consider in the scheduling process"
    )
    competitive_balance: bool = Field(
        default=False,
        description="Indicates if competitive balance should be maintained in the schedule"
    )
    team_availability: dict = Field(
        default_factory=dict,
        description="Availability of teams for scheduling, such as dates when they are not available"
    )
class GeneralParameters(Parameters):
    game_frequency_limit: int = Field(
        default=0,
        description="Maximum number of games allowed within a certain period"
    )
    season_structure: str = Field(
        default="",
        description="Structure of the season, such as number of games or playoff format"
    )
class TemporalConstraint(Constraint):
    type: TemporalConstraints = Field(
        default=TemporalConstraints.default,
        description="Type of the temporal constraint, must be one of 'back_to_back', 'rest_days', 'days_of_week', or 'date_range'"
    )
    parameters: TemporalParameters = Field(
        default_factory=TemporalParameters,
        description="Parameters for the temporal constraint, such as rest days or specific dates"
    )

class VenueConstraint(Constraint):
    type: VenueConstraints = Field(
        default=VenueConstraints.default,
        description="Type of the venue constraint, must be one of 'home_away', 'travel_considerations', 'venue_availability', or 'venue_capacity'"
    )
    parameters: VenueParameters = Field(
        default_factory=VenueParameters,
        description="Parameters for the venue constraint, such as venue availability or capacity"
    )


class TeamConstraint(Constraint):
    type: TeamConstraints = Field(
        default=TeamConstraints.default,
        description="Type of the team constraint, must be one of 'team_preferences', 'rivalries', 'competitive_balance', or 'team_availability'"
    )
    parameters: TeamParameters = Field(
        default_factory=TeamParameters,
        description="Parameters for the team constraint, such as team preferences or availability"
    )

class GeneralConstraint(Constraint):
    type: GeneralConstraints = Field(
        default=GeneralConstraints.default,
        description="Type of the general constraint, must be one of 'game_frequency_limit' or 'season_structure'"
    )
    parameters: GeneralParameters = Field(
        default_factory=GeneralParameters,
        description="Parameters for the general constraint, such as game frequency limit or season structure"
    )
