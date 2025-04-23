from fastapi import APIRouter
from .. import schemas
from ..repository import explainer


router = APIRouter(
    prefix = '/explain',
    tags = ['Explainer']
)


@router.post("/generate_steps", status_code=200, response_model=schemas.GuidedExplanation)
def generate_steps(request: schemas.PromptRequest):
    return explainer.generate_steps(request)


@router.post('/', status_code=200)
def explain(request: schemas.TopicRequest):
    return explainer.explain(request)


# @router.post('/imagine', status_code=200)
# def imagine(request: schemas.TopicRequest):
#     return explainer.imagine(request)