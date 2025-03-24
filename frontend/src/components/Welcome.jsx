import React from 'react';
import './Welcome.css'; 

function Welcome({ onStart }) {
  return (
    <div className="welcome-container">
		<h2 className="welcome-title">Welcome to Recipe Assistant</h2>
		<div className="welcome-content">
			<p>Your AI-powered cooking companion</p>
			<p>Get recipes, cooking tips, and ingredient substitutions instantly</p>
			<button className="start-button" onClick={onStart}>
			Start Cooking
			</button>
		</div>
    </div>
  );
}

export default Welcome;