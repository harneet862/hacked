import Prod from './components/Prod';
import TimeChart from './components/TimeChart';
import TimeComparison from './components/TimeComparison';

function App() {
  const websites = [
    { name: 'Google Docs', time: '2h 30m' },
    { name: 'Khan Academy', time: '1h 15m' },
    { name: 'Notion', time: '45m' },
    { name: 'LeetCode', time: '3h 20m' },
  ];

  const data = [
    {
      title: "Morning Routine",
      start_time: "2024-03-20T06:00:00",
      end_time: "2024-03-20T07:30:00",
      ratio: 0.8
    },
    {
      title: "Breakfast",
      start_time: "2024-03-20T07:30:00",
      end_time: "2024-03-20T08:00:00",
      ratio: 0.5
    },
    {
      title: "Workout Session",
      start_time: "2024-03-20T08:00:00",
      end_time: "2024-03-20T09:00:00",
      ratio: 1.0
    },
    {
      title: "Work Block 1",
      start_time: "2024-03-20T09:00:00",
      end_time: "2024-03-20T11:00:00",
      ratio: 1.2 // Will show as 100%
    },
    {
      title: "Lunch Break",
      start_time: "2024-03-20T12:00:00",
      end_time: "2024-03-20T13:00:00",
      ratio: 0.9
    },
    {
      title: "Client Meeting",
      start_time: "2024-03-20T14:00:00",
      end_time: "2024-03-20T15:30:00",
      ratio: 0.75
    },
    {
      title: "Creative Work",
      start_time: "2024-03-20T16:00:00",
      end_time: "2024-03-20T17:00:00",
      ratio: 0.4
    },
    {
      title: "Evening Relaxation",
      start_time: "2024-03-20T18:00:00",
      end_time: "2024-03-20T20:00:00",
      ratio: 0.6
    }
  ];

  return (
    <div className="min-h-screen bg-gray-800 p-8">
      <div className="w-8/12 mx-auto mb-10">
      <TimeComparison data={data}/>
      </div>
      
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