import Prod from './components/Prod.jsx';



function App() {


  const websites = [
    { name: 'Google Docs', time: '2h 30m' },
    { name: 'Khan Academy', time: '1h 15m' },
    { name: 'Notion', time: '45m' },
    { name: 'LeetCode', time: '3h 20m' },
  ];

  return (
    <>
      <Prod websites={websites} />
      <Prod websites={websites} />
      <Prod websites={websites} />
      <Prod websites={websites} />
      <Prod websites={websites} />
      <Prod websites={websites} />
    </>
  )
}

export default App
