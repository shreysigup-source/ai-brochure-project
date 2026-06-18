import { useState } from "react";
import UrlInputScreen from "./components/UrlInputScreen";
import LoadingScreen from "./components/LoadingScreen";
import ResultScreen from "./components/ResultScreen";
import { generateBrochure } from "./api";

function App() {
  // "input" -> "loading" -> "result"   (errors send us back to "input")
  const [screen, setScreen] = useState("input");
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleGenerate(url) {
    setScreen("loading");
    setErrorMessage("");

    try {
      const data = await generateBrochure(url);
      setResult(data);
      setScreen("result");
    } catch (error) {
      let message = "Something went wrong. Please try again.";
      if (error.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error.code === "ERR_NETWORK") {
        message = "Could not reach the server. Make sure the backend (uvicorn) is running on port 8000.";
      }
      setErrorMessage(message);
      setScreen("input");
    }
  }

  function handleStartOver() {
    setResult(null);
    setErrorMessage("");
    setScreen("input");
  }

  return (
    <div className="min-h-screen bg-paper text-ink flex items-center justify-center p-6">
      {screen === "input" && (
        <UrlInputScreen onGenerate={handleGenerate} errorMessage={errorMessage} />
      )}
      {screen === "loading" && <LoadingScreen />}
      {screen === "result" && result && (
        <ResultScreen result={result} onStartOver={handleStartOver} />
      )}
    </div>
  );
}

export default App;