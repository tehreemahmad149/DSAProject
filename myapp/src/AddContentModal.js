// AddContentModal.js
import React, { useState } from 'react';
import './AddContentModal.css';

const AddContentModal = ({ isOpen, onClose, onAddContent }) => {
  const [content, setContent] = useState('');

  const handleAddContent = () => {
    onAddContent(content);
    setContent(''); // Clear content after adding
  };

  return (
    <div className={`modal ${isOpen ? 'open' : 'closed'}`}>
      <div className="modal-content">
        <span className="close" onClick={onClose}>
          &times;
        </span>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Enter your content here"
          className="modal-textarea"
        />
        <button onClick={handleAddContent} className="add-content-button">
          Add Content
        </button>
      </div>
    </div>
  );
};

export default AddContentModal;
