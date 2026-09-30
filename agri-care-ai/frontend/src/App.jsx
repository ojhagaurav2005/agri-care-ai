import { useEffect, useState } from "react";
import axios from "axios";
import Chatbot from "./components/Chatbot";

const API_URL = "https://agrii-care-ai.onrender.com

const translations = {
  en: {
    title: "AI Crop Care Advisor",
    subtitle: "Smart crop guidance for farmers",
    location: "Location",
    crop: "Crop",
    landSize: "Land Size",
    unit: "Unit",
    growthStage: "Growth Stage",
    symptoms: "Symptoms",
    symptomsPlaceholder:
      "Example: yellow leaves, holes in leaves, spindle shaped lesions...",
    getAdvice: "Get Crop Advice",
    analyzing: "Analyzing Crop...",
    cropSelect: "Select Crop",
    stageSelect: "Select Growth Stage",
    acres: "Acres",
    bigha: "Bigha",
    results: "Crop Advice",
    estimatedCost: "Estimated Treatment Cost",
    weather: "Weather Advisory",
    spray: "Spray Recommendation",
    smart: "Smart Advisory",
    ai: "AI Prediction",
    why: "Why this result?",
    pests: "Possible Pests & Diseases",
    confidence: "AI Confidence",
    confidenceLevel: "Confidence Level",
    high: "High",
    moderate: "Moderate",
    low: "Low",
    noPrediction: "No reliable AI prediction",
    disclaimer:
      "This is an AI-generated possible match, not a confirmed diagnosis. Verify the symptoms with a local agriculture expert before taking treatment action.",
    weatherUnavailable: "Weather information is currently unavailable.",
    invalidLand: "Please enter a valid land size.",
    requiredLocation: "Please enter your location.",
    requiredCrop: "Please select a crop.",
    requiredStage: "Please select a growth stage.",
    requiredSymptoms: "Please enter crop symptoms.",
    backendError:
      "Unable to get crop advice. Please check the backend server.",
    language: "हिंदी",
  },

  hi: {
    title: "AI फसल देखभाल सलाहकार",
    subtitle: "किसानों के लिए स्मार्ट फसल सलाह",
    location: "स्थान",
    crop: "फसल",
    landSize: "भूमि का क्षेत्रफल",
    unit: "इकाई",
    growthStage: "फसल की अवस्था",
    symptoms: "लक्षण",
    symptomsPlaceholder:
      "उदाहरण: पत्तियाँ पीली हैं, पत्तियों में छेद हैं, लंबे धब्बे हैं...",
    getAdvice: "फसल की सलाह प्राप्त करें",
    analyzing: "फसल का विश्लेषण हो रहा है...",
    cropSelect: "फसल चुनें",
    stageSelect: "फसल की अवस्था चुनें",
    acres: "एकड़",
    bigha: "बीघा",
    results: "फसल सलाह",
    estimatedCost: "अनुमानित उपचार लागत",
    weather: "मौसम सलाह",
    spray: "स्प्रे सलाह",
    smart: "स्मार्ट सलाह",
    ai: "AI अनुमान",
    why: "यह परिणाम क्यों?",
    pests: "संभावित कीट और रोग",
    confidence: "AI विश्वसनीयता",
    confidenceLevel: "विश्वसनीयता स्तर",
    high: "उच्च",
    moderate: "मध्यम",
    low: "कम",
    noPrediction: "विश्वसनीय AI अनुमान उपलब्ध नहीं है",
    disclaimer:
      "यह AI द्वारा दिया गया संभावित अनुमान है, निश्चित रोग निदान नहीं। उपचार शुरू करने से पहले स्थानीय कृषि विशेषज्ञ से लक्षणों की पुष्टि करें।",
    weatherUnavailable: "मौसम की जानकारी अभी उपलब्ध नहीं है।",
    invalidLand: "कृपया भूमि का सही क्षेत्रफल दर्ज करें।",
    requiredLocation: "कृपया अपना स्थान दर्ज करें।",
    requiredCrop: "कृपया फसल चुनें।",
    requiredStage: "कृपया फसल की अवस्था चुनें।",
    requiredSymptoms: "कृपया फसल के लक्षण दर्ज करें।",
    backendError:
      "फसल की सलाह प्राप्त नहीं हो सकी। कृपया backend server जांचें।",
    language: "English",
  },
};

