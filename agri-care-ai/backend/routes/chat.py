from fastapi import APIRouter
from pydantic import BaseModel
import os

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])


class ChatRequest(BaseModel):
    message: str
    language: str = "en"


def get_fallback_response(message: str, language: str):
    text = message.lower()

    if any(word in text for word in [
        "poison",
        "poisoning",
        "swallowed",
        "ingested",
        "chemical",
        "pesticide poisoning",
    ]):
        if language == "hi":
            return (
                "⚠️ यह जहर/रसायन से जुड़ी आपात स्थिति हो सकती है। "
                "इस chatbot पर निर्भर न रहें। तुरंत स्थानीय emergency "
                "medical service या poison information centre से संपर्क करें। "
                "व्यक्ति को बिना medical advice के उल्टी कराने की कोशिश न करें।"
            )

        return (
            "⚠️ This may be a poisoning or chemical exposure emergency. "
            "Do not rely on this chatbot. Contact local emergency medical "
            "services or a poison information centre immediately. "
            "Do not induce vomiting unless instructed by a medical professional."
        )

    if any(word in text for word in [
        "dose",
        "dosage",
        "how much pesticide",
        "per acre",
        "ml per",
        "gram per",
        "litre",
        "mix",
    ]):
        if language == "hi":
            return (
                "⚠️ मैं pesticide की exact dose, mixing ratio या per-acre "
                "मात्रा नहीं बता सकता। सही मात्रा हमेशा संबंधित registered "
                "product के official label और स्थानीय कृषि विशेषज्ञ की सलाह "
                "के अनुसार तय करें।"
            )

        return (
            "⚠️ I can't provide an exact pesticide dose, mixing ratio, "
            "or per-acre quantity. Use the registered product's official "
            "label and follow guidance from a qualified local agriculture expert."
        )

    if any(word in text for word in [
        "yellow",
        "yellowing",
        "leaves turning yellow",
    ]):
        if language == "hi":
            return (
                "🌾 पत्तियाँ पीली होने के कई कारण हो सकते हैं, जैसे पानी की "
                "समस्या, पोषक तत्वों की कमी, जड़ की समस्या या कुछ कीट/रोग। "
                "फसल की अवस्था, मिट्टी की नमी और पत्तियों के अन्य लक्षण देखें। "
                "यदि समस्या बढ़ रही है तो स्थानीय कृषि विशेषज्ञ से पुष्टि करें।"
            )

        return (
            "🌾 Yellow leaves can have several causes, including water stress, "
            "nutrient deficiency, root problems, or certain pests and diseases. "
            "Check the crop stage, soil moisture, and other leaf symptoms. "
            "If the problem is spreading, verify it with a local agriculture expert."
        )

    if any(word in text for word in [
        "rice",
        "paddy",
    ]):
        if language == "hi":
            return (
                "🌾 चावल की फसल के लिए लक्षणों के साथ फसल की अवस्था बताना "
                "उपयोगी होगा। उदाहरण: 'धान की vegetative stage में पत्तियाँ "
                "पीली और सूखी हो रही हैं।' इससे संभावित समस्या को बेहतर समझा जा सकता है।"
            )

        return (
            "🌾 For rice, it helps to provide the crop stage together with "
            "the symptoms. For example: 'Rice is in the vegetative stage "
            "and leaves are turning yellow and drying.' This helps narrow "
            "down the possible issue."
        )

    if any(word in text for word in [
        "weather",
        "rain",
        "temperature",
        "humidity",
        "wind",
    ]):
        if language == "hi":
            return (
                "🌦️ मौसम की स्थिति crop-care decisions को प्रभावित कर सकती है। "
                "तेज हवा या बारिश के दौरान spraying से बचना और बहुत अधिक तापमान "
                "में सावधानी रखना उपयोगी है।"
            )

        return (
            "🌦️ Weather conditions can affect crop-care decisions. "
            "Avoid spraying during strong winds or rain, and use caution "
            "during very high temperatures."
        )

    if language == "hi":
        return (
            "🌱 मैं फसल के लक्षण, कीट, रोग और मौसम से जुड़े सामान्य crop-care "
            "सवालों में मदद कर सकता हूँ। अपनी फसल और उसके लक्षण बताइए।"
        )

    return (
        "🌱 I can help with general crop symptoms, pests, diseases, "
        "and weather-related crop-care questions. Tell me the crop "
        "and describe its symptoms."
    )


@router.post("")
async def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        return {
            "status": "success",
            "reply": (
                "Please enter a crop-care question."
                if request.language != "hi"
                else "कृपया फसल से जुड़ा सवाल लिखें।"
            ),
        }

    reply = get_fallback_response(
        message,
        request.language if request.language in ["en", "hi"] else "en",
    )

    return {
        "status": "success",
        "reply": reply,
        "source": "safe-rule-based-assistant",
    }