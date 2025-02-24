import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    try {
      // Add user message
      setMessages(prev => [...prev, { role: 'user', content: input }]);
      
      // Get AI response
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: input
      });

      // Add AI response
      setMessages(prev => [
        ...prev, 
        { 
          role: 'bot', 
          content: response.data.answer,
          sources: response.data.sources
        }
      ]);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
    setInput('');
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="content">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
              {msg.sources && (
                <div className="sources">
                  <h4>Reference Recipes:</h4>
                  {msg.sources.map((source, idx) => (
                    <div key={idx} className="source">
                      <p>{source.substring(0, 150)}...</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && <div className="loading">Thinking...</div>}
      </div>
      
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your recipe question..."
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default Chat;