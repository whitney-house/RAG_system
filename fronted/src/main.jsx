import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';  // Ensure the path is correct
import './index.css';  // Ensure the global styles are imported

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);