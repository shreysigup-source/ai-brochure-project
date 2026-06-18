import { useEffect, useState } from "react";

// These map roughly to what main.py is actually doing behind the scenes:
// crawler.py -> extractor.py -> generator.py
const STEPS = [
  "Visiting the website…",
  "Reading the pages…",
  "Sorting facts with AI…",
  "Writing the brochure…",
];

function LoadingScreen() {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStepIndex((prev) => (prev + 1) % STEPS.length);
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-md text-center">
      <div className="stamp-mark mx-auto mb-6" aria-hidden="true">
        <span>SENT</span>
      </div>
      <p className="font-mono text-sm text-ink-soft uppercase tracking-wide" role="status">
        {STEPS[stepIndex]}
      </p>
    </div>
  );
}

export default LoadingScreen;