function App() {
  const [language, setLanguage] = useState("en");
  const t = translations[language];

  const [crops, setCrops] = useState([]);

  const [form, setForm] = useState({
    location: "",
    crop: "",
    landSize: "",
    unit: "acres",
    growthStage: "",
    symptoms: "",
  });

  const [advice, setAdvice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingCrops, setLoadingCrops] = useState(true);
  const [error, setError] = useState("");

  const selectedCrop = crops.find(
    (crop) => crop.name === form.crop
  );

  useEffect(() => {
    loadCrops();
  }, []);

  const loadCrops = async () => {
    try {
      setLoadingCrops(true);

      const response = await axios.get(
        `${API_URL}/crops/`,
        {
          timeout: 10000,
        }
      );

      setCrops(
        Array.isArray(response.data)
          ? response.data
          : []
      );

      setError("");
    } catch (err) {
      console.error("Crop loading error:", err);

      setError(
        "Unable to load crop information. Please check the backend server."
      );
    } finally {
      setLoadingCrops(false);
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setError("");

    if (name === "crop") {
      setForm((previous) => ({
        ...previous,
        crop: value,
        growthStage: "",
      }));

      return;
    }

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const validateForm = () => {
    if (!form.location.trim()) {
      return t.requiredLocation;
    }

    if (!form.crop) {
      return t.requiredCrop;
    }

    if (!form.landSize || Number(form.landSize) <= 0) {
      return t.invalidLand;
    }

    if (!form.growthStage) {
      return t.requiredStage;
    }

    if (!form.symptoms.trim()) {
      return t.requiredSymptoms;
    }

    return "";
  };

  const getAdvice = async (event) => {
    event.preventDefault();

    const validationError = validateForm();

    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    setError("");
    setAdvice(null);

    try {
      const response = await axios.post(
        `${API_URL}/advice`,
        {
          location: form.location.trim(),
          crop: form.crop,
          landSize: Number(form.landSize),
          unit: form.unit,
          growthStage: form.growthStage,
          symptoms: form.symptoms.trim(),
        },
        {
          timeout: 30000,
        }
      );

      if (response.data?.status === "error") {
        throw new Error(
          response.data.message ||
            "Advice generation failed"
        );
      }

      setAdvice(response.data);

      setTimeout(() => {
        document
          .getElementById("results")
          ?.scrollIntoView({
            behavior: "smooth",
          });
      }, 100);
    } catch (err) {
      console.error("Advice error:", err);

      if (err.response?.data?.detail) {
        if (
          Array.isArray(
            err.response.data.detail
          )
        ) {
          setError(
            err.response.data.detail
              .map((item) => item.msg)
              .join(", ")
          );
        } else {
          setError(
            String(
              err.response.data.detail
            )
          );
        }
      } else if (err.message) {
        setError(err.message);
      } else {
        setError(t.backendError);
      }
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceLevel = (
    confidenceValue
  ) => {
    const value = Number(
      confidenceValue || 0
    );

    if (value >= 70) {
      return {
        label: t.high,
        className:
          "bg-green-100 text-green-700",
      };
    }

    if (value >= 40) {
      return {
        label: t.moderate,
        className:
          "bg-yellow-100 text-yellow-700",
      };
    }

    return {
      label: t.low,
      className:
        "bg-red-100 text-red-700",
    };
  };

  const confidence =
    getConfidenceLevel(
      advice?.ml_confidence
    );

  const isWeatherRisk =
    advice?.smart_advisory?.includes(
      "⚠️"
    ) ||
    advice?.smart_advisory?.includes(
      "💨"
    ) ||
    advice?.smart_advisory?.includes(
      "🌧️"
    ) ||
    advice?.smart_advisory?.includes(
      "🌡️"
    );

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50">

      <header className="border-b bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-5">

          <div>
            <h1 className="text-2xl font-bold text-green-700 md:text-3xl">
              🌱 {t.title}
            </h1>

            <p className="mt-1 text-sm text-gray-600">
              {t.subtitle}
            </p>
          </div>

          <button
            type="button"
            onClick={() =>
              setLanguage(
                (previous) =>
                  previous === "en"
                    ? "hi"
                    : "en"
              )
            }
            className="rounded-lg border border-green-600 px-4 py-2 text-sm font-semibold text-green-700 transition hover:bg-green-600 hover:text-white"
          >
            {t.language}
          </button>

        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8">

        <section className="mb-8 rounded-2xl bg-white p-5 shadow-lg md:p-8">

          <div className="mb-6">

            <h2 className="text-xl font-bold text-gray-800">
              🌾 {t.getAdvice}
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Enter your crop information and symptoms to receive guidance.
            </p>

          </div>

          {error && (
            <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
              ⚠️ {error}
            </div>
          )}

          <form
            onSubmit={getAdvice}
            className="space-y-5"
          >

            <div className="grid gap-5 md:grid-cols-2">

              <div>
                <label className="mb-2 block text-sm font-semibold text-gray-700">
                  {t.location}
                </label>

                <input
                  name="location"
                  value={form.location}
                  onChange={handleChange}
                  placeholder="Example: Buxar, Bihar"
                  className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-gray-700">
                  {t.crop}
                </label>

                <select
                  name="crop"
                  value={form.crop}
                  onChange={handleChange}
                  disabled={loadingCrops}
                  className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
                >

                  <option value="">
                    {loadingCrops
                      ? "Loading crops..."
                      : t.cropSelect}
                  </option>

                  {crops.map((crop) => (
                    <option
                      key={
                        crop.id ||
                        crop.name
                      }
                      value={crop.name}
                    >
                      {crop.name}
                    </option>
                  ))}

                </select>
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-gray-700">
                  {t.landSize}
                </label>

                <input
                  type="number"
                  min="0"
                  step="0.1"
                  name="landSize"
                  value={form.landSize}
                  onChange={handleChange}
                  placeholder="Example: 5"
                  className="w-full rounded-lg border border-gray-300 px-4 py-3 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-gray-700">
                  {t.unit}
                </label>

                <select
                  name="unit"
                  value={form.unit}
                  onChange={handleChange}
                  className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
                >

                  <option value="acres">
                    {t.acres}
                  </option>

                  <option value="bigha">
                    {t.bigha}
                  </option>

                </select>
              </div>

              <div className="md:col-span-2">

                <label className="mb-2 block text-sm font-semibold text-gray-700">
                  {t.growthStage}
                </label>

                <select
                  name="growthStage"
                  value={form.growthStage}
                  onChange={handleChange}
                  disabled={!selectedCrop}
                  className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100 disabled:bg-gray-100"
                >

                  <option value="">
                    {selectedCrop
                      ? t.stageSelect
                      : "Select Crop First"}
                  </option>

                  {selectedCrop?.growth_stages?.map(
                    (stage, index) => (
                      <option
                        key={
                          stage.id ||
                          stage.order ||
                          index
                        }
                        value={stage.name}
                      >
                        {stage.name}
                      </option>
                    )
                  )}

                </select>

              </div>

              <div className="md:col-span-2">

                <label className="mb-2 block text-sm font-semibold text-gray-700">
                  {t.symptoms}
                </label>

                <textarea
                  name="symptoms"
                  value={form.symptoms}
                  onChange={handleChange}
                  rows="5"
                  maxLength="500"
                  placeholder={
                    t.symptomsPlaceholder
                  }
                  className="w-full resize-none rounded-lg border border-gray-300 px-4 py-3 outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100"
                />

              </div>

            </div>

            <button
              type="submit"
              disabled={
                loading ||
                loadingCrops
              }
              className="w-full rounded-lg bg-green-600 px-6 py-3 font-bold text-white shadow-md transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-gray-400"
            >
              {loading
                ? `⏳ ${t.analyzing}`
                : `🔍 ${t.getAdvice}`}
            </button>

          </form>
        </section>

        {advice && (
          <section
            id="results"
            className="space-y-6"
          >

            <div className="rounded-2xl bg-white p-5 shadow-lg md:p-8">

              <h2 className="text-2xl font-bold text-gray-800">
                🌱 {t.results}
              </h2>

              <div className="mt-6 grid gap-4 md:grid-cols-4">

                <InfoCard
                  title={t.crop}
                  value={
                    advice.crop ||
                    form.crop
                  }
                />

                <InfoCard
                  title={t.location}
                  value={
                    advice.location ||
                    form.location
                  }
                />

                <InfoCard
                  title={t.landSize}
                  value={`${form.landSize} ${form.unit}`}
                />

                <InfoCard
                  title={t.growthStage}
                  value={
                    advice.growth_stage ||
                    form.growthStage
                  }
                />

              </div>
            </div>

            <div className="grid gap-6 md:grid-cols-2">

              <div className="rounded-2xl bg-green-600 p-6 text-white shadow-lg">

                <h3 className="text-lg font-bold">
                  💰 {t.estimatedCost}
                </h3>

                <p className="mt-3 text-4xl font-bold">
                  {advice.estimated_cost !==
                    null &&
                  advice.estimated_cost !==
                    undefined
                    ? `₹${advice.estimated_cost}`
                    : "N/A"}
                </p>

                <p className="mt-2 text-sm opacity-90">
                  {advice.cost_note ||
                    "Estimated cost based on demo treatment prices. Verify current local prices before purchase."}
                </p>

              </div>

              <div className="rounded-2xl bg-white p-6 shadow-lg">

                <h3 className="text-lg font-bold text-gray-800">
                  🤖 {t.ai}
                </h3>

                <p className="mt-3 text-lg font-semibold text-gray-800">
                  {advice.ml_prediction ||
                    t.noPrediction}
                </p>

                <div className="mt-4 flex flex-wrap items-center gap-3">

                  <span className="rounded-full bg-gray-100 px-3 py-1 text-sm font-semibold text-gray-700">
                    {t.confidence}:{" "}
                    {advice.ml_confidence ??
                      0}
                    %
                  </span>

                  <span
                    className={`rounded-full px-3 py-1 text-sm font-semibold ${confidence.className}`}
                  >
                    {t.confidenceLevel}:{" "}
                    {confidence.label}
                  </span>

                </div>

                <p className="mt-4 text-sm text-gray-600">
                  ⚠️ {t.disclaimer}
                </p>

              </div>

            </div>

            <div className="rounded-2xl bg-white p-6 shadow-lg">

              <h3 className="text-lg font-bold text-gray-800">
                🌦️ {t.weather}
              </h3>

              {advice.weather?.available ? (
                <>
                  <div className="mt-5 grid gap-4 sm:grid-cols-2 md:grid-cols-5">

                    <WeatherCard
                      label="Rain"
                      value={`${advice.weather.rain_forecast_mm} mm`}
                      icon="🌧️"
                    />

                    <WeatherCard
                      label="Temperature"
                      value={`${advice.weather.temperature_c} °C`}
                      icon="🌡️"
                    />

                    <WeatherCard
                      label="Humidity"
                      value={`${advice.weather.humidity_percent}%`}
                      icon="💧"
                    />

                    <WeatherCard
                      label="Wind"
                      value={`${advice.weather.wind_speed_kmh} km/h`}
                      icon="💨"
                    />

                    <WeatherCard
                      label="Rain Probability"
                      value={`${advice.weather.rain_probability_percent}%`}
                      icon="☔"
                    />

                  </div>

                  {advice.spray_recommendation && (
                    <div className="mt-5 rounded-xl border border-blue-200 bg-blue-50 p-4">

                      <p className="font-semibold text-blue-800">
                        💦 {t.spray}
                      </p>

                      <p className="mt-1 text-sm text-blue-700">
                        {advice.spray_recommendation}
                      </p>

                    </div>
                  )}
                </>
              ) : (
                <div className="mt-4 rounded-xl border border-yellow-200 bg-yellow-50 p-4 text-sm text-yellow-700">
                  ⚠️ {t.weatherUnavailable}
                </div>
              )}

            </div>

            {advice.smart_advisory && (
              <div
                className={`rounded-2xl p-6 shadow-lg ${
                  isWeatherRisk
                    ? "border border-yellow-200 bg-yellow-50"
                    : "border border-green-200 bg-green-50"
                }`}
              >

                <h3 className="text-lg font-bold text-gray-800">
                  🧠 {t.smart}
                </h3>

                <p className="mt-3 text-gray-700">
                  {advice.smart_advisory}
                </p>

              </div>
            )}

            {advice.why_result && (
              <div className="rounded-2xl bg-white p-6 shadow-lg">

                <h3 className="text-lg font-bold text-gray-800">
                  💡 {t.why}
                </h3>

                <p className="mt-3 text-sm leading-6 text-gray-700">
                  {advice.why_result}
                </p>

              </div>
            )}

            {advice.pests?.length > 0 && (
              <div className="rounded-2xl bg-white p-6 shadow-lg">

                <h3 className="text-lg font-bold text-gray-800">
                  🐛 {t.pests}
                </h3>

                <div className="mt-4 grid gap-3 md:grid-cols-2">

                  {advice.pests.map(
                    (pest, index) => (
                      <div
                        key={
                          pest.id ||
                          index
                        }
                        className="rounded-lg border border-gray-200 bg-gray-50 p-4"
                      >

                        <p className="font-semibold text-gray-800">
                          {pest.name}
                        </p>

                        {pest.type && (
                          <p className="mt-1 text-xs font-medium text-green-700">
                            {pest.type}
                          </p>
                        )}

                        {pest.symptoms && (
                          <p className="mt-2 text-sm text-gray-600">
                            <strong>
                              Symptoms:
                            </strong>{" "}
                            {pest.symptoms}
                          </p>
                        )}

                      </div>
                    )
                  )}

                </div>
              </div>
            )}

          </section>
        )}

        <Chatbot
          cropName={form.crop}
          growthStage={form.growthStage}
          location={form.location}
          landSize={form.landSize}
          unit={form.unit}
        />

      </main>
    </div>
  );
}

function InfoCard({
  title,
  value,
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">

      <p className="text-sm font-medium text-gray-500">
        {title}
      </p>

      <p className="mt-1 font-semibold text-gray-800">
        {value}
      </p>

    </div>
  );
}

function WeatherCard({
  label,
  value,
  icon,
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">

      <div className="text-2xl">
        {icon}
      </div>

      <p className="mt-2 text-sm font-medium text-gray-500">
        {label}
      </p>

      <p className="mt-1 font-semibold text-gray-800">
        {value}
      </p>

    </div>
  );
}

export default App;