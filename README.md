# Enterprise HR Policy & Employee Support Agentic RAG Copilot

## Problem

NovaRetail is a fictional retail company with 3,000 employees. Its HR team
maintains documents about leave, remote work, payroll, benefits, onboarding,
conduct, and HR operations.

Employees frequently ask HR questions because they cannot easily find the
right policy. Keyword searches can return too many documents, and a general
chatbot may provide inaccurate answers. Internal documents may also lack
current public information, such as the latest public holiday rules.

The goal is to create an HR support assistant that answers from company
documents when possible, uses public web search only when internal information
is insufficient, and makes clear when an answer comes from external sources.
When the available evidence does not support an answer, the assistant should
say so rather than guess.

## Implementation

The project will be developed in these steps:

1. **Plan the project lifecycle.** Define the requirements, system design,
   implementation, testing, deployment, and ongoing improvement stages.
2. **Design the HR solution.** Identify employee questions, trusted HR
   documents, and cases that require current public information.
3. **Plan the agent workflow.** Search the private HR knowledge base first,
   assess the retrieved evidence, and use web search only when internal
   evidence is insufficient. Rewrite unclear queries and stop with an
   insufficient-evidence response when the available sources do not support
   an answer.
4. **Set up the application structure.** Organize the project into separate
   modules for configuration, document ingestion, retrieval, the LangGraph
   workflow, API routes, and audit logging.
5. **Configure the application.** Read service credentials and settings from
   environment variables, keeping secret values out of the source code.
6. **Load and process HR documents.** Read the source documents and split
   their contents into passages suitable for retrieval.
7. **Build the knowledge index.** Create embeddings for the passages and
   store them in a Pinecone index for private HR document search.
8. **Build the decision workflow.** Use LangGraph to route questions, retrieve
   and grade private evidence, fall back to Tavily when needed, rewrite
   queries, and generate evidence-based answers.
9. **Add audit logging.** Store the workflow decisions and outcomes in
   SQLite so the path taken for a response can be reviewed.
10. **Develop the backend and interface.** Create FastAPI endpoints for the
    application and connect them to the workflow and employee web interface.
11. **Integrate and test the application.** Verify the private knowledge
    path, web-search fallback, insufficient-evidence behavior, and complete
    interaction between the interface and backend.
12. **Prepare deployment.** Package the application with Docker and deploy it
    to a DigitalOcean cloud environment.
---