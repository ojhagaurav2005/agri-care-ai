from database.db import SessionLocal
from models.models import ProductPrice

db = SessionLocal()

prices = [
    ProductPrice(
        treatment_id=1,
        unit="per acre",
        price_inr=300,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=2,
        unit="per acre",
        price_inr=250,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=3,
        unit="per acre",
        price_inr=400,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=4,
        unit="per acre",
        price_inr=350,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=5,
        unit="per acre",
        price_inr=250,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=6,
        unit="per acre",
        price_inr=500,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=7,
        unit="per acre",
        price_inr=300,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=8,
        unit="per acre",
        price_inr=250,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=9,
        unit="per acre",
        price_inr=300,
        updated_note="Demo estimate - verify current local price"
    ),
    ProductPrice(
        treatment_id=10,
        unit="per acre",
        price_inr=350,
        updated_note="Demo estimate - verify current local price"
    )
]

db.add_all(prices)
db.commit()
db.close()

print("Product prices seeded successfully.")