import React from 'react';
import Chat from './components/Chat';  // Ensure the path is correct
import './app.css';  // Ensure the component styles are imported

function App() {
  return (
    <div className="app">
      <h1>Recipe Assistant</h1>
      <Chat />
    </div>
  );
}

export default App;