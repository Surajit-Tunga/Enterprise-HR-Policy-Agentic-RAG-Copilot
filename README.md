# Enterprise HR Policy & Employee Support Agentic RAG Copilot

> **Project status: Development / foundation stage.** This repository currently
> provides a small FastAPI application, a health endpoint, and environment-based
> settings. The retrieval-augmented generation (RAG) workflow, HR document
> ingestion, vector search, web-search fallback, audit persistence, employee
> interface, and production deployment described below are target capabilities;
> they are not yet implemented.

## 1. Executive summary

NovaRetail is a fictional retail company with approximately 3,000 employees.
Its HR team supports employees across topics such as leave, remote work,
payroll, benefits, onboarding, conduct, and HR operations. Employees need a
reliable way to find the policy that applies to their question without having
to know which document or HR contact to search for.

This project proposes an employee-support assistant that retrieves evidence
from approved internal HR documents, generates a concise answer grounded in
that evidence, and shows where the answer came from. If a question depends on
current public information and internal evidence is insufficient, the target
workflow may use an approved public web-search service and clearly label
external information. If the evidence is missing, conflicting, or inadequate,
the assistant should say so and direct the employee to HR instead of guessing.

The business objective is to make routine policy information easier to access
while preserving employee trust, source traceability, and human HR oversight.
This is a decision-support and information-retrieval tool, not an authority
that determines employee eligibility, interprets individual cases, or replaces
HR, Legal, or Payroll.

## 2. Business problem and problem segmentation

### 2.1 Current-state problem

Employees may have difficulty locating the correct, current policy across
multiple HR documents. Keyword search can return broad or irrelevant results,
and a general-purpose chatbot can produce plausible but unsupported answers.
These problems can lead to repeated HR questions, inconsistent employee
understanding, and time spent by HR staff on requests that could be answered
from an approved policy.

This is the project's problem hypothesis, not a measured baseline. No
production usage data, HR ticket analysis, or employee research is currently
included in the repository. Baseline measures should be collected before
business benefits are claimed.

### 2.2 Problem segments

| Segment | Example need | Business impact | Proposed handling |
|---|---|---|---|
| Policy discovery | Find the leave or remote-work policy that applies | Time spent searching; repeat questions to HR | Retrieve relevant passages from approved internal documents and cite them |
| Policy understanding | Summarize a policy section in plain language | Misunderstanding or inconsistent interpretation | Explain only what retrieved evidence supports; retain qualifications and exceptions |
| Time-sensitive public information | Check a current public holiday or government rule | Internal material may not reflect a recent public update | Use public search only when justified, subject to source allowlisting and clear external-source labels |
| Missing or conflicting information | Resolve an uncovered question or inconsistent documents | Unsupported answers can mislead employees | Report the evidence gap or conflict and route the employee to HR |
| Individual or sensitive case | Ask for a decision based on personal circumstances | Privacy, fairness, and employment-decision risk | Do not make the decision; provide general policy information and an HR escalation path |

### 2.3 Stakeholders

- **Employees:** need understandable answers, source context, and a clear way to
  ask HR when the assistant cannot help.
- **HR policy owners:** approve source documents, clarify policy ownership, and
  review content changes and escalations.
- **HR operations:** benefit from fewer repetitive information requests and
  visibility into common evidence gaps.
- **Legal, Privacy, and Security:** review data use, retention, access controls,
  external services, and high-impact use cases before launch.
- **Engineering and operations:** build, secure, monitor, and maintain the
  application and its integrations.

## 3. Objectives, scope, and constraints

### Objectives

1. Make approved internal HR information easier to find and understand.
2. Ground answers in retrieved evidence and expose source references.
3. Keep internal-document retrieval as the primary information path.
4. Use external information only for an explicitly justified, current-information
   need, and distinguish it from company policy.
5. Abstain or escalate when evidence is inadequate, ambiguous, or conflicting.
6. Measure answer quality, safety, employee experience, and operational impact
   before expanding access.

