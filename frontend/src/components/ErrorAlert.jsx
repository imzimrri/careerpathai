import React from "react"

const ErrorAlert = ({ message }) => {
  if (!message) return null

  return (
    <div style={styles.alert}>
      <span style={styles.icon}>⚠️</span>
      <span style={styles.message}>{message}</span>
    </div>
  )
}

const styles = {
  alert: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "16px",
    backgroundColor: "#fef2f2",
    border: "1px solid #fecaca",
    borderRadius: "8px",
    color: "#991b1b",
    fontSize: "14px",
  },
  icon: {
    fontSize: "20px",
  },
  message: {
    flex: 1,
  },
}

export default ErrorAlert
