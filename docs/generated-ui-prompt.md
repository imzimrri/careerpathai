You are an expert React developer specializing in creating clean, responsive, and modern user interfaces with Bootstrap.

Your task is to build a single-page application for a project called "CareerPath AI".

---

### **1. High-Level Goal**

Create a responsive, single-page React application that allows a user to input their current and target job roles. The application will then display a generated career plan. For this task, you will simulate the API call and use mock data for the result.

---

### **2. Detailed, Step-by-Step Instructions**

1.  **Create the main component:** Build a single functional React component named `CareerPathGenerator`.
2.  **Set up state:** Use the `useState` hook to manage the following states:
    - `currentRole` (string, initial: '')
    - `targetRole` (string, initial: '')
    - `plan` (null or object, initial: null)
    - `isLoading` (boolean, initial: false)
    - `error` (string, initial: '')
3.  **Build the UI:**
    - Use a main `container` from Bootstrap to center the content and apply a `max-width`.
    - Add a heading `<h1>` with the text "CareerPath AI".
    - Create a `<form>` element.
    - Inside the form, add two text input fields, each wrapped in a `form-group`.
      - The first should have a `<label>` "Your Current Role".
      - The second should have a `<label>` "Your Target Role".
    - Add a primary Bootstrap `<button>` with the text "Generate Path". This button should be of `type="submit"`.
4.  **Implement Interaction Logic:**
    - The submit button must be `disabled` if `currentRole` or `targetRole` is empty.
    - When the form is submitted, prevent the default form submission, set `isLoading` to `true`, clear any previous `plan` and `error`, and call a simulated fetch function.
5.  **Simulate API Call:**
    - Create an `async` function for the form's `onSubmit` handler.
    - Inside, use `setTimeout` to create a 2-second delay to simulate a network request.
    - After the delay, set `isLoading` to `false` and populate the `plan` state with the mock data provided below.
6.  **Render Conditional Content:**
    - If `isLoading` is `true`, display a Bootstrap `Spinner` component.
    - If `error` has a value, display it in a Bootstrap `Alert` with the `danger` variant.
    - If a `plan` exists, display the results inside a Bootstrap `Card`. The steps in the plan should be rendered as a numbered list (`<ol>`).

---

### **3. Code Examples, Data Structures & Constraints**

- **Tech Stack:** Use React (with functional components and hooks) and Bootstrap 5 for all styling. Do NOT use TypeScript or any other libraries.
- **Styling:**
  - **Color Palette:** Primary: `#007bff`, Error: `#dc3545`, Card Background: `#f8f9fa`, Text: `#343a40`.
  - **Typography:** Use a system font stack. The `<h1>` should be around 2.25rem, and body text should be 1rem.
  - **Layout:** The main container should have padding (`p-4` or `p-5`).
- **Mock Result Data Structure:** When the simulated API call succeeds, use this object to set the `plan` state:
  ```json
  {
    "title": "Your Path from Frontend Developer to Machine Learning Engineer",
    "steps": [
      "Master Python fundamentals and key libraries (NumPy, Pandas).",
      "Learn core machine learning concepts and algorithms (Supervised/Unsupervised Learning).",
      "Build a portfolio of 3-5 projects demonstrating your ML skills."
    ]
  }
  ```
- **Constraints:**
  - Do NOT use class components.
  - Do NOT install or use any external libraries other than React and Bootstrap.
  - Ensure the UI is responsive and looks good on both mobile and desktop screens.

---

### **4. Scope**

You should only create the code for this single React component. Assume that React and Bootstrap are already set up in the project. Provide the complete code for the `CareerPathGenerator.js` file.
