import Prod from './components/Prod';
import TimeChart from './components/TimeChart';

function App() {
  const websites = [
    { name: 'Google Docs', time: '2h 30m' },
    { name: 'Khan Academy', time: '1h 15m' },
    { name: 'Notion', time: '45m' },
    { name: 'LeetCode', time: '3h 20m' },
  ];

  return (
    <div className="min-h-screen bg-gray-800 p-8">
      <TimeChart websites={websites} />
      
      <div className="grid gap-6 max-w-4xl mx-auto w-full">
        <Prod websites={websites} category="Productivity"/>
        <Prod websites={websites} category="Education"/>
        <Prod websites={websites} category="Fitness" />
        <Prod websites={websites} category="Entertainment"/>
        <Prod websites={websites} category="Social Media"/>
        <Prod websites={websites} category="Blogging"/>
        <Prod websites={websites} category="News"/>
        <Prod websites={websites} category="Travel"/>
        <Prod websites={websites} category="Other"/>
      </div>
    </div>
  );
}

export default App;