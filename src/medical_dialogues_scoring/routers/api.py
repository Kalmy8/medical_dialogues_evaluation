from fastapi import APIRouter, Depends
from medical_dialogues_scoring.services.scoring import ScoringService
from medical_dialogues_scoring.models.scoring_endpoint import Dialogue, ScoringResponse

router = APIRouter()


@router.post("/score", response_model=ScoringResponse)
async def score_dialogue(
    dialogue: Dialogue,
    scoring_service: ScoringService = Depends(),
) -> ScoringResponse:
    score = await scoring_service.score(
        section_text=dialogue.section_text,
        dialogue=dialogue.dialogue,
    )
    return score
