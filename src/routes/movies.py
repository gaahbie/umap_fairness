from fastapi import APIRouter, Depends, HTTPException
import uuid
from scipy.stats import multinomial
import pandas as pd
import unidecode


router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    responses={404: {"description": "Not found"}},
)

# Mock DB
# Should change later to a postgresSQL
data = pd.read_csv("./data/items.csv", lineterminator='\n')
data['title_l'] = data['title'].apply(lambda x: unidecode.unidecode(x.lower()))


@router.get("/{imdb_id}")
async def get_movie_by_imdb_id(imdb_id):
    selected_movie = data[data['imdb'] == imdb_id]
    
    return {
        'imdb_id': imdb_id,
        'title': selected_movie['title'].values[0]+ f" ({selected_movie['year'].values[0]})",
        'description': selected_movie['overview'].values[0],
        'poster': selected_movie['poster_w500'].values[0],
        'trailer': "https://www.youtube.com/watch?v="+selected_movie['youtubeId'].values[0],
        'rating': 0
    }


@router.get("")
async def search_movie(search: str, skip: int = 0, limit: int = 10):

    selected_movies = data[data["title_l"].str.contains(unidecode.unidecode(search.lower()))]

    datas = []

    for index, row in list(selected_movies.iterrows())[skip: skip+limit]:
        datas.append(
            {
                'imdb_id': row['imdb'],
                'title': row['title'] + f" ({row['year']})",
                'description': row['overview'],
                'poster': row['poster_w500'],
                'trailer': "https://www.youtube.com/watch?v="+row['youtubeId'],
                'rating': 0
            }
        )
    
    return datas
