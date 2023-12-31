

// src/App.js

import React, { useState } from 'react';

import './App.css';



function App() {

  const [startTime, setStartTime] = useState('');

  const [endTime, setEndTime] = useState('');

  const [logs, setLogs] = useState([]);



  const fetchLogs = async () => {

    try {

      const response = await fetch(`http://10.0.2.15:8000/access-logs/?start_time=${startTime}&end_time=${endTime}`);

      const data = await response.json();

      setLogs(data.access_logs);

    } catch (error) {

      console.error('Error fetching logs:', error);

    }

  };



  return (

    <div className="App">

      <h1>Access Logs Query</h1>

      <div>

        <label>Start Time:</label>

        <input type="datetime-local" value={startTime} onChange={(e) => setStartTime(e.target.value)} />

      </div>

      <div>

        <label>End Time:</label>

        <input type="datetime-local" value={endTime} onChange={(e) => setEndTime(e.target.value)} />

      </div>

      <button onClick={fetchLogs}>Fetch Logs</button>

      <div>

        <h2>Access Logs:</h2>

        <ul>

          {logs.map((log, index) => (

            <li key={index}>{JSON.stringify(log)}</li>

          ))}

        </ul>

      </div>

    </div>

  );

}



export default App;
