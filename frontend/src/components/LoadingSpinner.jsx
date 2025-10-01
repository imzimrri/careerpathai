import React from "react"

const LoadingSpinner = () => {
  return (
    <div style={styles.container}>
      <div style={styles.spinner}></div>
      <p style={styles.text}>Generating your personalized career path...</p>
    </div>
  )
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "16px",
    padding: "24px",
  },
  spinner: {
    width: "40px",
    height: "40px",
    border: "4px solid #e5e7eb",
    borderTop: "4px solid #5b7cff",
    borderRadius: "50%",
    animation: "spin 1s linear infinite",
  },
  text: {
    color: "#6b7280",
    fontSize: "14px",
    margin: 0,
  },
}

// Add keyframe animation
const styleSheet = document.styleSheets[0]
const keyframes = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`
if (styleSheet && !document.querySelector("style[data-spinner]")) {
  const style = document.createElement("style")
  style.setAttribute("data-spinner", "true")
  style.textContent = keyframes
  document.head.appendChild(style)
}

export default LoadingSpinner
