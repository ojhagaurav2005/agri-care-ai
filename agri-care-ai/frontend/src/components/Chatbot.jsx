import { useState } from "react";
import axios from "axios";

const API_URL = "https://agrii-care-ai.onrender.com";

export default function Chatbot({
  cropName = "",
  growthStage = "",
  location = "",
  landSize = "",
  unit = "acres",
}) {
  const [open, setOpen] = useState(false);
  const [language, setLanguage] = useState("en");
  const [input, setInput] = useState("");
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "🌱 Hello! I can help with crop symptoms, pests, diseases, weather and treatment-cost questions.",
    },
  ]);

  const startVoiceInput = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Voice input is not supported in this browser. Please use Google Chrome or Microsoft Edge."
      );
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = language === "hi" ? "hi-IN" : "en-IN";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      const spokenText = event.results[0][0].transcript;

      setInput((previous) =>
        previous ? `${previous} ${spokenText}` : spokenText
      );
    };

    recognition.onerror = (event) => {
      console.error("Voice recognition error:", event.error);
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  };

  const sendMessage = async () => {
    const message = input.trim();

    if (!message || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        text: message,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const context = [
        cropName && `Crop: ${cropName}`,
        growthStage && `Growth stage: ${growthStage}`,
        location && `Location: ${location}`,
        landSize && `Farm size: ${landSize} ${unit}`,
      ]
        .filter(Boolean)
        .join(" • ");

      const response = await axios.post(
        `${API_URL}/api/chat`,
        {
          message: `${message}\n\nFarm context: ${
            context || "No farm information selected."
          }`,
          language,
        },
        {
          timeout: 15000,
        }
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text:
            response.data?.reply ||
            "Sorry, I could not generate a response.",
        },
      ]);
    } catch (error) {
      console.error("Chatbot error:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text:
            "⚠️ I couldn't connect to the crop-care assistant. Please check that the backend is running and try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((previous) => !previous)}
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-full bg-green-600 px-5 py-4 font-semibold text-white shadow-xl transition hover:scale-105 hover:bg-green-700"
      >
        {open ? "✕ Close" : "💬 Crop Assistant"}
      </button>

      {open && (
        <div className="fixed bottom-24 right-4 z-50 flex h-[620px] w-[calc(100vw-2rem)] max-w-[390px] flex-col overflow-hidden rounded-3xl border border-green-100 bg-white shadow-2xl sm:right-6">
          <div className="bg-gradient-to-r from-green-700 to-emerald-600 p-4 text-white">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-xs font-medium uppercase tracking-wide text-green-100">
                  AI Crop Care
                </p>

                <h2 className="mt-1 text-lg font-bold">
                  🌾 Farm Assistant
                </h2>

                <p className="mt-1 text-xs text-green-50">
                  Farmer-friendly crop-care guidance
                </p>
              </div>

              <select
                value={language}
                onChange={(event) => setLanguage(event.target.value)}
                className="rounded-lg border-0 bg-white px-2 py-1.5 text-xs font-semibold text-gray-800 outline-none"
              >
                <option value="en">English</option>
                <option value="hi">हिन्दी</option>
              </select>
            </div>

            {(cropName || growthStage || location || landSize) && (
              <div className="mt-3 rounded-xl bg-white/15 p-2 text-xs text-green-50">
                <span className="font-semibold">Current farm:</span>{" "}
                {cropName && `Crop: ${cropName}`}
                {growthStage && ` • Stage: ${growthStage}`}
                {location && ` • Location: ${location}`}
                {landSize && ` • Farm: ${landSize} ${unit}`}
              </div>
            )}
          </div>

          <div className="flex-1 space-y-3 overflow-y-auto bg-gray-50 p-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[88%] rounded-2xl px-4 py-3 text-sm leading-5 ${
                    message.role === "user"
                      ? "rounded-br-md bg-green-600 text-white"
                      : "rounded-bl-md border border-gray-100 bg-white text-gray-800 shadow-sm"
                  }`}
                >
                  {message.text}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="rounded-2xl bg-white px-4 py-3 text-sm text-gray-500 shadow-sm">
                  🌱 Thinking...
                </div>
              </div>
            )}
          </div>

          <div className="border-t bg-white p-3">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                maxLength={300}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about your crop..."
                className="min-w-0 flex-1 rounded-xl border border-gray-300 px-3 py-2.5 text-sm outline-none focus:border-green-500 focus:ring-2 focus:ring-green-100"
              />

              <button
                type="button"
                onClick={startVoiceInput}
                disabled={listening || loading}
                title="Voice input"
                className={`rounded-xl px-3 py-2.5 text-lg ${
                  listening
                    ? "animate-pulse bg-red-500 text-white"
                    : "bg-green-100 text-green-700 hover:bg-green-200"
                }`}
              >
                {listening ? "🔴" : "🎤"}
              </button>

              <button
                type="button"
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="rounded-xl bg-green-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-green-700 disabled:bg-gray-300"
              >
                {loading ? "..." : "Send"}
              </button>
            </div>

            <p className="mt-2 text-center text-[10px] text-gray-400">
              🎤 Voice input works best in Chrome or Edge.
            </p>

            <p className="text-center text-[10px] text-gray-400">
              For exact pesticide doses, follow the official label and local
              agricultural guidance.
            </p>
          </div>
        </div>
      )}
    </>
  );
}