import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import React from 'react';
import ReactDOM from 'react-dom';
import Summary from './component/summary'

const sampleData = {
  "Social Media": 120,
  "Work": 300,
  "Entertainment": 150,
};

ReactDOM.createRoot(document.getElementById('popup-root')).render(
  <Summary data={sampleData} />
);


// createRoot(document.getElementById('root')).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )
