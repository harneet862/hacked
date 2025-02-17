import React from 'react';

function Summary({ data }) {
  return (
    <div>
      <h1>RoutineRadar</h1>
      {data ? (
        <div>
          <h2>Website Summary</h2>
          <ul>
            {Object.entries(data).map(([category, time]) => (
              <li key={category}>
                {category}: {time} minutes
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No data available.</p>
      )}
    </div>
  );
}

export default Summary;
