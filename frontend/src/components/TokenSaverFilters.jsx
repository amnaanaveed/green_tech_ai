import React from 'react';
import { Sprout, Settings2 } from 'lucide-react';

const TokenSaverFilters = ({ cropFilter, setCropFilter, answerLength, setAnswerLength }) => {
  return (
    <div className="sidebar">
      <h2><Sprout size={28} /> GreenTech AI</h2>
      <p style={{ fontSize: '0.85rem', color: '#86efac', marginBottom: '20px' }}>
        Cross-lingual Agricultural Expert
      </p>

      <div className="filter-group">
        <label><Settings2 size={16} style={{display: 'inline', marginBottom: '-3px'}}/> Context Filter (Crop)</label>
        <select value={cropFilter} onChange={(e) => setCropFilter(e.target.value)}>
          <option value="All">All Context (General Search)</option>
          <option value="Wheat">Wheat</option>
          <option value="Rice">Rice</option>
          <option value="Cotton">Cotton</option>
        </select>
        <small style={{fontSize: '0.7rem', color: '#4ade80'}}>Saves tokens by limiting PDF search.</small>
      </div>

      <div className="filter-group" style={{marginTop: '15px'}}>
        <label><Settings2 size={16} style={{display: 'inline', marginBottom: '-3px'}}/> Answer Length Filter</label>
        <select value={answerLength} onChange={(e) => setAnswerLength(e.target.value)}>
          <option value="Detailed">Detailed Explanation</option>
          <option value="Short">Short Answer</option>
        </select>
        <small style={{fontSize: '0.7rem', color: '#4ade80'}}>Forces AI to output fewer tokens.</small>
      </div>
    </div>
  );
};

export default TokenSaverFilters;