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
      const response = await axios.post('http://localhost:8000/api/add-content/', {
        content: JSON.stringify(content),
      });

      if (response.data.success) {
        await axios.post('http://localhost:8000/api/update-forward/');
        await axios.post('http://localhost:8000/api/update-inverted/');
      }

      setIsModalOpen(false);
    } catch (error) {
      console.error('Error adding content:', error);
    }
  };

  return (
    <div className="search-page-container">
      <div className="search-bar">
        <img className="google-logo" src="https://freelogopng.com/images/all_img/1657952217google-logo-png.png" alt="Google Logo" />
        <div className="search-input-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="search-input"
            placeholder="Search Google"
          />
          <button onClick={handleSearch} className="search-button">
            Search
          </button>
        </div>
        <button onClick={handleAddContent} className="add-content-button">
          Add Content
        </button>
      </div>

      <ul className="results-container">
  {results.map((result) => {
    const titleParts = result.title.split('--');
    const source = titleParts[0];
    const date = titleParts[1];
    const displayTitle = titleParts.slice(2).join('--');

    return (
      <li key={result.title} className="result-item">
        <a href={result.url} target="_blank" className="result-link">
          <h3>{displayTitle}</h3>
        </a>
        <p>Date: {date}</p>
        <p>Source: {source}</p>
      </li>
    );
  })}
</ul>

      {isModalOpen && (
        <AddContentModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onAddContent={handleAddContentModal}
        />
      )}
    </div>
  );
};

export default SearchPage;