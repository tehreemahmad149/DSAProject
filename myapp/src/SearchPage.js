// SearchPage.js
import React, { useState } from 'react';
import axios from 'axios';
import AddContentModal from './AddContentModal';
import './SearchPage.css';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/search/', { query });
      setResults(response.data.results);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  const handleAddContent = () => {
    setIsModalOpen(true);
  };

  const handleAddContentModal = async (content) => {
    try {
      const response = await axios.post('http://localhost:8000/api/add-content/', { content });
      console.log(response.data);  // Handle the response as needed
      setIsModalOpen(false);
    } catch (error) {
      console.error('Error adding content:', error);
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
      <button onClick={handleAddContent} className="add-content-button">
        Add Content
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
      {/* Conditionally render the modal based on isModalOpen */}
      {isModalOpen && (
        <AddContentModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onAddContent={handleAddContentModal}  // Pass the function to handle adding content
        />
      )}
    </div>
  );
};

export default SearchPage;
