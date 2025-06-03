from fastapi import APIRouter, Depends, HTTPException
import uuid
from scipy.stats import multinomial
from pydantic import BaseModel
from typing import Optional
from src.db import crud, models, schemas
from src.db.database import SessionLocal, engine
from src.db.utils import get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



router = APIRouter(
    prefix="/ab_testing",
    tags=["A/B Testing"],
    responses={404: {"description": "Not found"}},
)

class UserInfo(BaseModel):
    email: Optional[str] = None

@router.post("/")
async def generate_experiment_token(user_info: Optional[UserInfo], db: Session = Depends(get_db)):
    id_ = uuid.uuid4()
    
    response = crud.get_all_user(db)
    if len(response) == 0:
        rv = list(multinomial.rvs(1, p=[1/6, 1/6, 1/6, 1/6, 1/6, 1/6], size=1)[0])
        rv = rv.index(1)
    else:
        exps_dist = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
        for i in response:
            exps_dist[i.experiment_type] += 1
                
        last_choose_exp = min([exps_dist[i] for i in exps_dist])
        need_to_choose_exps = [k for k in exps_dist if exps_dist[k] == last_choose_exp]

        rv = list(multinomial.rvs(1, p=[1/len(need_to_choose_exps) for i in need_to_choose_exps], size=1)[0])
        rv = need_to_choose_exps[rv.index(1)]

    crud.create_user(
        db, schemas.UserCreate(
            experiment_id=str(id_),
            experiment_type=rv,
            email=user_info.email if user_info.email is not None else "NA"
        )
    )
    print(f"Usuario de ID: {id_} foi para experimento: {rv}")
    return {"token": id_, 'experiment': rv}


@router.get("/{id}")
async def get_experiment_info(id: str, db: Session = Depends(get_db)):
    result = crud.get_user(db, id)
    return result