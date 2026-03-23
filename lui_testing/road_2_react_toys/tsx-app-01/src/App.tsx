import { useState } from 'react'

/*
 * when we trim down to a simpler app the next 4 imports are no longer needed

 import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
*/

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
    <h1>My App #1</h1>
    <button onClick={() => setCount(count + 1)}>
    Clicked {count} times
    </button>
    </div>
  )
}

export default App
