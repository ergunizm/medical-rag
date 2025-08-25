import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:8000/api/query';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);
    setError('');

    try {
      const response = await axios.post(API_URL, {
        question: query
      });
      
      setResult(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Medical RAG Query Interface</h1>
      <form onSubmit={handleSubmit} className="query-form">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a medical question..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Ask'}
        </button>
      </form>

      {loading && <div className="loading">Fetching answer, please wait...</div>}
      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result-container">
          <div className="answer">
            <h2>Answer</h2>
            <p>{result.answer}</p>
          </div>

          <div className="sources-container">
            <h2>Sources</h2>
            {result.sources.map((source, index) => (
              <div key={index} className="source-card">
                <p>{source.text}</p>
                <p className="source-filename">Source: {source.source}</p>
              </div>
            ))}
          </div>

          <div className="performance">
            <p>
              Retrieval: {result.latency_ms.retrieval} ms | 
              Generation: {result.latency_ms.generation} ms | 
              Total: {result.latency_ms.total} ms
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;