from database.db import SessionLocal
from models.models import Crop, GrowthStage


def seed_stages():
    db = SessionLocal()

    stages = {
        "Rice": [
            ("Germination", 1, "0-10"),
            ("Vegetative", 2, "10-45"),
            ("Reproductive", 3, "45-80"),
            ("Maturity", 4, "80-120"),
        ],
        "Wheat": [
            ("Germination", 1, "0-15"),
            ("Tillering", 2, "15-45"),
            ("Flowering", 3, "45-80"),
            ("Grain Filling", 4, "80-110"),
            ("Maturity", 5, "110-140"),
        ],
        "Tomato": [
            ("Seedling", 1, "0-30"),
            ("Vegetative", 2, "30-50"),
            ("Flowering", 3, "50-70"),
            ("Fruit Development", 4, "70-100"),
            ("Maturity", 5, "100-130"),
        ],
    }

    for crop_name, crop_stages in stages.items():
        crop = db.query(Crop).filter(Crop.name == crop_name).first()

        if crop:
            for name, order, duration in crop_stages:
                existing = (
                    db.query(GrowthStage)
                    .filter(
                        GrowthStage.crop_id == crop.id,
                        GrowthStage.order == order
                    )
                    .first()
                )

                if not existing:
                    db.add(
                        GrowthStage(
                            crop_id=crop.id,
                            name=name,
                            order=order,
                            typical_duration_days=duration
                        )
                    )

    db.commit()
    db.close()

    print("Growth stage data seeded successfully.")


if __name__ == "__main__":
    seed_stages()