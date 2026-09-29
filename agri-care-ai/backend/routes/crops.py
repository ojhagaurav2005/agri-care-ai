from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from models.models import Crop

router = APIRouter(prefix="/crops", tags=["Crops"])


@router.get("/")
def get_crops(db: Session = Depends(get_db)):
    crops = db.query(Crop).all()

    return [
        {
            "id": crop.id,
            "name": crop.name,
            "season": crop.season,
            "description": crop.description,
            "growth_stages": [
                {
                    "name": stage.name,
                    "order": stage.order,
                    "duration_days": stage.typical_duration_days
                }
                for stage in sorted(
                    crop.growth_stages,
                    key=lambda stage: stage.order
                )
            ]
        }
        for crop in crops
    ]