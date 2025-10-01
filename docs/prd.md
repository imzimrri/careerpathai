This is an excellent step. A Product Requirements Document (PRD) is crucial for keeping your 6-hour MVP focused. This PRD is structured to clearly define the minimal, high-impact features and map them directly to the required hackathon tools.

Product Requirements Document (PRD)

1. Meta Data
   Field Value
   Product Name CareerPath AI
   Document Version 1.0 (MVP)
   Target User Career-changing software engineer/developer
   Goal (Hackathon MVP) Demonstrate a fully functional, end-to-end RAG/Agent system that takes a career goal and returns an actionable, personalized learning path with course recommendations.
   Metric for Success Successful, observable execution of the full technical stack (Weaviate → FriendliAI → aci.dev → Daytona → Comet) within a single user query.

🤖 Team Full Stack BMAD
Custom Gem
This is an excellent step. A Product Requirements Document (PRD) is crucial for keeping your 6-hour MVP focused. This PRD is structured to clearly define the minimal, high-impact features and map them directly to the required hackathon tools.

Product Requirements Document (PRD)

1. Meta Data
   Field Value
   Product Name CareerPath AI
   Document Version 1.0 (MVP)
   Target User Career-changing software engineer/developer
   Goal (Hackathon MVP) Demonstrate a fully functional, end-to-end RAG/Agent system that takes a career goal and returns an actionable, personalized learning path with course recommendations.
   Metric for Success Successful, observable execution of the full technical stack (Weaviate → FriendliAI → aci.dev → Daytona → Comet) within a single user query.

Export to Sheets 2. Goals & Problem
Section Description
Problem Developers struggle to identify clear, actionable steps when switching career paths (e.g., moving from Frontend to ML). Generic online advice is often irrelevant to their specific background.
Solution A personalized AI coach that combines domain-specific RAG with an external tool-calling agent to generate a focused 3-step learning plan, complete with direct course links.
Out of Scope for MVP User authentication, real-time API calls to LinkedIn/Udemy, persistence of user data, complex code execution (e.g., running unit tests), and a sophisticated UI.

🤖 Team Full Stack BMAD
Custom Gem
This is an excellent step. A Product Requirements Document (PRD) is crucial for keeping your 6-hour MVP focused. This PRD is structured to clearly define the minimal, high-impact features and map them directly to the required hackathon tools.

Product Requirements Document (PRD)

1. Meta Data
   Field Value
   Product Name CareerPath AI
   Document Version 1.0 (MVP)
   Target User Career-changing software engineer/developer
   Goal (Hackathon MVP) Demonstrate a fully functional, end-to-end RAG/Agent system that takes a career goal and returns an actionable, personalized learning path with course recommendations.
   Metric for Success Successful, observable execution of the full technical stack (Weaviate → FriendliAI → aci.dev → Daytona → Comet) within a single user query.

Export to Sheets 2. Goals & Problem
Section Description
Problem Developers struggle to identify clear, actionable steps when switching career paths (e.g., moving from Frontend to ML). Generic online advice is often irrelevant to their specific background.
Solution A personalized AI coach that combines domain-specific RAG with an external tool-calling agent to generate a focused 3-step learning plan, complete with direct course links.
Out of Scope for MVP User authentication, real-time API calls to LinkedIn/Udemy, persistence of user data, complex code execution (e.g., running unit tests), and a sophisticated UI.

Export to Sheets 3. User Stories (MVP Scope)
These stories define the absolute minimum features required to demonstrate the full stack.

ID Story Technical Requirement/Tool
S1 As a user, I can input my Current Role and my Target Role so the system can understand my career change goal. Frontend/UI: Two simple text fields and a submit button.
S2 As the AI Agent, I can retrieve relevant skills and job knowledge for the Target Role from a specialized knowledge base to ensure the advice is accurate. Weaviate (RAG): Retrieve documents based on the semantic similarity of the Target Role.
S3 As the AI Agent, I can analyze the retrieved knowledge and identify the top 3 missing skills required for the transition. FriendliAI (LLM): Orchestrate the RAG query and perform the skill-gap analysis reasoning.
S4 As the AI Agent, I can call an external tool to search for learning content for each recommended skill so I can provide actionable course links. aci.dev (Agent Gateway): Call the search_learning_content(skill: str) mock tool.
S5 As the AI Agent, I can generate a code snippet demonstrating the first recommended skill (e.g., a "Hello World" of that technology). FriendliAI (LLM): Generate a short, 5-line Python script.
S6 As the AI Agent, I can send the generated code snippet to a secure sandbox for validation to prove the code is functional and safe. Daytona (Safe Runtime): Execute the code snippet and return a simple "Success/Failure" status.
S7 As a developer, I want all RAG queries, LLM calls, and tool actions to be logged and tracked so I can debug and measure the agent's performance. Comet (Observability): Log the full trace, including latency, RAG context, and Daytona execution results.

