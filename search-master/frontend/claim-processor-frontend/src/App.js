import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState('');
  const [sources, setSources] = useState([]);
  const [activeTab, setActiveTab] = useState('results');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setResult(''); // Clear previous result
    setSources([]); // Clear previous sources
    try {
      // POST request to the backend
      const response = await axios.post('http://localhost:8000/process', { text }, {
        headers: { 'Content-Type': 'application/json' },
      });
      setResult(response.data.result);
      setSources(response.data.sources);
    } catch (error) {
      console.error('Error:', error);
      setResult('Error processing request');
      setSources([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-6xl mx-auto grid grid-cols-2 gap-6">
        {/* Left Column */}
        <div>
          <h1 className="text-3xl font-bold text-orange-600 text-center mb-6">
            Process Claims and Media Files
          </h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <textarea
              className="w-full p-2 border border-orange-200 rounded focus:border-orange-400"
              rows="10"
              placeholder="Enter your claims code here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full px-4 py-2 bg-orange-500 text-white rounded ${
                isLoading ? 'opacity-50' : 'hover:bg-orange-600'
              }`}
            >
              {isLoading ? 'Processing...' : 'Process'}
            </button>
          </form>
        </div>

        {/* Right Column */}
        <div>
          <div className="flex border-b border-gray-300 mb-4">
            <button
              className={`px-4 py-2 ${
                activeTab === 'results' ? 'bg-white border-t border-l border-r' : 'bg-gray-200'
              } rounded-t`}
              onClick={() => setActiveTab('results')}
            >
              Results
            </button>
            <button
              className={`px-4 py-2 ${
                activeTab === 'sources' ? 'bg-white border-t border-l border-r' : 'bg-gray-200'
              } rounded-t`}
              onClick={() => setActiveTab('sources')}
            >
              Sources
            </button>
          </div>

          {activeTab === 'results' && (
            <div className="bg-orange-50 p-4 rounded-lg">
              <h1 className="text-xl font-bold text-orange-600 text-center mb-4">Results</h1>
              <ReactMarkdown>{result}</ReactMarkdown>
            </div>
          )}

          {activeTab === 'sources' && (
            <div>
              <h2 className="text-xl font-bold text-orange-600">Sources</h2>
              <p>The sources used to arrive at the conclusions:</p>
              <div className="mt-4 space-y-4">
                {sources.map((source, index) => (
                  <a
                    key={index}
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block bg-orange-500 text-white p-4 rounded hover:bg-orange-600 transition"
                  >
                    <div className="font-bold">{source.title}</div>
                    <div className="break-all">{source.url}</div>
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;