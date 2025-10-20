from pydantic import BaseModel, Field


class Dialogue(BaseModel):
    section_text: str
    dialogue: str


class ScoringResponse(BaseModel):
    chief_complaint_documented: bool = Field(..., description="Establish and document the patient’s chief complaint.")
    individual_treatment_plan_developed: bool = Field(..., description="Unless the care is maintenance or supportive care, develop an individual treatment plan for each patient.")
    specific_treatment_goals_established: bool = Field(..., description="Based on the chief complaint and objective clinical exam findings, establish specific treatment goals for each patient which are objective, measurable, reasonable, and intended to improve a functional deficit.")
    standardized_assessment_tools_used: bool = Field(..., description="Ensure the initial examination includes the use of standardized outcome assessment tools to establish a functional baseline against which progress towards goals may be objectively measured.")