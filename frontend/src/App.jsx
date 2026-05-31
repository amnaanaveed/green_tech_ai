import React, { useState } from 'react';
import { Send, Sprout, Bot, Settings2 } from 'lucide-react';
import { sendMessageToAI } from './services/api';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Assalam o Alaikum! Main GreenTech AI hoon. Aap apni fasal ka masla Urdu ya Roman Urdu mein pooch sakte hain.', aiUsed: null }
  ]);
  const [inputData, setInputData] = useState('');
  const [loading, setLoading] = useState(false);

  // 🔥 Token Saving Filters State
  const [cropFilter, setCropFilter] = useState('All');
  const [answerLength, setAnswerLength] = useState('Detailed');

  const handleSend = async () => {
    if (!inputData.trim()) return;

    // 1. User ka message UI mein add karein
    const newMessages = [...messages, { sender: 'user', text: inputData, aiUsed: null }];
    setMessages(newMessages);
    setInputData('');
    setLoading(true);

    // 2. Backend (FastAPI) ko data bhejein with Token Filters!
    const response = await sendMessageToAI(inputData, cropFilter, answerLength);

    // 3. AI ka jawab UI mein add karein
    setMessages([...newMessages, { sender: 'bot', text: response.answer, aiUsed: response.ai_used }]);
    setLoading(false);
  };

  return (
    <div className="app-container">
      
      {/* LEFT SIDEBAR: TOKEN SAVER FILTERS */}
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

      {/* RIGHT AREA: CHAT INTERFACE */}
      <div className="chat-area">
        <div className="chat-history">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              {msg.sender === 'bot' && <Bot size={18} style={{ marginBottom: '-4px', marginRight: '5px' }} />}
              {msg.text}
              
              {/* Show which AI model answered */}
              {msg.aiUsed && (
                <div style={{display: 'block'}}>
                  <span className="ai-badge">Powered by {msg.aiUsed}</span>
                </div>
              )}
            </div>
          ))}
          {loading && <div className="loader">GreenTech AI is typing...</div>}
        </div>

        <div className="input-area">
          <input 
            type="text" 
            placeholder="Apna sawal likhein (e.g. Kapas ki bimari ka ilaaj?)"
            value={inputData}
            onChange={(e) => setInputData(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={loading}
          />
          <button onClick={handleSend} disabled={loading}>
            <Send size={20} />
          </button>
        </div>
      </div>

    </div>
  );
}

export default App;