### Initial scope

- Employee questions about approved, general HR policy and operational
  information.
- Search over a curated set of internal HR documents.
- A controlled, optional public-information fallback for appropriate questions.
- Evidence-aware answers, source presentation, abstention, and HR escalation.
- Backend API and, in a later phase, an employee-facing interface.

### Out of scope for the initial release

- Making or recommending employment decisions, such as hiring, discipline,
  promotion, benefits eligibility, or leave approval.
- Replacing HR case management, payroll systems, or formal policy notices.
- Giving legal, medical, tax, or financial advice.
- Accessing or inferring individual employee records unless a separately
  approved, authenticated use case is designed.
- Treating public web pages as a source of company policy.

### Key assumptions and constraints

- NovaRetail and its employee population are fictional project assumptions.
- HR will identify authoritative documents, owners, effective dates, and
  handling rules before ingestion.
- The initial codebase does not yet include those documents or integrations.
- External search, model, and vector database services are proposed
  dependencies; vendor approval, data-processing terms, availability, and cost
  must be assessed before use.
- Applicable employment, privacy, accessibility, records-retention, and
  jurisdictional requirements need review with the relevant business owners.

## 4. Target employee experience

1. An employee submits a question through the eventual interface or API.
2. The application validates the request and applies input, privacy, and
   access-control rules.
3. The workflow searches the approved internal HR knowledge base first.
4. Retrieved passages are assessed for relevance, authority, and sufficiency.
5. If evidence is sufficient, the assistant produces a bounded answer with
   references to the supporting document passages.
6. If internal evidence is insufficient, the workflow may determine whether the
   question requires current public information. If so, it can use the
   approved web-search path and label the resulting information as external.
7. If evidence remains insufficient or sources conflict, the assistant explains
   the limitation and offers an HR escalation route.
8. The system records an appropriately minimized audit event so authorized
   operators can troubleshoot and evaluate the workflow.

The sequence above is a target workflow. It is not currently exposed by the
application.

## 5. Functional requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| FR-01 | Accept an employee question through a defined backend endpoint | Validated request/response contract and API tests |
| FR-02 | Search only approved and indexed HR documents as the primary path | Retrieval integration tests with known documents and expected source metadata |
| FR-03 | Return answers grounded in retrieved evidence with usable source references | Evaluation cases verify factual support and reference correctness |
| FR-04 | Detect inadequate or conflicting evidence and abstain rather than invent policy | Tests for no-result, low-relevance, and conflicting-source cases |
| FR-05 | Invoke public search only for eligible current-information questions | Routing tests confirm internal-first behavior and controlled fallback |
| FR-06 | Mark external results distinctly from internal company policy | Response contract and interface tests verify source labels |
| FR-07 | Provide a clear HR escalation message when the assistant cannot safely answer | API and user-experience tests verify the escalation path |
| FR-08 | Record workflow outcomes for authorized review without unnecessarily storing sensitive content | Audit-schema review and tests for minimized fields and access controls |
| FR-09 | Expose application health for deployment monitoring | Health check returns a successful response when the service is available |
| FR-10 | Load runtime configuration from environment settings and keep secret values out of source control | Configuration tests and secret-handling review |

## 6. Non-functional requirements

- **Privacy and confidentiality:** minimize employee data sent to model or search
  providers; do not ingest individual case records by default.
- **Security:** use authenticated, authorized access where required; protect
  secrets; apply input validation, rate limiting, and secure transport at
  deployment.
- **Reliability:** handle unavailable model, vector-store, and web-search
  dependencies with explicit errors or safe abstention, not fabricated
  success-shaped answers.
- **Traceability:** retain source identity, document version/effective date,
  retrieval outcome, and routing outcome where justified by the audit policy.
- **Maintainability:** keep configuration, ingestion, retrieval, workflow,
  API, and audit responsibilities separated as the application grows.
- **Accessibility and usability:** present clear language, citations, external
  labels, and escalation options in an accessible interface.
