import { useState } from 'react'

/*
 * when we trim down to a simpler app the next 4 imports are no longer needed

import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
*/

import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <section id="center">
      <div>
        <h1>My App #2</h1>
        <button
          className="counter"
          onClick={() => setCount((count) => count + 1)}
        >
        Count is {count}
        </button>
      </div>
    </section>
  )
}

export default App
