from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.db import get_db
from models.models import Crop, PestDisease, ProductPrice
from ml.predict import predict_disease

import requests


router = APIRouter(
    prefix="/advice",
    tags=["Advice"]
)


class AdviceRequest(BaseModel):
    location: str
    crop: str
    landSize: float
    unit: str
    growthStage: str = ""
    symptoms: str = ""


def get_weather(location):
    try:
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geocode_url,
            params={
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10,
            headers={
                "User-Agent": "AI-Crop-Care-Advisor/1.0"
            }
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {
                "available": False,
                "message": (
                    "Weather data could not be found "
                    "for this location."
                )
            }

        place = geo_data["results"][0]

        latitude = place["latitude"]
        longitude = place["longitude"]

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "precipitation,"
                    "rain,"
                    "showers,"
                    "wind_speed_10m"
                ),
                "daily": (
                    "precipitation_probability_max,"
                    "precipitation_sum,"
                    "temperature_2m_max"
                ),
                "forecast_days": 1,
                "timezone": "auto"
            },
            timeout=10,
            headers={
                "User-Agent": "AI-Crop-Care-Advisor/1.0"
            }
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

        current = weather_data["current"]
        daily = weather_data["daily"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        precipitation = current["precipitation"]

        rain_probability = (
            daily["precipitation_probability_max"][0]
        )

        rain_forecast = (
            daily["precipitation_sum"][0]
        )

        alerts = []

        if (
            rain_forecast >= 10
            or rain_probability >= 70
        ):
            alerts.append({
                "type": "rain",
                "severity": "high",
                "icon": "🌧️",
                "title": "Rain Alert",
                "message": (
                    "Rain is expected. Avoid or delay "
                    "spraying when rainfall is imminent "
                    "and follow the product label."
                )
            })

        if humidity >= 80:
            alerts.append({
                "type": "humidity",
                "severity": "medium",
                "icon": "💧",
                "title": "High Humidity",
                "message": (
                    "High humidity can favor some "
                    "fungal diseases. Monitor the crop "
                    "closely."
                )
            })

        if temperature >= 35:
            alerts.append({
                "type": "temperature",
                "severity": "high",
                "icon": "🌡️",
                "title": "High Temperature",
                "message": (
                    "High temperature may increase "
                    "crop heat stress."
                )
            })

        if wind_speed >= 20:
            alerts.append({
                "type": "wind",
                "severity": "high",
                "icon": "💨",
                "title": "Strong Wind",
                "message": (
                    "Strong wind can cause spray drift. "
                    "Avoid spraying during strong winds."
                )
            })

        if not alerts:
            alerts.append({
                "type": "suitable",
                "severity": "low",
                "icon": "☀️",
                "title": "Weather Suitable",
                "message": (
                    "Current weather conditions appear "
                    "suitable for normal field operations. "
                    "Always check the product label."
                )
            })

        return {
            "available": True,
            "location": place.get("name"),
            "region": place.get("admin1"),
            "country": place.get("country"),
            "temperature_c": temperature,
            "humidity_percent": humidity,
            "wind_speed_kmh": wind_speed,
            "current_precipitation_mm": precipitation,
            "rain_probability_percent": rain_probability,
            "rain_forecast_mm": rain_forecast,
            "alerts": alerts
        }

    except requests.RequestException as error:
        print("Weather API error:", error)

        return {
            "available": False,
            "message": (
                "Weather service could not be reached."
            )
        }

    except Exception as error:
        print("Weather processing error:", error)

        return {
            "available": False,
            "message": (
                "Live weather data is temporarily unavailable."
            )
        }


def symptom_match(
    user_symptoms,
    pest_symptoms
):
    if not user_symptoms:
        return False

    user_words = set(
        user_symptoms.lower().split()
    )

    pest_words = set(
        pest_symptoms.lower().split()
    )

    common_words = (
        user_words.intersection(
            pest_words
        )
    )

    useful_words = {
        "yellow",
        "yellowing",
        "drying",
        "curling",
        "spots",
        "lesions",
        "holes",
        "rust",
        "pustules",
        "insects",
        "caterpillar",
        "dead",
        "white",
    }

    matched_words = (
        common_words.intersection(
            useful_words
        )
    )

    return len(matched_words) > 0


@router.post("")
def get_advice(
    request: AdviceRequest,
    db: Session = Depends(get_db)
):

    print(
        "Advice request:",
        request.model_dump()
    )

    ml_result = None

    if request.symptoms:

        try:
            ml_result = predict_disease(
                request.symptoms
            )

            if (
                ml_result["confidence"]
                < 40
            ):
                ml_result["prediction"] = None

        except Exception as error:
            print(
                "ML prediction error:",
                error
            )

            ml_result = None

    crop = (
        db.query(Crop)
        .filter(
            Crop.name == request.crop
        )
        .first()
    )

    if not crop:
        return {
            "status": "error",
            "message": (
                f"Crop '{request.crop}' "
                "was not found in database."
            )
        }

    pests = (
        db.query(PestDisease)
        .filter(
            PestDisease.crop_id == crop.id
        )
        .all()
    )

    matched_pests = []

    for pest in pests:

        if symptom_match(
            request.symptoms,
            pest.symptoms
        ):
            matched_pests.append(
                pest
            )

    pest_data = []

    lowest_treatment_cost = None

    for pest in matched_pests:

        treatment_data = []

        for treatment in pest.treatments:

            price = (
                db.query(ProductPrice)
                .filter(
                    ProductPrice.treatment_id
                    == treatment.id
                )
                .first()
            )

            treatment_cost = None

            if (
                price
                and request.unit.lower()
                in ["acre", "acres"]
            ):

                treatment_cost = round(
                    price.price_inr
                    * request.landSize,
                    2
                )

                if (
                    lowest_treatment_cost
                    is None
                    or treatment_cost
                    < lowest_treatment_cost
                ):
                    lowest_treatment_cost = (
                        treatment_cost
                    )

            treatment_data.append({
                "method": getattr(
                    treatment,
                    "method_name",
                    None
                ),
                "category": getattr(
                    treatment,
                    "category",
                    None
                ),
                "active_ingredient": getattr(
                    treatment,
                    "active_ingredient",
                    None
                ),
                "timing": getattr(
                    treatment,
                    "application_timing",
                    None
                ),
                "precautions": getattr(
                    treatment,
                    "precautions",
                    None
                ),
                "estimated_cost": (
                    treatment_cost
                ),
                "cost_unit": (
                    price.unit
                    if price
                    else None
                )
            })

        pest_data.append({
            "id": pest.id,
            "name": pest.name,
            "type": pest.type,
            "symptoms": pest.symptoms,
            "description": getattr(
                pest,
                "description",
                None
            ),
            "monitoring_method": getattr(
                pest,
                "monitoring_method",
                None
            ),
            "treatments": treatment_data
        })

    weather = get_weather(
        request.location
    )

    disease = None

    if ml_result:
        disease = (
            ml_result.get("prediction")
        )

    smart_advisory = ""

    if weather.get("available"):

        temperature = weather.get(
            "temperature_c",
            0
        )

        humidity = weather.get(
            "humidity_percent",
            0
        )

        wind_speed = weather.get(
            "wind_speed_kmh",
            0
        )

        rain_probability = weather.get(
            "rain_probability_percent",
            0
        )

        rain_forecast = weather.get(
            "rain_forecast_mm",
            0
        )

        if disease:

            if humidity >= 80:

                smart_advisory = (
                    f"⚠️ Weather + Disease Alert: "
                    f"Possible {disease} detected and "
                    f"humidity is high. Monitor the "
                    f"affected crop parts closely."
                )

            elif (
                rain_probability >= 70
                or rain_forecast >= 10
            ):

                smart_advisory = (
                    f"🌧️ Treatment Timing Alert: "
                    f"Possible {disease} detected, "
                    f"but rain is expected. Avoid or "
                    f"delay spraying when rainfall "
                    f"is imminent."
                )

            elif wind_speed >= 20:

                smart_advisory = (
                    f"💨 Spray Advisory: Possible "
                    f"{disease} detected, but wind "
                    f"speed is high. Avoid spraying "
                    f"during strong winds."
                )

            elif temperature >= 35:

                smart_advisory = (
                    f"🌡️ Heat Advisory: Possible "
                    f"{disease} detected. Current "
                    f"temperature is high. Monitor "
                    f"the crop for heat stress."
                )

            else:

                smart_advisory = (
                    f"🌾 Smart Advisory: Possible "
                    f"{disease} detected. Continue "
                    f"crop monitoring and follow "
                    f"locally recommended practices."
                )

        else:

            if humidity >= 80:

                smart_advisory = (
                    "💧 Weather Risk Advisory: "
                    "High humidity may create "
                    "favorable conditions for some "
                    "fungal diseases."
                )

            elif rain_probability >= 70:

                smart_advisory = (
                    "🌧️ Rain Advisory: Rain is "
                    "expected. Consider delaying "
                    "spraying until suitable "
                    "weather conditions."
                )

            elif wind_speed >= 20:

                smart_advisory = (
                    "💨 Wind Advisory: Strong winds "
                    "are present. Avoid spraying "
                    "during strong winds."
                )

            elif temperature >= 35:

                smart_advisory = (
                    "🌡️ Heat Advisory: High "
                    "temperature may increase "
                    "crop stress."
                )

            else:

                smart_advisory = (
                    "☀️ Smart Advisory: No major "
                    "weather risk was detected "
                    "from the current conditions."
                )

    else:

        smart_advisory = (
            "ℹ️ Smart advisory is unavailable "
            "because live weather data could "
            "not be retrieved."
        )

    spray_recommendation = (
        "Suitable for spraying"
    )

    if weather.get("available"):

        if (
            weather.get(
                "wind_speed_kmh",
                0
            ) >= 20
            or weather.get(
                "rain_probability_percent",
                0
            ) >= 70
            or weather.get(
                "rain_forecast_mm",
                0
            ) >= 10
        ):

            spray_recommendation = (
                "Avoid spraying under the "
                "current weather conditions"
            )

        elif weather.get(
            "temperature_c",
            0
        ) >= 35:

            spray_recommendation = (
                "Use caution with spraying "
                "because of high temperature"
            )

    if request.unit.lower() in [
        "acre",
        "acres"
    ]:

        cost_note = (
            "Estimated cost based on demo "
            "treatment prices. Verify current "
            "local prices before purchase."
        )

    else:

        cost_note = (
            "Cost estimation currently supports "
            "acres. Bigha conversion varies by "
            "region, so verify the local "
            "conversion before using the estimate."
        )

    if disease:

        why_result = (
            f"The ML model found a possible "
            f"match for '{disease}' from the "
            f"symptoms entered. The confidence "
            f"score is {ml_result['confidence']}%. "
            f"This is only a possible match and "
            f"should be verified."
        )

    elif matched_pests:

        why_result = (
            "Possible pest or disease matches "
            "were found because some symptom "
            "keywords matched the crop database."
        )

    else:

        why_result = (
            "No specific pest or disease match "
            "was found from the entered symptoms. "
            "The issue may also be related to "
            "water, soil, nutrients, seed quality "
            "or other growing conditions."
        )

    return {
        "status": "success",

        "message": (
            f"Crop advice generated for "
            f"{request.crop}."
        ),

        "crop": request.crop,

        "location": request.location,

        "land_size": request.landSize,

        "unit": request.unit,

        "growth_stage": request.growthStage,

        "symptoms": request.symptoms,

        "ml_prediction": (
            disease
            if ml_result
            else None
        ),

        "ml_confidence": (
            ml_result["confidence"]
            if ml_result
            else None
        ),

        "pests": pest_data,

        "pests_and_diseases": pest_data,

        "estimated_cost": (
            round(
                lowest_treatment_cost,
                2
            )
            if lowest_treatment_cost
            is not None
            else 0
        ),

        "total_estimated_cost": (
            round(
                lowest_treatment_cost,
                2
            )
            if lowest_treatment_cost
            is not None
            else 0
        ),

        "cost_note": cost_note,

        "weather": weather,

        "spray_recommendation":
            spray_recommendation,

        "smart_advisory":
            smart_advisory,

        "why_result":
            why_result,

        "advice_note": (
            "Possible pest or disease "
            "matches are shown based on "
            "the symptoms entered."
            if matched_pests
            else
            "No specific pest or disease "
            "match was found from the "
            "symptoms entered."
        )
    }