- **Performance and cost:** establish service-level targets and per-request
  cost limits during design and validate them with representative workloads.
  No response-time or cost targets have yet been established.
- **Content freshness:** support document ownership, versioning, expiry or
  review dates, and re-indexing when approved content changes.

## 7. Proposed technical implementation

### 7.1 Logical architecture

```text
Employee
   |
   v
Employee interface (planned)
   |
   v
FastAPI application
   |
   v
Question workflow / orchestration (planned)
   |                         |
   v                         v
Internal HR retrieval     Conditional public search
   |                         |
   v                         v
Pinecone vector index     Tavily search (planned)
   \                         /
    \                       /
     v                     v
      Evidence-aware answer generation
                    |
                    v
        Answer + source labels + escalation
                    |
                    v
          Audit events (SQLite planned)
```

The diagram represents the proposed design. The currently implemented
application is limited to the FastAPI application and health route described
in the development status section.

### 7.2 Proposed technology choices

The current configuration names the following intended technologies. Their
presence in configuration does not mean they are integrated or operational.

| Concern | Current direction | Development note |
|---|---|---|
| API service | FastAPI | Implemented as a minimal app with a health route |
| Runtime configuration | `pydantic-settings` and `.env` support | Settings class and cached settings loader are implemented |
| LLM | OpenAI API; configured model defaults to `gpt-4o-mini` | Not called by the current application |
| Embeddings | OpenAI embeddings; configured model defaults to `text-embedding-3-small` | No embedding or ingestion code exists yet |
| Vector search | Pinecone | Index name, namespace, and `top_k` are configurable; no client or index integration exists yet |
| Public web search | Tavily | API key setting exists; no search integration or source policy exists yet |
| Workflow orchestration | LangGraph is proposed in the original implementation plan | Not listed as an installed dependency and not implemented |
| Audit persistence | SQLite is proposed in the original implementation plan | No audit schema or persistence code exists yet |
| Local launch | Uvicorn through `run.py` | Implemented; reload is enabled when `app_env` is `development` |
| Deployment | Docker and DigitalOcean are proposed | No deployment configuration exists yet |

These are provisional choices and should be confirmed against security review,
privacy requirements, operational capabilities, and cost before production use.

### 7.3 Document ingestion and knowledge management (planned)

The ingestion pipeline should be designed before adding documents to a vector
index:

1. **Register approved sources:** record document ID, title, owner, source
   location, jurisdiction or employee group, approval status, effective date,
   review date, and version.
2. **Validate and extract:** accept approved file formats, extract text, detect
   unreadable or empty files, and surface ingestion errors to an operator.
3. **Normalize and segment:** preserve headings and useful structural context;
   split content into retrieval-sized passages without separating important
   exceptions from the rules they qualify.
4. **Attach metadata:** include source ID, version, effective date, section,
   access classification, and permitted audience with each passage.
5. **Embed and index:** create embeddings and upsert passages into the
   configured vector index and namespace.
6. **Verify and publish:** check document counts and representative retrievals
   before making an index version available to employee queries.
7. **Refresh and retire:** re-index approved revisions and remove or deprecate
   superseded material so expired policy is not presented as current.

No source document inventory, chunking policy, indexing pipeline, or lifecycle
controls are present yet. HR policy owners must decide how authoritative
documents and conflicting revisions are resolved.

### 7.4 Question workflow and answer controls (planned)

The proposed workflow should make its routing and evidence decisions explicit:

- Validate the query and avoid collecting unnecessary personal information.
- Classify whether the question is general policy information, time-sensitive
  public information, a sensitive individual case, or outside scope.
- Retrieve from the internal knowledge base first, with source metadata
  preserved.
- Evaluate whether passages are relevant, current, authoritative, and
  sufficient; do not equate a non-empty retrieval result with adequate evidence.
- Optionally reformulate a query to improve retrieval, while preserving the
  original meaning and not adding assumptions.
