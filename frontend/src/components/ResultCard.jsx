import React from "react"

const ResultCard = ({ plan }) => {
  if (!plan) return null

  const { title, skillsToLearn, skillsWithCourses, codeValidationResult } = plan

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
        {skillsWithCourses &&
          skillsWithCourses.map((skillData, skillIndex) => (
            <div key={skillIndex} style={styles.skillSection}>
              <h5 style={styles.skillName}>{skillData.skill}</h5>
              <div style={styles.courseList}>
                {skillData.courses &&
                  skillData.courses.map((course, courseIndex) => (
                    <a
                      key={courseIndex}
                      href={course.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={styles.courseLink}
                    >
                      <div style={styles.courseInfo}>
                        <span style={styles.courseTitle}>{course.title}</span>
                        <span style={styles.courseMeta}>
                          {course.platform} • {course.duration || "N/A"} •{" "}
                          {course.level || "All Levels"}
                        </span>
                      </div>
                      <span style={styles.arrow}>→</span>
                    </a>
                  ))}
              </div>

              {skillData.code_snippet && (
                <div style={styles.codeSection}>
                  <h6 style={styles.codeTitle}>💻 Code Example</h6>
                  <pre style={styles.codeBlock}>
                    <code>{skillData.code_snippet.code}</code>
                  </pre>
                  <p style={styles.codeDescription}>
                    {skillData.code_snippet.description}
                  </p>

                  {skillData.code_snippet.validation && (
                    <div
                      style={{
                        ...styles.validationBox,
                        ...(skillData.code_snippet.validation.status ===
                        "Success"
                          ? styles.validationSuccess
                          : styles.validationError),
                      }}
                    >
                      <div style={styles.validationHeader}>
                        <strong>
                          Validation: {skillData.code_snippet.validation.status}
                        </strong>
                        <span style={styles.validationTime}>
                          {skillData.code_snippet.validation.execution_time}s
                        </span>
                      </div>
                      {skillData.code_snippet.validation.output && (
                        <pre style={styles.outputBlock}>
                          {skillData.code_snippet.validation.output}
                        </pre>
                      )}
                      <p style={styles.validationDetails}>
                        {skillData.code_snippet.validation.details}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
      </div>

      {codeValidationResult && (
        <div style={styles.section}>
          <h4 style={styles.sectionTitle}>✅ Overall Validation Status</h4>
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
  skillSection: {
    marginBottom: "20px",
    padding: "16px",
    backgroundColor: "white",
    borderRadius: "8px",
    border: "1px solid #e5e7eb",
  },
  skillName: {
    fontSize: "15px",
    fontWeight: "600",
    color: "#1a1a1a",
    marginTop: 0,
    marginBottom: "12px",
  },
  courseList: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    marginBottom: "12px",
  },
  courseLink: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "12px",
    backgroundColor: "#f9fafb",
    border: "1px solid #e5e7eb",
    borderRadius: "6px",
    textDecoration: "none",
    transition: "all 0.2s",
  },
  courseInfo: {
    display: "flex",
    flexDirection: "column",
    gap: "4px",
    flex: 1,
  },
  courseTitle: {
    fontWeight: "500",
    color: "#1a1a1a",
    fontSize: "14px",
  },
  courseMeta: {
    fontSize: "12px",
    color: "#6b7280",
  },
  arrow: {
    fontSize: "18px",
    color: "#5b7cff",
    marginLeft: "12px",
  },
  codeSection: {
    marginTop: "16px",
    padding: "12px",
    backgroundColor: "#f9fafb",
    borderRadius: "6px",
  },
  codeTitle: {
    fontSize: "14px",
    fontWeight: "600",
    color: "#1a1a1a",
    marginTop: 0,
    marginBottom: "8px",
  },
  codeBlock: {
    backgroundColor: "#1a1a1a",
    color: "#f9fafb",
    padding: "12px",
    borderRadius: "4px",
    fontSize: "13px",
    lineHeight: "1.5",
    overflow: "auto",
    marginBottom: "8px",
    fontFamily: "monospace",
  },
  codeDescription: {
    fontSize: "13px",
    color: "#6b7280",
    margin: "0 0 12px 0",
  },
  outputBlock: {
    backgroundColor: "#f3f4f6",
    color: "#1a1a1a",
    padding: "8px",
    borderRadius: "4px",
    fontSize: "12px",
    marginTop: "8px",
    marginBottom: "8px",
    fontFamily: "monospace",
  },
  validationBox: {
    padding: "12px",
    borderRadius: "6px",
    border: "1px solid",
    marginTop: "8px",
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
    fontSize: "13px",
  },
  validationStatus: {
    fontSize: "14px",
    fontWeight: "600",
  },
  validationTime: {
    fontSize: "12px",
    color: "#6b7280",
  },
  validationDetails: {
    margin: 0,
    fontSize: "13px",
    lineHeight: "1.6",
  },
}

export default ResultCard
