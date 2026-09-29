from database.db import SessionLocal
from models.models import Crop


def seed_crops():
    db = SessionLocal()

    crops = [
        Crop(
            name="Rice",
            season="Kharif",
            description="Rice is a major cereal crop commonly grown during the monsoon season."
        ),
        Crop(
            name="Wheat",
            season="Rabi",
            description="Wheat is a major winter cereal crop grown during the Rabi season."
        ),
        Crop(
            name="Tomato",
            season="Rabi/Kharif",
            description="Tomato is a vegetable crop affected by several insect pests and diseases."
        )
    ]

    for crop in crops:
        existing = db.query(Crop).filter(Crop.name == crop.name).first()
        if not existing:
            db.add(crop)

    db.commit()
    db.close()

    print("Crop data seeded successfully.")


if __name__ == "__main__":
    seed_crops()