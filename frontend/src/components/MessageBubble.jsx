import React from 'react';
import { Bot } from 'lucide-react';

const MessageBubble = ({ msg }) => {
  return (
    <div className={`message ${msg.sender}`}>
      {msg.sender === 'bot' && <Bot size={18} style={{ marginBottom: '-4px', marginRight: '5px' }} />}
      {msg.text}
      
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