🤖 Team Full Stack BMAD
Custom Gem
This is an excellent step. A Product Requirements Document (PRD) is crucial for keeping your 6-hour MVP focused. This PRD is structured to clearly define the minimal, high-impact features and map them directly to the required hackathon tools.

Product Requirements Document (PRD)

1. Meta Data
   Field Value
   Product Name CareerPath AI
   Document Version 1.0 (MVP)
   Target User Career-changing software engineer/developer
   Goal (Hackathon MVP) Demonstrate a fully functional, end-to-end RAG/Agent system that takes a career goal and returns an actionable, personalized learning path with course recommendations.
   Metric for Success Successful, observable execution of the full technical stack (Weaviate → FriendliAI → aci.dev → Daytona → Comet) within a single user query.

Export to Sheets 2. Goals & Problem
Section Description
Problem Developers struggle to identify clear, actionable steps when switching career paths (e.g., moving from Frontend to ML). Generic online advice is often irrelevant to their specific background.
Solution A personalized AI coach that combines domain-specific RAG with an external tool-calling agent to generate a focused 3-step learning plan, complete with direct course links.
Out of Scope for MVP User authentication, real-time API calls to LinkedIn/Udemy, persistence of user data, complex code execution (e.g., running unit tests), and a sophisticated UI.

Export to Sheets 3. User Stories (MVP Scope)
These stories define the absolute minimum features required to demonstrate the full stack.

ID Story Technical Requirement/Tool
S1 As a user, I can input my Current Role and my Target Role so the system can understand my career change goal. Frontend/UI: Two simple text fields and a submit button.
S2 As the AI Agent, I can retrieve relevant skills and job knowledge for the Target Role from a specialized knowledge base to ensure the advice is accurate. Weaviate (RAG): Retrieve documents based on the semantic similarity of the Target Role.
S3 As the AI Agent, I can analyze the retrieved knowledge and identify the top 3 missing skills required for the transition. FriendliAI (LLM): Orchestrate the RAG query and perform the skill-gap analysis reasoning.
S4 As the AI Agent, I can call an external tool to search for learning content for each recommended skill so I can provide actionable course links. aci.dev (Agent Gateway): Call the search_learning_content(skill: str) mock tool.
S5 As the AI Agent, I can generate a code snippet demonstrating the first recommended skill (e.g., a "Hello World" of that technology). FriendliAI (LLM): Generate a short, 5-line Python script.
S6 As the AI Agent, I can send the generated code snippet to a secure sandbox for validation to prove the code is functional and safe. Daytona (Safe Runtime): Execute the code snippet and return a simple "Success/Failure" status.
S7 As a developer, I want all RAG queries, LLM calls, and tool actions to be logged and tracked so I can debug and measure the agent's performance. Comet (Observability): Log the full trace, including latency, RAG context, and Daytona execution results.

Export to Sheets 4. Technical Specifications & Tool Mapping
Tool Specification for MVP Data Flow Step
Weaviate Single collection (e.g., JobKnowledge). Use near_text (vector search) for retrieval on the user's Target Role input. Step 2 (Retrieval)
FriendliAI Use a fast, small-to-medium-sized model (e.g., Llama 3 8B) for quick inference. The model must be capable of Tool-Calling/Function-Calling to utilize aci.dev. Step 3 (Reasoning/Generation)
aci.dev Implement a single mock tool (search_learning_content) that returns a JSON list of hard-coded YouTube URLs for a few expected input skills. Step 4 (Tool Action)
Daytona API call to provision a simple sandboxed container, execute a hard-coded Python script (the one generated in S5), and terminate the container. Step 6 (Code Validation)
Comet (Opik) Use the SDK to log the Weaviate retrieval results (context), the FriendliAI prompt/response, and the Daytona execution status, all within a single trace. Step 7 (Logging)

5. Success Criteria (Demo Script)
   The demo is a success if the presenter can:

Input a career goal (S1).

Receive a final, synthesized answer that includes:

The 3 skills to learn (S3).

Links to external courses (from the aci.dev tool call) (S4).

A confirmation that a code snippet was generated and securely validated (S6).

Show the Comet Dashboard displaying the single, end-to-end trace log for that specific query (S7).