- Use external search only for eligible questions that genuinely require
  current public information. Keep external results separate from internal
  policy evidence and identify the source and retrieval date.
- Generate a concise answer that is limited to the evidence, identifies
  uncertainty or conflicts, and provides citations.
- Abstain and provide an HR route when evidence does not support a safe answer.
- Bound retries and tool calls to control latency, cost, and repeated
  retrieval; expose failures to the caller or monitoring system.

The original implementation plan names LangGraph for orchestration, Pinecone
for internal retrieval, and Tavily for optional public search. Those
integrations and decision rules remain to be built and tested.

### 7.5 API and interface (planned)

The current API has a `GET /health` endpoint only. A future question endpoint
should define and validate a stable request and response contract before
connecting the user interface. At minimum, the contract should account for:

- A question and request/correlation identifier.
- An answer or explicit abstention status.
- Source references with source type (internal or external), title or stable
  identifier, section where available, and effective/retrieval date.
- An escalation indicator and safe user-facing message.
- A non-sensitive error state for unavailable dependencies.

Authentication, authorization, employee identity, retention behavior, and
whether conversations are stored are not yet specified. These are design
decisions that must be resolved before handling real employee queries.

### 7.6 Audit and observability (planned)

The proposed SQLite audit store should be treated as an operational log, not a
place to retain full employee conversations by default. A privacy review should
determine the minimum useful fields, access policy, retention period, and
redaction approach. Candidate event fields include a request ID, timestamp,
workflow outcome, selected route, source identifiers, latency, and error
category. Logging full prompts, answers, or personal data should require an
explicit need and approval.

Operational monitoring should cover API health, dependency failures, retrieval
quality signals, abstention rates, latency, and usage/cost. Logs must not expose
API keys or other secrets.

## 8. Privacy, security, and responsible use

Because HR questions may include sensitive personal details, privacy and
security controls are prerequisites for any pilot with real employees:

- Use only approved, access-controlled HR content in the knowledge base.
- Do not place employee records or case-management data in the index without a
  separately approved purpose, access model, and retention design.
- Minimize query data sent to external model and search services; review
  provider data handling and contractual protections before integration.
- Keep credentials in environment-based secret management, not source code,
  logs, or committed `.env` files.
- Define authentication, authorization, transport security, abuse protection,
  and administrative access before deployment.
- Treat retrieved document text and public search results as untrusted input;
  they must not be allowed to override application instructions or control
  tools.
- Clearly distinguish company policy from public information and identify
  uncertainty.
- Provide a human escalation path and prohibit automated employment decisions.
- Review data retention, audit access, accessibility, and applicable
  jurisdictional obligations with responsible stakeholders.

These controls are requirements and design considerations, not capabilities
already implemented in this repository.

## 9. Delivery plan and current development status

| Workstream | Intended outcome | Status |
|---|---|---|
| Project foundation | Repository, Python dependencies, application entry point | Partially implemented |
| API foundation | FastAPI app and operational health check | Implemented (`GET /health`) |
| Configuration | Environment-backed settings for app and planned integrations | Implemented as settings only; no integrations are configured or verified |
| Requirements and content governance | Approved use cases, source inventory, ownership, effective-date rules | Not implemented / requires business input |
| Document ingestion | Extraction, segmentation, metadata, indexing, refresh lifecycle | Not implemented |
| Internal retrieval | Pinecone connection, retrieval, source metadata, relevance/sufficiency checks | Not implemented |
| Agent workflow | Internal-first routing, optional search, abstention, bounded retries | Not implemented |
| Answer generation | Grounded responses with source references and safe escalation | Not implemented |
| Audit and monitoring | Privacy-minimized audit events, metrics, and operational alerts | Not implemented |
| Employee interface | Accessible question-and-answer experience | Not implemented |
| Quality assurance | Unit, integration, safety, retrieval, and user-acceptance tests | Not implemented |
| Deployment | Containerization, hosting, secrets, monitoring, and release process | Not implemented |

### Suggested implementation sequence

