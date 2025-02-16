import React, { useState } from 'react';

function Prod({ websites }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="w-full bg-gray-900 text-gray-300 shadow-lg p-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full text-left bg-gray-800 px-4 py-2 text-white font-bold rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-600"
      >
        {isOpen ? 'Hide Productivity' : 'Show Productivity'}
      </button>
      {isOpen && (
        <div className="mt-4">
          <h1 className="text-2xl font-bold mb-4 text-center text-white">Productivity</h1>
          <div className="overflow-auto h-60">
            <table className="w-full table-auto text-left">
              <thead>
                <tr>
                  <th className="px-4 py-2 border-b border-gray-700">Website</th>
                  <th className="px-4 py-2 border-b border-gray-700">Time Spent</th>
                </tr>
              </thead>
              <tbody>
                {websites.map((site, index) => (
                  <tr key={index} className="odd:bg-gray-800 even:bg-gray-700">
                    <td className="px-4 py-2">{site.name}</td>
                    <td className="px-4 py-2">{site.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default Prod;
