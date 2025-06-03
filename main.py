from fastapi import Depends, FastAPI
from src.routes.ab_testing import router as ab_route
from src.routes.movies import router as movie_route
from src.routes.profile import router as profile_route
from src.routes.questionnaire import router as questionnaire_route
from src.routes.recommendation import router as recommendation_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ab_route)
app.include_router(movie_route)
app.include_router(profile_route)
app.include_router(recommendation_route)
app.include_router(questionnaire_route)