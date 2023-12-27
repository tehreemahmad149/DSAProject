// AddContentModal.js
import React, { useState } from 'react';
import './AddContentModal.css';

const AddContentModal = ({ isOpen, onClose, onAddContent }) => {
  const [content, setContent] = useState('');

  const handleAddContent = () => {
    // Call the parent function to handle adding content
    onAddContent(content);
  };

  return (
    <div className={`modal ${isOpen ? 'open' : 'closed'}`}>
      <div className="modal-content">
        <span className="close" onClick={onClose}>&times;</span>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Enter your content here"
        />
        <button onClick={handleAddContent}>Add Content</button>
      </div>
    </div>
  );
};

export default AddContentModal;