import { useState } from "react";

function UrlInputScreen({ onGenerate, errorMessage }) {
  const [url, setUrl] = useState("");
  const [touched, setTouched] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setTouched(true);
    if (!url.trim()) return;
    onGenerate(url.trim());
  }

  return (
    <div className="w-full max-w-md">
      <div className="relative bg-white border border-paper-line rounded-sm shadow-sm">
        <div className="postal-perforation" />
        <div className="p-8 pt-10">
          <span className="inline-block text-xs font-mono tracking-[0.2em] uppercase text-postal mb-3">
            Brochure Post
          </span>
          <h1 className="font-display text-3xl text-ink mb-2 leading-tight">
            Address a website,
            <br />
            receive a brochure.
          </h1>
          <p className="text-ink-soft text-sm mb-8">
            Drop in a company's homepage. We'll read it, sort what matters, and post back a brochure.
          </p>

          <form onSubmit={handleSubmit} className="space-y-3">
            <label
              htmlFor="company-url"
              className="block text-xs font-mono uppercase tracking-wide text-ink-soft"
            >
              Destination URL
            </label>
            <input
              id="company-url"
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://company.com"
              className="w-full border-b-2 border-paper-line focus:border-postal outline-none focus-visible:ring-2 focus-visible:ring-postal/30 font-mono text-ink py-2 bg-transparent transition-colors"
            />
            {touched && !url.trim() && (
              <p className="text-postal text-xs">Enter a URL before sending.</p>
            )}
            {errorMessage && <p className="text-postal text-xs">{errorMessage}</p>}

            <button
              type="submit"
              className="w-full mt-4 bg-ink text-paper font-medium py-3 rounded-sm hover:bg-postal transition-colors focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-postal"
            >
              Generate Brochure
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default UrlInputScreen;