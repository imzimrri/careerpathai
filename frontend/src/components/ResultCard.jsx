import React from "react"

const ResultCard = ({ plan }) => {
  if (!plan) return null

  const { title, skillsToLearn, recommendedCourses, codeValidationResult } =
    plan

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>{title || "Your Recommended Career Path"}</h3>
      </div>

      <div style={styles.section}>
        <h4 style={styles.sectionTitle}>🎯 Top 3 Skills to Learn</h4>
        <ol style={styles.list}>
          {skillsToLearn &&
            skillsToLearn.map((skill, index) => (
              <li key={index} style={styles.listItem}>
                {skill}
              </li>
            ))}
        </ol>
      </div>

      <div style={styles.section}>
        <h4 style={styles.sectionTitle}>📚 Recommended Courses</h4>
        <div style={styles.courseList}>
          {recommendedCourses &&
            recommendedCourses.map((course, index) => (
              <a
                key={index}
                href={course.url}
                target="_blank"
                rel="noopener noreferrer"
                style={styles.courseLink}
              >
                <span style={styles.courseName}>{course.skill}</span>
                <span style={styles.arrow}>→</span>
              </a>
            ))}
        </div>
      </div>

      {codeValidationResult && (
        <div style={styles.section}>
          <h4 style={styles.sectionTitle}>✅ Code Snippet Validation</h4>
          <div
            style={{
              ...styles.validationBox,
              ...(codeValidationResult.status === "Success"
                ? styles.validationSuccess
                : styles.validationError),
            }}
          >
            <div style={styles.validationHeader}>
              <strong>{codeValidationResult.skill}</strong>
              <span style={styles.validationStatus}>
                {codeValidationResult.status}
              </span>
            </div>
            <p style={styles.validationDetails}>
              {codeValidationResult.details}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

const styles = {
  container: {
    marginTop: "32px",
    padding: "24px",
    backgroundColor: "#f9fafb",
    borderRadius: "12px",
    border: "1px solid #e5e7eb",
  },
  header: {
    marginBottom: "24px",
    paddingBottom: "16px",
    borderBottom: "2px solid #e5e7eb",
  },
  title: {
    margin: 0,
    fontSize: "20px",
    fontWeight: "600",
    color: "#1a1a1a",
  },
  section: {
    marginBottom: "24px",
  },
  sectionTitle: {
    fontSize: "16px",
    fontWeight: "600",
    color: "#1a1a1a",
    marginBottom: "12px",
  },
  list: {
    margin: 0,
    paddingLeft: "24px",
  },
  listItem: {
    marginBottom: "8px",
    color: "#4b5563",
    fontSize: "15px",
    lineHeight: "1.6",
  },
  courseList: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  courseLink: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "12px 16px",
    backgroundColor: "white",
    border: "1px solid #e5e7eb",
    borderRadius: "8px",
    textDecoration: "none",
    color: "#5b7cff",
    fontSize: "15px",
    transition: "all 0.2s",
  },
  courseName: {
    fontWeight: "500",
  },
  arrow: {
    fontSize: "18px",
    transition: "transform 0.2s",
  },
  validationBox: {
    padding: "16px",
    borderRadius: "8px",
    border: "1px solid",
  },
  validationSuccess: {
    backgroundColor: "#f0fdf4",
    borderColor: "#86efac",
    color: "#166534",
  },
  validationError: {
    backgroundColor: "#fef2f2",
    borderColor: "#fecaca",
    color: "#991b1b",
  },
  validationHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "8px",
  },
  validationStatus: {
    fontSize: "14px",
    fontWeight: "600",
  },
  validationDetails: {
    margin: 0,
    fontSize: "14px",
    lineHeight: "1.6",
  },
}

export default ResultCard
