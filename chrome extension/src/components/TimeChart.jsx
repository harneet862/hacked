import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const TimeChart = ({ websites }) => {
  const processData = () => {
    return websites.map(site => {
      const [hours, minutes] = site.time.replace(/[^0-9hm]/g, '').split(/h?m?/);
      return {
        name: site.name,
        time: parseInt(hours) + (parseInt(minutes || 0) / 60)
      };
    });
  };

  const chartData = processData();
  const maxTime = Math.max(...chartData.map(item => item.time));

  return (
    <div className="w-8/12 mx-auto bg-gray-800 p-6 rounded-2xl shadow-xl mb-8">
      <h2 className="text-2xl font-semibold mb-6 text-center text-cyan-300">
        Overview
      </h2>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <XAxis
              dataKey="name"
              stroke="#718096"
              tick={{ fill: '#cbd5e0', fontSize: 13 }}
              axisLine={false}
              tickLine={{ stroke: '#4a5568' }}
            />
            <YAxis
              stroke="#718096"
              tick={{ fill: '#cbd5e0', fontSize: 13 }}
              axisLine={false}
              tickLine={{ stroke: '#4a5568' }}
              domain={[0, maxTime * 1.2]}
              tickFormatter={(value) => `${Math.floor(value)}h`}
            />
            <Tooltip
              cursor={{ fill: 'transparent' }}
              contentStyle={{
        
                backgroundColor: '#2d3748',
                border: '1px solid #4a5568',
                borderRadius: '6px',
                color: '#e2e8f0'
              }}
              formatter={(value) => [`${value.toFixed(1)} hours`, 'Time']}
            />
            <Bar
              dataKey="time"
              fill="#63b3ed"
              radius={[6, 6, 0, 0]}
              animationDuration={500}
              strokeWidth={0}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default TimeChart;