1. Confirm business requirements, employee use cases, escalation ownership, and
   prohibited use cases with HR, Privacy, Legal, and Security.
2. Inventory and approve source documents; define version, effective-date,
   audience, and deprecation rules.
3. Specify API contracts, data handling, security boundaries, audit retention,
   and measurable pilot success criteria.
4. Implement ingestion and internal retrieval with representative documents
   and source traceability.
5. Implement the internal-first answer path, evidence sufficiency checks,
   abstention, and escalation behavior.
6. Add external search only after defining eligible question categories,
   approved domains/source-quality criteria, labeling, and privacy controls.
7. Add audit and observability with reviewed data minimization.
8. Build the interface and integrate it with the API.
9. Run evaluation, security/privacy review, accessibility review, and a
   controlled HR-led pilot before expanding access.
10. Prepare production deployment and support processes only after pilot
    acceptance and operational ownership are established.

## 10. Success measures and evaluation

No baseline, service-level objective, or acceptance threshold has yet been
established. Define these with HR and engineering before pilot evaluation.
Potential measures include:

- **Evidence correctness:** proportion of answers supported by cited,
  authoritative, current passages.
- **Citation quality:** proportion of citations that resolve to the referenced
  document and support the associated claim.
- **Safe abstention:** behavior on questions with no evidence, conflicting
  policies, sensitive individual circumstances, or out-of-scope requests.
- **Routing quality:** correct internal-first behavior and appropriate use or
  non-use of public search.
- **Employee experience:** task completion, answer clarity, trust, and
  successful escalation when needed.
- **Operational impact:** changes in repetitive HR inquiries, measured against
  an agreed baseline and without assuming all contacts should be avoided.
- **Service health:** availability, dependency error rates, response latency,
  and cost per interaction.
- **Content health:** stale-document rate, ingestion failures, and time from an
  approved policy update to searchable availability.

Evaluation should include representative and adversarially ambiguous
questions, policy exceptions, outdated documents, conflicting sources, and
questions that should trigger abstention or HR escalation. A favorable answer
rate alone is not evidence of quality; unsupported certainty is a failure.

## 11. Risks and mitigations

| Risk | Potential consequence | Proposed mitigation |
|---|---|---|
| Outdated or unapproved source material | Employees receive obsolete or unauthorized guidance | Establish ownership, approval metadata, expiry/review dates, and retirement checks |
| Unsupported model-generated claims | Employee misunderstanding or policy harm | Require evidence-grounded answers, citation checks, sufficiency rules, and abstention |
| Conflicting policies or exceptions | Incorrect simplification of nuanced rules | Preserve document context, detect conflicts, surface uncertainty, and escalate |
| External information mistaken for company policy | Confusion about employee rights or company commitments | Keep source types separate and prominently label external material |
| Sensitive information in queries or logs | Privacy exposure or inappropriate data sharing | Minimize collection, review provider handling, redact where appropriate, and set retention controls |
| Prompt injection in documents or web results | Workflow manipulation or unsafe tool behavior | Treat retrieved content as untrusted data and constrain tools and instructions |
| Integration outage or cost growth | Unavailable or expensive employee service | Add timeouts, bounded retries, explicit failures, usage limits, and monitoring |
| Unclear accountability | Employees rely on an answer without a responsible owner | Define HR ownership, escalation procedures, disclaimers, and support operations |
| Unevaluated business benefit | Overstated savings or low adoption | Establish baselines and pilot measures before claiming impact |

## 12. Repository development notes

At this stage, the repository contains:

- `app/main.py`: creates the FastAPI application and exposes `GET /health`.
- `app/core/config.py`: defines application and planned integration settings,
  loads `.env` values using `pydantic-settings`, and caches the settings object.
- `run.py`: starts the app with Uvicorn using configured host and port; enables
  reload when the environment is `development`.
- `requirements.txt`: lists FastAPI, Uvicorn, Pydantic Settings, and
  python-dotenv.

---
