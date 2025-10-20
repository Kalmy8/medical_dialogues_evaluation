from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from medical_dialogues_scoring.config import AppSettings, get_app_settings
from fastapi import Depends
from medical_dialogues_scoring.models.scoring_endpoint import ScoringResponse

class ScoringService:
    def __init__(self, settings: AppSettings = Depends(get_app_settings)):
        llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o", temperature=0)
        self.structured_llm = llm.with_structured_output(ScoringResponse)

    async def score(self, section_text: str, dialogue: str) -> ScoringResponse:
        """
        Scores the dialogue using an LLM based on a set of standards.
        """
        # TODO remove hardcod
        prompt = PromptTemplate.from_template(
            """
            Evaluate the following medical dialogue based on the provided text and dialogue.
            Your task is to determine if the dialogue meets the four core standards.
            You must respond in the required format.

            Core Standards:
            1. Establish and document the patient's chief complaint.
            2. Unless the care is maintenance or supportive care, develop an individual treatment plan for each patient.
            3. Based on the chief complaint and objective clinical exam findings, establish specific treatment goals for each patient which are objective, measurable, reasonable, and intended to improve a functional deficit.
            4. Ensure the initial examination includes the use of standardized outcome assessment tools to establish a functional baseline against which progress towards goals may be objectively measured.

            Section Text: {section_text}
            Dialogue: {dialogue}
            """
        )

        chain = prompt | self.structured_llm

        try:
            response = await chain.ainvoke({
                "section_text": section_text,
                "dialogue": dialogue,
            })
            return response
        except OutputParserException:
            # Fallback in case of parsing error
            return ScoringResponse(
                chief_complaint_documented=False,
                individual_treatment_plan_developed=False,
                specific_treatment_goals_established=False,
                standardized_assessment_tools_used=False,
            )
