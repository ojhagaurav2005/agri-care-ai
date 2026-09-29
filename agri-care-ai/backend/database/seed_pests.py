from database.db import SessionLocal
from models.models import Crop, PestDisease


def seed_pests():
    db = SessionLocal()

    pest_data = {
        "Rice": [
            (
                "Rice Stem Borer",
                "Pest",
                "Dead hearts in vegetative stage and white ear heads during reproductive stage.",
                "Vegetative/Reproductive",
                "Monitor dead hearts and white ear heads regularly."
            ),
            (
                "Brown Planthopper",
                "Pest",
                "Yellowing and drying of plants, often starting in patches.",
                "Vegetative/Reproductive",
                "Inspect the base of plants for planthoppers and hopper burn."
            ),
            (
                "Rice Blast",
                "Disease",
                "Spindle-shaped lesions on leaves and lesions on neck or panicle.",
                "Vegetative/Reproductive",
                "Regularly inspect leaves and panicles for characteristic lesions."
            )
        ],
        "Wheat": [
            (
                "Aphids",
                "Pest",
                "Small insects on leaves and spikes with curling or yellowing symptoms.",
                "Vegetative/Reproductive",
                "Inspect leaves and spikes for aphid colonies."
            ),
            (
                "Wheat Rust",
                "Disease",
                "Rust-colored or yellow-orange pustules appearing on leaves.",
                "Vegetative/Reproductive",
                "Regularly inspect leaves for rust pustules."
            )
        ],
        "Tomato": [
            (
                "Fruit Borer",
                "Pest",
                "Holes in fruits with caterpillar feeding inside the fruit.",
                "Flowering/Fruit Development",
                "Inspect flowers and fruits regularly for eggs, larvae, and feeding damage."
            ),
            (
                "Whitefly",
                "Pest",
                "Small white insects on the underside of leaves with yellowing and curling.",
                "Vegetative/Flowering",
                "Check the underside of leaves for whiteflies."
            ),
            (
                "Early Blight",
                "Disease",
                "Dark spots with concentric rings on older leaves.",
                "Vegetative/Fruiting",
                "Inspect lower leaves regularly for characteristic spots."
            )
        ]
    }

    for crop_name, pests in pest_data.items():
        crop = db.query(Crop).filter(Crop.name == crop_name).first()

        if crop:
            for name, pest_type, symptoms, stage, monitoring in pests:
                existing = (
                    db.query(PestDisease)
                    .filter(
                        PestDisease.crop_id == crop.id,
                        PestDisease.name == name
                    )
                    .first()
                )

                if not existing:
                    db.add(
                        PestDisease(
                            crop_id=crop.id,
                            name=name,
                            type=pest_type,
                            symptoms=symptoms,
                            affected_stage=stage,
                            monitoring_method=monitoring
                        )
                    )

    db.commit()
    db.close()

    print("Pest and disease data seeded successfully.")


if __name__ == "__main__":
    seed_pests()