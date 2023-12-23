// myapp/src/SearchPage.js
import React, { useState } from 'react';
import axios from 'axios';
import './SearchPage.css'; // Import your CSS file for styling

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <div className="google-search-container">
      <div className="google-logo"></div>
      <div className="search-box">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
          placeholder="Enter your query"
        />
      </div>
      <button onClick={handleSearch} className="search-button">
        Search
      </button>

      <ul className="results-container">
        {results.map((result) => (
          <li key={result.title} className="result-item">
            <a href={result.url} className="result-link">
              <h3>{result.title}</h3>
            </a>
            <p>Score: {result.score}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchPage;
