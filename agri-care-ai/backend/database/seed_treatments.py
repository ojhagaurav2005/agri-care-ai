from database.db import SessionLocal
from models.models import PestDisease, Treatment


def seed_treatments():
    db = SessionLocal()

    treatment_data = {
        "Rice Stem Borer": [
            (
                "Cultural",
                "Field sanitation and removal of heavily affected tillers",
                None,
                "Remove and destroy severely affected plant parts where practical.",
                "Regular monitoring is important."
            ),
            (
                "Biological",
                "Encourage natural enemies",
                None,
                "Conserve beneficial insects and avoid unnecessary broad-spectrum pesticide use.",
                "Use integrated pest management practices."
            )
        ],
        "Brown Planthopper": [
            (
                "Cultural",
                "Avoid excessive nitrogen and maintain proper spacing",
                None,
                "Maintain balanced fertilizer use and avoid excessive nitrogen application.",
                "Monitor fields regularly."
            )
        ],
        "Rice Blast": [
            (
                "Cultural",
                "Balanced nutrient management",
                None,
                "Avoid excessive nitrogen and maintain proper field management.",
                "Use resistant varieties where available."
            )
        ],
        "Aphids": [
            (
                "Cultural",
                "Monitor and conserve beneficial insects",
                None,
                "Remove heavily infested plant parts where practical and conserve natural enemies.",
                "Check leaves and spikes regularly."
            )
        ],
        "Wheat Rust": [
            (
                "Cultural",
                "Use resistant varieties",
                None,
                "Prefer locally recommended resistant varieties where available.",
                "Monitor fields regularly."
            )
        ],
        "Fruit Borer": [
            (
                "Cultural",
                "Remove damaged fruits",
                None,
                "Collect and destroy infested fruits and monitor plants regularly.",
                "Use integrated pest management practices."
            ),
            (
                "Biological",
                "Encourage beneficial insects",
                None,
                "Conserve natural enemies and use biological control where locally recommended.",
                "Avoid unnecessary broad-spectrum pesticide use."
            )
        ],
        "Whitefly": [
            (
                "Cultural",
                "Remove heavily infested leaves",
                None,
                "Remove severely infested leaves where practical and monitor the underside of leaves.",
                "Monitor regularly."
            )
        ],
        "Early Blight": [
            (
                "Cultural",
                "Remove infected plant debris",
                None,
                "Remove infected leaves and plant debris and maintain good field sanitation.",
                "Avoid working with wet foliage."
            )
        ]
    }

    for pest_name, treatments in treatment_data.items():
        pest = (
            db.query(PestDisease)
            .filter(PestDisease.name == pest_name)
            .first()
        )

        if pest:
            for category, method_name, active_ingredient, precautions, note in treatments:
                existing = (
                    db.query(Treatment)
                    .filter(
                        Treatment.pest_id == pest.id,
                        Treatment.method_name == method_name
                    )
                    .first()
                )

                if not existing:
                    db.add(
                        Treatment(
                            pest_id=pest.id,
                            category=category,
                            method_name=method_name,
                            active_ingredient=active_ingredient,
                            application_timing="Apply according to locally recommended practice.",
                            dosage_note="Verify with product label or local agricultural advisory.",
                            precautions=precautions,
                            pre_harvest_interval_days=None,
                            is_verified="demo"
                        )
                    )

    db.commit()
    db.close()

    print("Treatment data seeded successfully.")


if __name__ == "__main__":
    seed_treatments()