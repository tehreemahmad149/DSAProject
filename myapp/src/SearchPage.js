// myapp/src/SearchPage.js
import React, { useState } from 'react';
import axios from 'axios';

const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/search/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Set content type to JSON
                },
                body: JSON.stringify({ query }), // Send the query as JSON
            });

            const data = await response.json();
            setResults(data.results);
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    };

    return (
        <div>
            <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
            <button onClick={handleSearch}>Search</button>

            <ul>
                {results.map((result) => (
                    <li key={result.doc_id}>Document ID: {result.doc_id}, Score: {result.score}</li>
                ))}
            </ul>
        </div>
    );
};

export default SearchPage;
