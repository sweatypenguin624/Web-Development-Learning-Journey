import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

console.log("✅ main.jsx is executing!");
const rootElement = document.getElementById("root");
console.log("Root Element:", rootElement);
if (!rootElement) {
  console.error("Root element not found!");
} else {
  ReactDOM.render(<App />, rootElement);
}