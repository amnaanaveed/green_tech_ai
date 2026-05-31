import axios from 'axios';

// Hamara FastAPI server is address par chal raha hai
const API_URL = 'http://127.0.0.1:8000';

export const sendMessageToAI = async (query, cropFilter, answerLength) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, {
      query: query,
      crop_filter: cropFilter,
      answer_length: answerLength
    });
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    return { 
        answer: "Sorry, connection mein koi masla aaya hai. Ensure backend server is running.", 
        ai_used: "None" 
    };
  }
};