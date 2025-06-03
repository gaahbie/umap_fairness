from sqlalchemy.orm import Session
import time
from src.db import models, schemas


def add_interaction(db: Session, interaction: schemas.InteractionCreate):
    interaction_data = models.ItemInteractions(
        added_timestamp=int(time.time()),
        user_experiment_id=interaction.user_id,
        item_id=interaction.item_id,
        rating=interaction.rating
    )
    db.add(interaction_data)
    db.commit()
    db.refresh(interaction_data)

    return interaction_data

def get_interactions(db: Session, exp_id: str):
        return db.query(models.ItemInteractions).filter(models.ItemInteractions.user_experiment_id == exp_id).all()

def create_user(db: Session, user: schemas.UserCreate):
    user_data = models.User(
        started_timestamp=int(time.time()),
        experiment_id=user.experiment_id,
        experiment_type=user.experiment_type,
        email=user.email
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return user_data

def get_user(db: Session, exp_id: str):
    return db.query(models.User).filter(models.User.experiment_id == exp_id).first()

def get_all_user(db: Session):
    return db.query(models.User).all()


def create_popularity(db: Session, dist: schemas.AddPopularity):

    response = db.query(models.UserPopularityDistribution).filter(
        models.UserPopularityDistribution.user_experiment_id == dist.experiment_id
    ).first()

    if response is None:
        dist_data = models.UserPopularityDistribution(
            user_experiment_id=dist.experiment_id,
            H=dist.H,
            M=dist.M,
            T=dist.T
        )
        db.add(dist_data)
        db.commit()
        db.refresh(dist_data)
        return dist_data

    else:
        response.H = dist.H
        response.M = dist.M
        response.T = dist.T
        db.commit()

def get_popularity(db: Session, exp_id: str):
    data = db.query(models.UserPopularityDistribution).filter(
        models.UserPopularityDistribution.user_experiment_id == exp_id
    ).first()
    return {
        "H": data.H,
        "M": data.M,
        "T": data.T,
    }


def create_popularity_budget(db: Session, dist: schemas.AddPopularity):

    response = db.query(models.UserBudgetDistribution).filter(
        models.UserBudgetDistribution.user_experiment_id == dist.experiment_id
    ).first()

    if response is None:
        dist_data = models.UserBudgetDistribution(
            user_experiment_id=dist.experiment_id,
            H=dist.H,
            M=dist.M,
            T=dist.T
        )
        db.add(dist_data)
        db.commit()
        db.refresh(dist_data)
        return dist_data

    else:
        response.H = dist.H
        response.M = dist.M
        response.T = dist.T
        db.commit()

def get_popularity_budget(db: Session, exp_id: str):
    data = db.query(models.UserBudgetDistribution).filter(
        models.UserBudgetDistribution.user_experiment_id == exp_id
    ).first()

    return {
        "H": data.H,
        "M": data.M,
        "T": data.T,
    }


def store_demographic(db: Session, data, user_id):
    for quest in data.demographicQuestions:
        question = quest.question
        answer = quest.answer

        question_data = models.UserDemographicAnswer(
            user_id = user_id,
            experiment_question = question,
            experiment_answer = answer,
        )
        db.add(question_data)
        db.commit()
        db.refresh(question_data)


def store_recommendation(db: Session, data, user_id):

    for quest in data.recommendationQuestions:
        question = quest.question
        answer = quest.answer

        question_data = models.UserRecommendationAnswer(
            user_id = user_id,
            experiment_question = question,
            experiment_answer = answer,
        )
        db.add(question_data)
        db.commit()
        db.refresh(question_data)


def store_selected_recommendation(db: Session, data, user_id):
    selected_data = models.SelectedRecommendationAnswer(
        user_id = user_id,
        movie_selected = data.selected_movie,
    )
    db.add(selected_data)
    db.commit()
    db.refresh(selected_data)

    for movie in data.recommendations:
        item_id = movie.imdb_id
        watched_the_movie = movie.watched_the_movie

        question_data = models.WatchedRecommendationAnswer(
            user_id = user_id,
            item_id = item_id,
            watched_the_movie = watched_the_movie,
        )
        db.add(question_data)
        db.commit()
        db.refresh(question_data)