from sqlalchemy import Boolean, Column, Integer, String, Float

from .database import Base

class User(Base):
    __tablename__ = 'users'

    started_timestamp = Column(Integer)
    experiment_id = Column(String, primary_key=True, index=True)
    experiment_type = Column(Integer)
    email = Column(String)


class UserPopularityDistribution(Base):
    __tablename__ = 'userdistribution_pop'

    user_experiment_id = Column(String, index=True, primary_key=True)
    H = Column(Float)
    M = Column(Float)
    T = Column(Float)

class UserBudgetDistribution(Base):
    __tablename__ = 'userdistribution_budget'

    user_experiment_id = Column(String, index=True, primary_key=True)
    H = Column(Float)
    M = Column(Float)
    T = Column(Float)


class ItemInteractions(Base):
    __tablename__ = 'interactions'

    id = Column(Integer, primary_key=True)
    added_timestamp = Column(Integer)
    user_experiment_id = Column(String, index=True)
    item_id = Column(String)
    rating = Column(Integer)


class UserDemographicAnswer(Base):
    __tablename__ = 'demographic_answer'

    id = Column(Integer, primary_key=True)
    user_id = Column(String,  index=True)
    experiment_question = Column(String)
    experiment_answer = Column(String)

class UserRecommendationAnswer(Base):
    __tablename__ = 'recommendation_answer'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    experiment_question = Column(String)
    experiment_answer = Column(String)


class SelectedRecommendationAnswer(Base):
    __tablename__ = 'selected_recommendation_answer'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    movie_selected = Column(String)


class WatchedRecommendationAnswer(Base):
    __tablename__ = 'watched_recommendation_answer'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    item_id = Column(String)
    watched_the_movie = Column(Boolean)

