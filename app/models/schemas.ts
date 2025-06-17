import { v4 as uuidv4 } from "uuid";

export enum TemporalConstraints {
  Default = "Default",
  BackToBack = "BackToBackConstraint",
  RestDays = "RestDaysConstraint",
  DaysOfWeek = "DaysOfWeekConstraint",
  DateRange = "DateRangeConstraint",
}

export enum VenueConstraints {
  Default = "Default",
  HomeAway = "HomeAwayConstraint",
  TravelConsiderations = "TravelConsiderationsConstraint",
  VenueAvailability = "VenueAvailabilityConstraint",
  VenueCapacity = "VenueCapacityConstraint",
}

export enum TeamConstraints {
  Default = "Default",
  TeamPreferences = "TeamPreferencesConstraint",
  Rivalries = "RivalriesConstraint",
  CompetitiveBalance = "CompetitiveBalanceConstraint",
  TeamAvailability = "TeamAvailabilityConstraint",
}

export enum GeneralConstraints {
  Default = "Default",
  GameFrequencyLimit = "GameFrequencyLimitConstraint",
  SeasonStructure = "SeasonStructureConstraint",
}

export interface Constraint {
  id: string;
  type: TemporalConstraints | VenueConstraints | TeamConstraints | GeneralConstraints;
  scope: string[];
  priority: "hard" | "soft";
  confidence: number;
}

export interface StructuredOutput {
  constraints: Constraint[];
  metadata: Record<string, any>;
}

export interface Parameters {
  restriction_value: string;
}

export interface TemporalParameters extends Parameters {
  back_to_back: boolean;
  rest_days: number;
  days_of_week: string[];
  date_range: [string, string];
}

export interface VenueParameters extends Parameters {
  home_away: boolean;
  travel_considerations: boolean;
  venue_availability: string[];
  venue_capacity: number;
}

export interface TeamParameters extends Parameters {
  team_preferences: Record<string, any>;
  rivalries: string[];
  competitive_balance: boolean;
  team_availability: Record<string, any>;
}

export interface GeneralParameters extends Parameters {
  game_frequency_limit: number;
  season_structure: string;
}

export interface TemporalConstraint extends Constraint {
  type: TemporalConstraints;
  parameters: TemporalParameters;
}

export interface VenueConstraint extends Constraint {
  type: VenueConstraints;
  parameters: VenueParameters;
}

export interface TeamConstraint extends Constraint {
  type: TeamConstraints;
  parameters: TeamParameters;
}

export interface GeneralConstraint extends Constraint {
  type: GeneralConstraints;
  parameters: GeneralParameters;
}

// Utility function to generate a new constraint with a unique ID
export function createConstraint(): Constraint {
  return {
    id: uuidv4(),
    type: GeneralConstraints.Default,
    scope: [],
    priority: "hard",
    confidence: -1.0,
  };
}
