import React, { useState, useEffect } from 'react';
import { Send, Mic, MicOff } from 'lucide-react';
import MessageBubble from './MessageBubble';

const ChatInterface = ({ messages, loading, inputData, setInputData, handleSend }) => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState(null);

  // 🔥 Voice Recognition Setup
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recog = new SpeechRecognition();
      
      recog.continuous = false; 
      recog.interimResults = true; // Bolte waqt sath sath text likha aayega
      recog.lang = 'ur-PK'; // Urdu/Pakistan set kiya hai taake desi words samajh sake!

      recog.onresult = (event) => {
        let currentTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          currentTranscript += event.results[i][0].transcript;
        }
        setInputData(currentTranscript);
      };

      recog.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        setIsListening(false);
      };

      recog.onend = () => {
        setIsListening(false);
      };

      setRecognition(recog);
    } else {
      console.warn("Speech Recognition API aapke browser mein support nahi karti.");
    }
  }, [setInputData]);

  const toggleListening = () => {
    if (isListening) {
      recognition?.stop();
      setIsListening(false);
    } else {
      recognition?.start();
      setIsListening(true);
    }
  };

  return (
    <div className="chat-area">
      <div className="chat-history">
        {messages.map((msg, index) => (
          <MessageBubble key={index} msg={msg} />
        ))}
        {loading && <div className="loader">GreenTech AI is thinking...</div>}
      </div>

      <div className="input-area">
        {/* 🔥 NEW: Microphone Button */}
        <button 
          className={`mic-button ${isListening ? 'listening' : ''}`} 
          onClick={toggleListening}
          disabled={loading}
          title="Voice Typing"
        >
          {isListening ? <MicOff size={22} /> : <Mic size={22} />}
        </button>

        <input 
          type="text" 
          placeholder={isListening ? "Sun raha hoon... Boliye!" : "Apna sawal likhein ya mic par bolen..."}
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          disabled={loading}
        />
        <button className="send-btn" onClick={handleSend} disabled={loading || !inputData.trim()}>
          <Send size={20} />
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;