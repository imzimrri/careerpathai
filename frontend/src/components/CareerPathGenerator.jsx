import React, { useState } from "react"
import { generateCareerPath } from "../services/api"
import LoadingSpinner from "./LoadingSpinner"
import ErrorAlert from "./ErrorAlert"
import ResultCard from "./ResultCard"
import "../App.css"

const CareerPathGenerator = () => {
  const [currentRole, setCurrentRole] = useState("")
  const [targetRole, setTargetRole] = useState("")
  const [plan, setPlan] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")
    setPlan(null)

    try {
      const result = await generateCareerPath(currentRole, targetRole)
      setPlan(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const isButtonDisabled = !currentRole || !targetRole || isLoading

  return (
    <div className="app-container">
      <div className="badge">
        <span className="badge-icon">✨</span>
        AI-Powered Career Planning
      </div>

      <h1 className="main-title">CareerPath AI</h1>

      <p className="subtitle">
        Let artificial intelligence guide your professional journey
        <br />
        with personalized career development plans
      </p>

      <div className="form-card">
        <h2>Generate Your Career Path</h2>
        <p className="description">
          Enter your current role and where you'd like to be, and we'll create a
          personalized roadmap
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="currentRole">Your Current Role</label>
            <input
              type="text"
              id="currentRole"
              value={currentRole}
              onChange={(e) => setCurrentRole(e.target.value)}
              placeholder="e.g., Frontend Developer"
            />
          </div>

          <div className="form-group">
            <label htmlFor="targetRole">Your Target Role</label>
            <input
              type="text"
              id="targetRole"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g., Machine Learning Engineer"
            />
          </div>

          <button
            type="submit"
            className="submit-button"
            disabled={isButtonDisabled}
          >
            {isLoading ? "Generating..." : "Generate Path"}
            {!isLoading && <span className="arrow-icon">→</span>}
          </button>
        </form>

        {isLoading && (
          <div className="loading-container">
            <LoadingSpinner />
          </div>
        )}

        {error && (
          <div className="error-container">
            <ErrorAlert message={error} />
          </div>
        )}

        {plan && (
          <div className="results-container">
            <ResultCard plan={plan} />
          </div>
        )}
      </div>
    </div>
  )
}

export default CareerPathGenerator
