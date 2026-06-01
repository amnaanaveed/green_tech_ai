import React from 'react';
import { Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown'; // 👈 Yeh nayi library import ki

const MessageBubble = ({ msg }) => {
  return (
    <div className={`message ${msg.sender}`}>
      {msg.sender === 'bot' && <Bot size={18} style={{ marginBottom: '-4px', marginRight: '5px' }} />}
      
      {/* 👈 Yahan raw text ki jagah ReactMarkdown use kiya hai */}
      <div className="markdown-content">
        <ReactMarkdown>{msg.text}</ReactMarkdown> 
      </div>
      
      {/* Show which AI model answered */}
      {msg.aiUsed && (
        <div style={{display: 'block'}}>
          <span className="ai-badge">Powered by {msg.aiUsed}</span>
        </div>
      )}
    </div>
  );
};

export default MessageBubble;