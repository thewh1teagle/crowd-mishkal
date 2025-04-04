import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  useEffect(() => {
    // Loading meSpeak config and voice files in a vanilla JS way
    (window as any).mespeak.loadConfig("mespeak_config.json");
    (window as any).mespeak.loadVoice("en.json");

    // If you need to check when it's ready, you could listen for an event (if meSpeak emits one)
    // Or simply proceed after loading the files
  }, []); // Empty dependency array means it runs once when the component mounts

  return (
    <>
      <div className='bg-amber-200 w-10 h-10'>
      </div>
    </>
  )
}

export default App
