import React, { useState } from "react";
import { AIInput } from "@/components/ui/ai-input";

const App: React.FC = () => {
  const [shortUrl, setShortUrl] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5002";

  const handleSubmit = async (value: string) => {
    if (!value.trim()) {
      setError("Please enter a valid URL.");
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/shorten`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: value }),
      });

      const data = await response.json();
      if (!response.ok) {
        setError(data.error || "Failed to shorten URL.");
        return;
      }

      setShortUrl(data.shortUrl);
    } catch (error) {
      setError(`Network error: ${error instanceof Error ? error.message : "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(shortUrl);
    alert("Short URL copied to clipboard!");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-300 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
          Shorten Your URL
        </h1>
        <AIInput
          placeholder="Paste your URL here"
          onSubmit={handleSubmit}
          className={loading ? "opacity-50" : ""}
        />
        {shortUrl && (
          <div className="mt-6 flex flex-col items-center gap-3">
            <a
              href={shortUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-600 hover:text-indigo-800 text-lg break-all"
            >
              {shortUrl}
            </a>
            <button
              onClick={handleCopy}
              className="px-4 py-2 text-indigo-600 border border-indigo-600 rounded-lg hover:bg-indigo-600 hover:text-white transition-all"
            >
              Copy
            </button>
          </div>
        )}
        {error && (
          <p className="mt-4 text-red-500 text-sm text-center">{error}</p>
        )}
      </div>
    </div>
  );
};

export default App;