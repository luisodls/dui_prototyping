import React from 'react';
import ReactDOM from 'react-dom/client';

const rootElement = document.getElementById('root');

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);

  root.render(
    <React.StrictMode>
      <h1>Hello there!</h1>
    </React.StrictMode>
  );
} else {
  console.error("Failed to find the root element.");
}
