export const generateCareerPath = async (currentRole, targetRole) => {
  const response = await fetch('/api/generate-career-path', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ currentRole, targetRole }),
  });

  if (!response.ok) {
    // Try to parse a structured error from the backend, otherwise throw a generic error
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.error?.message || 'An unexpected error occurred while generating the path.');
  }

  return response.json();
};
