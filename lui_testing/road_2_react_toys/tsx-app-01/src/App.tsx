import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <section id="center">
      <div>
        <h1>My App #1</h1>
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
