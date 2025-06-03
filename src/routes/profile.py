from fastapi import APIRouter, Depends, HTTPException
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
data = pd.read_csv("./data/items.csv", lineterminator='\n')
exist_items = data['imdb'].unique().tolist()

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    responses={404: {"description": "Not found"}},
)

class Interaction(BaseModel):
    item_id: str
    rating: int

class AddInteractions(BaseModel):
    interactions: List[Interaction]
    user_id: str



@router.post("/")
def add_interacted_movies(interactions: AddInteractions, db: Session = Depends(get_db)):
    for interaction in interactions.interactions:
        if interaction.item_id not in exist_items:
            return {'message': f'Item {interaction.item_id} dont exist in the database'}
        crud.add_interaction(
            db,
            schemas.InteractionCreate(
                item_id=interaction.item_id,
                rating=interaction.rating,
                user_id=interactions.user_id
            )
        )
    
    response = crud.get_interactions(db, interactions.user_id)
    new_user_distribution_pop = utils.calculate_user_distribution_popularity([(i.item_id, i.rating) for i in response], data)
    new_user_distribution_budget = utils.calculate_user_distribution_budget([(i.item_id, i.rating) for i in response], data)

        

    crud.create_popularity_budget(db, schemas.AddPopularity(
        experiment_id=interactions.user_id,
        H=new_user_distribution_budget['H'],
        M=new_user_distribution_budget['M'],
        T=new_user_distribution_budget['T']
    ))

    crud.create_popularity(db, schemas.AddPopularity(
        experiment_id=interactions.user_id,
        H=new_user_distribution_pop['H'],
        M=new_user_distribution_pop['M'],
        T=new_user_distribution_pop['T']
    ))

    return {'message': 'interactions added'}


@router.get("/{id}")
def get_user_profile(id: str, db: Session = Depends(get_db)):
    response = crud.get_interactions(db, id)
    returned_data = [
        {
            'item_id': i.item_id,
            'rating': i.rating,
            'added_timestamp': i.added_timestamp
        } for i in response
    ]
    
    return returned_data
