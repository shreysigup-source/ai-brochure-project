import { useMemo } from "react";

// Turns the "## Heading" markdown that generator.py writes into
// [{ title, body }, ...] sections we can render as separate cards.
function parseBrochure(markdown) {
  if (!markdown) return [];

  const lines = markdown.split("\n");
  const sections = [];
  let current = null;

  for (const line of lines) {
    const headingMatch = line.match(/^##\s+(.*)/);
    if (headingMatch) {
      if (current) sections.push(current);
      current = { title: headingMatch[1].trim(), body: [] };
    } else if (current) {
      current.body.push(line);
    }
  }
  if (current) sections.push(current);

  return sections.map((section) => ({
    title: section.title,
    body: section.body.join("\n").trim(),
  }));
}

// Renders a section's body as a bullet list if every line looks like "- ...",
// otherwise as a normal paragraph.
function SectionBody({ text }) {
  const lines = text.split("\n").filter((line) => line.trim() !== "");
  const isList = lines.length > 0 && lines.every((line) => line.trim().startsWith("-"));

  if (isList) {
    return (
      <ul className="list-disc list-inside space-y-1 text-ink-soft text-sm leading-relaxed">
        {lines.map((line, i) => (
          <li key={i}>{line.replace(/^-+\s*/, "")}</li>
        ))}
      </ul>
    );
  }

  return <p className="text-ink-soft text-sm leading-relaxed whitespace-pre-line">{text}</p>;
}

function ResultScreen({ result, onStartOver }) {
  const sections = useMemo(() => parseBrochure(result?.brochure), [result]);
  const companyName = result?.structured_data?.company_name?.trim();

  function handleDownload() {
    // Opens the browser's print dialog scoped to just the brochure card
    // (see the @media print rules in index.css). The person can choose
    // "Save as PDF" there -- no extra PDF library needed.
    window.print();
  }

  return (
    <div className="w-full max-w-2xl">
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <span className="inline-block text-xs font-mono tracking-[0.2em] uppercase text-postal mb-1">
            Delivered
          </span>
          <h1 className="font-display text-2xl text-ink">{companyName || "Your Brochure"}</h1>
          <p className="text-ink-soft text-xs font-mono">{result?.url}</p>
        </div>
        <div className="flex gap-2 no-print shrink-0">
          <button
            onClick={handleDownload}
            className="text-sm border border-ink-soft text-ink px-4 py-2 rounded-sm hover:bg-ink hover:text-paper transition-colors focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-postal"
          >
            Download
          </button>
          <button
            onClick={onStartOver}
            className="text-sm text-postal px-4 py-2 rounded-sm hover:bg-postal-soft transition-colors focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-postal"
          >
            New Brochure
          </button>
        </div>
      </div>

      <div
        id="brochure-print-area"
        className="bg-white border border-paper-line rounded-sm divide-y divide-paper-line"
      >
        {sections.length === 0 && (
          <p className="p-8 text-ink-soft text-sm">No brochure content was returned.</p>
        )}
        {sections.map((section, i) => (
          <div key={i} className="p-6">
            <h2 className="font-display text-lg text-ink mb-2">{section.title}</h2>
            <SectionBody text={section.body} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResultScreen;