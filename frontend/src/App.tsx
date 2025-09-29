import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Get API URL from environment variable
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  // Fetch count from API
  useEffect(() => {
    const fetchCount = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await fetch(`${API_URL}/count`)
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        setCount(data.count || 0)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch count')
        console.error('Error fetching count:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchCount()
  }, [API_URL])

  // Increment count via API
  const incrementCount = async () => {
    try {
      setError(null)
      const response = await fetch(`${API_URL}/count/increment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setCount(data.count || 0)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to increment count')
      console.error('Error incrementing count:', err)
    }
  }

  return (
    <>
      <h1>Mon premier compteur!</h1>
      <div className="card">
        {loading ? (
          <p>Loading count...</p>
        ) : error ? (
          <div>
            <p style={{ color: 'red' }}>Error: {error}</p>
            <button onClick={() => window.location.reload()}>
              Retry
            </button>
          </div>
        ) : (
          <button onClick={incrementCount}>
            count is {count}
          </button>
        )}
        <p>
          Cliquez sur le bouton pour incrémenter le compteur.
        </p>
      </div>
    </>
  )
}

export default App
