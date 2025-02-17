import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';

const TimeComparison = () => {
  const [data, setData] = useState([]);
  
  const parseTime = (time) => new Date(time).getTime();

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/frontendata');  // Adjust endpoint if necessary
        console.log(response.data);
        setData(response.data.arr);  // Update state with fetched data
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);  // Empty dependency array ensures this runs once when the component mounts

  // Fixed timeline from 12 AM to 11 PM
  const getDayStart = (time) => {
    const date = new Date(time);
    date.setHours(0, 0, 0, 0);
    return date;
  };

  // Get the reference date from first data point
  const referenceDate = data.length > 0 ? getDayStart(parseTime(data[0].start_time)) : new Date();
  const minTime = referenceDate.getTime();
  const maxTime = new Date(referenceDate).setHours(23, 0, 0, 0);

  // Generate hours grid from 12 AM to 11 PM
  const hours = [];
  for (let h = 0; h < 24; h++) {
    const hour = new Date(referenceDate);
    hour.setHours(h);
    hours.push(hour);
  }

  // Calculate positions
  const totalDuration = maxTime - minTime;
  const timeToPosition = (time) => {
    const adjustedTime = Math.max(minTime, Math.min(time, maxTime));
    return ((adjustedTime - minTime) / totalDuration) * 100;
  };

  return (
    <div className="flex bg-[#0D1821] text-white p-5 rounded-lg shadow-xl mb-12">
      {/* Y-axis - Time Labels */}
      <div className="w-20 mr-4 relative">
        {hours.map((hour, i) => (
          <div 
            key={i}
            className="absolute text-xs text-gray-400 font-mono -translate-y-1/2"
            style={{ top: `${timeToPosition(hour.getTime())}%` }}
          >
            {hour.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        ))}
      </div>

      {/* Timeline Area */}
      <div className="flex-1 relative min-h-[800px]" style={{ height: `calc(100% + 80px)` }}>
        {/* Grid Lines */}
        {hours.map((hour, i) => (
          <div
            key={i}
            className="absolute h-px bg-gray-700 w-full"
            style={{ top: `${timeToPosition(hour.getTime())}%` }}
          />
        ))}

        {/* Task Bars */}
        {data.map((item, i) => {
          const start = Math.max(minTime, parseTime(item.start_time));
          const end = Math.min(maxTime, parseTime(item.end_time));
          const percentage = Math.min(item.ratio * 100, 100);

          return (
            <div 
              key={i}
              className="absolute w-full"
              style={{
                top: `${timeToPosition(start)}%`,
                height: `calc(${timeToPosition(end) - timeToPosition(start)}% - 16px)`,
                marginBottom: '16px'
              }}
            >
              <div className="h-full rounded-lg relative group" style={{ backgroundColor: '#746F72' }}>
                {/* Progress Bar */}
                <div
                  className="h-full rounded-l-lg transition-all duration-300 ease-out relative"
                  style={{ 
                    width: `${percentage}%`,
                    backgroundColor: '#5CC8FF'
                  }}
                >
                  <span className="absolute left-2 top-1/2 -translate-y-1/2 text-sm text-white font-medium truncate">
                    {item.title}
                  </span>
                  <span className="absolute right-2 top-1/2 -translate-y-1/2 text-sm text-white font-medium">
                    {Math.round(percentage)}%
                  </span>
                </div>

                {/* End Marker */}
                <div className="absolute right-0 inset-y-0 w-1 bg-gray-600/50 rounded-r" />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TimeComparison;