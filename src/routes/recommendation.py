from fastapi import APIRouter, Depends, HTTPException
import uuid
import pika
import gc
from scipy.stats import multinomial
from pydantic import BaseModel
from typing import List
from src.db import crud, models, schemas
from src.db.utils import get_db
from src.db.database import SessionLocal, engine
from sqlalchemy.orm import Session
import numpy as np
import pandas as pd
from src.calibration import pptm

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"],
    responses={404: {"description": "Not found"}},
)

data = pd.read_csv("./data/items.csv", lineterminator='\n')
movies_popularities = {}
movies_budgets = {}
for index, row in data.iterrows():
    movies_popularities[row['movieId']] = row['popularity_int']
    movies_budgets[row['movieId']] = row['popularity_budget_inf']

N_items = max(data['movieId'])+1

pop_map = {
    "H": 3,
    "M": 2,
    "T": 1
}
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

@router.get("/{id}")
async def get_user_recommendation(id: str, db: Session = Depends(get_db)):
    response = crud.get_interactions(db, id)
    
    unique_interactions = set([i.item_id for i in response])

    if len(unique_interactions) < 7:
        return {'message': 'user need to rate at least 10 movies', 'data': []}
    

    response_profile_ex = crud.get_user(db, id)
    profile_exp_type = response_profile_ex.experiment_type

    # Send interacted items
    channel.queue_declare(queue='recommender_start')
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body={
                        'profile_exp_type':profile_exp_type,
                        'unique_interactions': unique_interactions
                    })

    ...


    # interacted_items = []
    # for i in response:
    #     aux = data[data['imdb'] == i.item_id]
    #     interacted_items.append(int(aux['movieId'].values[0]))


    # movies_ids = [1 if int(i) in interacted_items else 0 for i in range(N_items)]
    # movies_ids = np.array(movies_ids)

    # model_matrix = np.load("./data/model.npz")
    # model_matrix = model_matrix['data']
    # pred_mat = np.dot(movies_ids, model_matrix)
    # del model_matrix
    # gc.collect()

    # item_score = list(enumerate(pred_mat))
    # del pred_mat
    # gc.collect()
    # itemscores = {k:v for k,v in item_score}
    
    # selected_items = [i[0] for i in sorted(item_score, key=lambda x: x[1], reverse=True)]
    # selected_items_score = sorted(item_score, key=lambda x: x[1], reverse=True)

    # top_10 = [i for i in selected_items if i not in interacted_items][:10]

    # if profile_exp_type == 0:
    #     selected_items = [i for i in selected_items if i not in interacted_items][:10]
    # elif profile_exp_type == 1 or profile_exp_type == 3:
    #     response = crud.get_popularity_budget(db, id)
    #     results = pptm.run_calibration(
    #         selected_items_score,
    #         response,
    #         movies_popularities,
    #         itemscores,
    #         data,
    #         movies_budgets,
    #         column='budget',
    #         c=1
    #     )
    #     selected_items = results

    # elif profile_exp_type == 2 or profile_exp_type == 4:
    #     response = crud.get_popularity(db, id)
    #     results = pptm.run_calibration(
    #         selected_items_score,
    #         response,
    #         movies_popularities,
    #         itemscores,
    #         data,
    #         movies_budgets,
    #         column='popularity',
    #         c=1
    #     )
    #     selected_items = results
    # else:
    #     selected_items = [i for i in selected_items if i not in interacted_items][:10]

    selected_items = [i for i in selected_items if i not in interacted_items][:10]
    recommendation_data = []

    distpop = {'H': 0,'M': 0,'T': 0}
    distbud = {'H': 0,'M': 0,'T': 0}
    for i in selected_items:
        movie_info = data[data['movieId'] == i]
        distpop[movie_info['popularity_int'].values[0]] += 1/10
        distbud[movie_info['popularity_budget_inf'].values[0]] += 1/10
        recommendation_data.append(
            {
                'imdb_id': movie_info['imdb'].values[0],
                'title': movie_info['title'].values[0] + f" ({movie_info['year'].values[0]})",
                'description': movie_info['overview'].values[0],
                'poster': movie_info['poster_w500'].values[0],
                'trailer': "https://www.youtube.com/watch?v="+movie_info['youtubeId'].values[0],
                'director': movie_info['director'].values[0],
                'cast': movie_info['actors'].values[0].replace(" (Ator/Atriz)", "").split("|")[:3],
                'popularity_level': pop_map[movie_info['popularity_int'].values[0]],
                'budget_level': pop_map[movie_info['popularity_budget_inf'].values[0]],
                'rating': 0,
                'genres': movie_info['genres'].values[0].split("|")
            }
        )
    
    del selected_items
    del distpop
    del distbud
    gc.collect()

    return {'message': 'recommendation generated', 'data': recommendation_data}
