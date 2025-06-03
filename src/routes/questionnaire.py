from fastapi import APIRouter, Depends, HTTPException, Response, status
import uuid
from scipy.stats import multinomial
from pydantic import BaseModel
from typing import List
from src.db import crud, models, schemas
from src.db.utils import get_db
from src.db.database import SessionLocal, engine
from sqlalchemy.orm import Session
from src.calibration import utils
import pandas as pd

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/questionnaire",
    tags=["Questionnaire"],
    responses={404: {"description": "Not found"}},
)

class DemographicQuestions(BaseModel):
    question: str
    answer: str

class Demographic(BaseModel):
    demographicQuestions: List[DemographicQuestions]


class RecommendationQuestions(BaseModel):
    question: str
    answer: str

class Recommendation(BaseModel):
    recommendationQuestions: List[RecommendationQuestions]


class SelectedRecommendationQuestions(BaseModel):
    imdb_id: str
    watched_the_movie: bool

class SelectedRecommendation(BaseModel):
    recommendations: List[SelectedRecommendationQuestions]
    selected_movie: str


@router.post("/demographic/{id}")
def store_demographic_questions(id: str, data: Demographic, response: Response, db: Session = Depends(get_db)):
    try:
        crud.store_demographic(
            db, data, id
        )
        return {'message': 'question stored'}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'error, cant store questions. Error: {e}'}


@router.post("/selected_movies/{id}")
def store_selected_movies_questions(id: str, data: SelectedRecommendation, response: Response, db: Session = Depends(get_db)):
    try:
        crud.store_selected_recommendation(
            db, data, id
        )
        return {'message': 'question stored'}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'error, cant store questions. Error: {e}'}


@router.post("/recommendation/{id}")
def store_recommendation_questions(id: str, data: Recommendation, response: Response, db: Session = Depends(get_db)):
    try:
        crud.store_recommendation(
            db, data, id
        )
        return {'message': 'question stored'}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'error, cant store questions. Error: {e}'}