from enum import Enum
from typing import List, Dict, Any, Tuple, Union, Literal, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TemporalConstraints(str, Enum):
  Default = "Default"
  BackToBack = "BackToBackConstraint"
  RestDays = "RestDaysConstraint"
  DaysOfWeek = "DaysOfWeekConstraint"
  DateRange = "DateRangeConstraint"


class VenueConstraints(str, Enum):
  Default = "Default"
  HomeAway = "HomeAwayConstraint"
  TravelConsiderations = "TravelConsiderationsConstraint"
  VenueAvailability = "VenueAvailabilityConstraint"
  VenueCapacity = "VenueCapacityConstraint"


class TeamConstraints(str, Enum):
  Default = "Default"
  TeamPreferences = "TeamPreferencesConstraint"
  Rivalries = "RivalriesConstraint"
  CompetitiveBalance = "CompetitiveBalanceConstraint"
  TeamAvailability = "TeamAvailabilityConstraint"


class GeneralConstraints(str, Enum):
  Default = "Default"
  GameFrequencyLimit = "GameFrequencyLimitConstraint"
  SeasonStructure = "SeasonStructureConstraint"

class ConstraintValue(str, Enum):
  Default = "Default"
  MustNot = "MustNot"
  PreferNot = "PreferNot"
  Prefer = "Prefer"
  Must = "Must"

class Parameters(BaseModel):
  restriction_value: Optional[ConstraintValue] = Field(
    default=None,
    description="Level of restriction for the constraint (e.g., Must, Prefer, etc.)."
  )

class DateRange(BaseModel):
  start_date: str = Field(
    ...,
    description="Start date of the range in YYYY-MM-DD format."
  )
  end_date: str = Field(
    ...,
    description="End date of the range in YYYY-MM-DD format."
  )

class TemporalParameters(Parameters):
  back_to_back: Optional[bool] = Field(
    default=None,
    description="Whether back-to-back games are allowed."
  )
  rest_days: Optional[int] = Field(
    default=None,
    description="Minimum number of rest days required between games."
  )
  days_of_week: Optional[List[str]] = Field(
    default=None,
    description="Allowed days of the week for games."
  )
  date_range: Optional[DateRange] = Field(
    default=None,
    description="Date range for scheduling games."
  )

class MaxConsecutiveGames(BaseModel):
    type: Optional[str] = Field(
      default=None,
      description="Type of consecutive games (e.g., home, away)."
    )
    limit: Optional[int] = Field(
      default=None,
      description="Maximum number of consecutive games allowed."
    )
  
class VenueParameters(Parameters):
  max_consecutive_games: Optional[MaxConsecutiveGames] = Field(
    default=None,
    description="Maximum number of consecutive home or away games allowed. Specify type and limit."
  )
  max_travel_distance: Optional[float] = Field(
    default=None,
    description="Maximum allowed travel distance for teams (in miles)."
  )
  venue_availability: Optional[List[str]] = Field(
    default=None,
    description="List of available venues or dates for venues."
  )
  venue_capacity: Optional[int] = Field(
    default=None,
    description="Minimum required venue capacity."
  )


class TeamParameters(Parameters):
  team_preferences: Optional[Dict[str, Any]] = Field(
    default=None,
    description="Preferences for specific teams."
  )
  rivalries: Optional[List[str]] = Field(
    default=None,
    description="List of team rivalries to consider."
  )
  competitive_balance: Optional[Dict[str, Any]] = Field(
    default=None,
    description="Rules to enforce competitive balance, e.g., prevent matchups between specific rankings such as first and last place teams. Example: {'prevent_matchups': [['1st', 'last']]}."
  )
  team_availability: Optional[Dict[str, Any]] = Field(
    default=None,
    description="Availability information for teams."
  )


class GeneralParameters(Parameters):
  game_frequency_limit: Optional[int] = Field(
    default=None,
    description="Maximum number of games allowed in the specified period."
  )
  game_frequency_timeframe: Optional[str] = Field(
    default=None,
    description="Timeframe for the game frequency limit (e.g., per week, per month)."
  )
  season_structure: Optional[str] = Field(
    default=None,
    description="Structure of the season (e.g., regular, playoffs)."
  )


class Constraint(BaseModel):
  type: Optional[Union[TemporalConstraints, VenueConstraints, TeamConstraints, GeneralConstraints]] = Field(
    default=None,
    description="Type of constraint."
  )
  scope: Optional[List[str]] = Field(
    default=None,
    description="Scope of the constraint (e.g., teams, venues)."
  )
  priority: Optional[Literal["hard", "soft"]] = Field(
    default="hard",
    description="Priority of the constraint (hard or soft)."
  )
  confidence: Optional[float] = Field(
    default=None,
    description="Confidence level for the constraint."
  )


class TemporalConstraint(Constraint):
  type: Optional[TemporalConstraints] = Field(
    default=None,
    description="Type of temporal constraint."
  )
  parameters: Optional[TemporalParameters] = Field(
    default=None,
    description="Parameters specific to temporal constraints."
  )


class VenueConstraint(Constraint):
  type: Optional[VenueConstraints] = Field(
    default=None,
    description="Type of venue constraint."
  )
  parameters: Optional[VenueParameters] = Field(
    default=None,
    description="Parameters specific to venue constraints."
  )


class TeamConstraint(Constraint):
  type: Optional[TeamConstraints] = Field(
    default=None,
    description="Type of team constraint."
  )
  parameters: Optional[TeamParameters] = Field(
    default=None,
    description="Parameters specific to team constraints."
  )


class GeneralConstraint(Constraint):
  type: Optional[GeneralConstraints] = Field(
    default=None,
    description="Type of general constraint."
  )
  parameters: Optional[GeneralParameters] = Field(
    default=None,
    description="Parameters specific to general constraints."
  )


class StructuredOutput(BaseModel):
  constraints: Optional[List[Union[TemporalConstraint, VenueConstraint, TeamConstraint, GeneralConstraint]]] = Field(
    default=None,
    description="List of constraints for the schedule."
  )
  metadata: Optional[Dict[str, Any]] = Field(
    default=None,
    description="Additional metadata related to the constraints."
  )


class Message(BaseModel):
  role: Optional[str] = Field(
    default=None,
    description="Role of the message sender (e.g., user, assistant)."
  )
  content: Optional[str] = Field(
    default=None,
    description="Content of the message."
  )


class StructuredRequest(BaseModel):
  messages: Optional[list[Message]] = Field(
    default=None,
    description="List of messages in the structured request."
  )


class ChatRequest(BaseModel):
  messages: Optional[Message] = Field(
    default=None,
    description="Single message for the chat request."
  )


class ChatResponse(BaseModel):
  response: Optional[str] = Field(
    default=None,
    description="Response content from the chat."
  )

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Unique user ID")
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's hashed password")
