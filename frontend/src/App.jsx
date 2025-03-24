import React, { useState } from 'react';
import Chat from './components/Chat';
import Welcome from './components/Welcome';
import './App.css';

function App() {
  const [showChat, setShowChat] = useState(false); // 不存 localStorage

  return (
    <div className="app">
       {showChat && <h1>🍽 Recipe Assistant</h1>}
      
      {showChat ? (
        <Chat />
      ) : (
        <Welcome onStart={() => setShowChat(true)} />
      )}
    </div>
  );
}

export default App;
