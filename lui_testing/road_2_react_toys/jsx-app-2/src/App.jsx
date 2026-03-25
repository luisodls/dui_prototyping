import { useState } from 'react'
import './App.css'

function App() {
  const [count1, setCount1] = useState(0)
  const [count2, setCount2] = useState(0)

  return (
    <section id="center">
      <div>
        <h1>My App #2</h1>
        <button
          //comment the next line and see how the app changes it appearance
          className="counter"

          onClick={() => setCount1((count1) => count1 + 1)}
        >
        Count is {count1}
        </button>

        <button
          //comment the next line and see how the app changes it appearance
          className="counter"

          onClick={() => setCount2((count2) => count2 + 1)}
        >
        Count is {count2}
        </button>

        </div>
    </section>
  )
}

export default App
