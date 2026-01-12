# Vibe Coding Practical Guide for Researchers

> From "Vibe Coding" to "Spec-Driven Development": A Comprehensive Guide for AI-Assisted Research Programming

## Table of Contents

- [1. Understanding Vibe Coding](#1-understanding-vibe-coding)
  - [1.1 The Programming Paradigm Shift](#11-the-programming-paradigm-shift)
  - [1.2 What is Vibe Coding?](#12-what-is-vibe-coding)
  - [1.3 When to Use vs. Avoid](#13-when-to-use-vs-avoid)
  - [1.4 Critical Pitfalls](#14-critical-pitfalls)
- [2. Evolution: From Vibe to Spec-Driven](#2-evolution-from-vibe-to-spec-driven)
  - [2.1 The Three Levels](#21-the-three-levels)
  - [2.2 Core Mindset Shift](#22-core-mindset-shift)
- [3. Tool Ecosystem (2025)](#3-tool-ecosystem-2025)
  - [3.1 AI-Native IDEs](#31-ai-native-ides)
  - [3.2 CLI Tools](#32-cli-tools)
  - [3.3 Recommended Combinations](#33-recommended-combinations)
- [4. Prompt Engineering Essentials](#4-prompt-engineering-essentials)
  - [4.1 The 5W1H Framework](#41-the-5w1h-framework)
  - [4.2 Context Management](#42-context-management)
  - [4.3 Six Key Techniques](#43-six-key-techniques)
- [5. Project Structure & Workflow](#5-project-structure--workflow)
  - [5.1 Recommended Project Structure](#51-recommended-project-structure)
  - [5.2 Documentation Strategy](#52-documentation-strategy)
- [6. Step-by-Step Implementation Guide](#6-step-by-step-implementation-guide)
  - [6.1 Phase 1: Project Scaffolding](#61-phase-1-project-scaffolding)
  - [6.2 Phase 2: Detailed Planning](#62-phase-2-detailed-planning)
  - [6.3 Phase 3: Iterative Implementation](#63-phase-3-iterative-implementation)
  - [6.4 Phase 4: Review & Documentation](#64-phase-4-review--documentation)
- [7. Debugging Workflow](#7-debugging-workflow)
- [8. Version Control & Experiment Tracking](#8-version-control--experiment-tracking)
- [9. Prompt Templates](#9-prompt-templates)
- [10. Advanced Skills (2025 Latest)](#10-advanced-skills-2025-latest)
  - [10.1 Rules Files Configuration](#101-rules-files-configuration-mdc--cursorrules)
  - [10.2 Multi-Agent Collaboration Strategy](#102-multi-agent-collaboration-strategy)
  - [10.3 Background Agents & Async Workflows](#103-background-agents--async-workflows)
  - [10.4 MCP Integration](#104-mcp-model-context-protocol-integration)
  - [10.5 Security Considerations](#105-security-considerations-for-ai-generated-code)
  - [10.6 Context Window Optimization](#106-context-window-optimization)
  - [10.7 Agentic Workflow Patterns](#107-agentic-workflow-patterns)
  - [10.8 Test-Driven AI Development](#108-test-driven-ai-development-tdad)
  - [10.9 Prompt Versioning & Experimentation](#109-prompt-versioning--experimentation)
- [11. Best Practices & Tips](#11-best-practices--tips)
- [References](#references)

---

## 1. Understanding Vibe Coding

### 1.1 The Programming Paradigm Shift

The evolution of programming languages has consistently raised abstraction levels, moving the human-machine interface closer to natural language.

| Dimension | Traditional Coding | AI-Assisted Coding | Essence of Change |
|-----------|-------------------|-------------------|-------------------|
| Core Skill | Syntax memorization, API lookup | Requirement description, Logic validation | Memory → Expression |
| Learning Curve | Steep (months-years) | Gentle (days-weeks) | Lower barrier |
| Dev Speed | Slow (manual writing + debugging) | Fast (second-level generation + iteration) | Efficiency breakthrough |
| Applicable Scope | All scenarios (incl. low-level) | 80% routine research tasks | 80/20 rule |

**What AI Excels At:**
- Standard algorithm implementation (sorting, statistics, GIS operations)
- Code language conversion (Python ↔ R)
- Error diagnosis and fix suggestions
- Documentation and comment generation

**AI's Limitations:**
- Complex business logic (requires deep domain knowledge)
- Innovative algorithm design (non-standard textbook content)
- System-level architecture decisions
- Extreme performance optimization (hardware-level)

### 1.2 What is Vibe Coding?

**Definition:** An exploratory, iterative programming method centered on natural language dialogue. Characterized by "feeling-driven" development—describing requirements intuitively and rapidly iterating through trial and error.

**Three Core Characteristics:**

| Feature | Description |
|---------|-------------|
| 🚪 **Low Barrier** | No need to memorize complex syntax; natural language becomes code |
| ⚡ **High Speed** | Ideas to code in minutes; rapid validation |
| 🔍 **Strong Exploration** | Discover unknown possibilities through dialogue |

### 1.3 When to Use vs. Avoid

#### ✅ Recommended (Code < 200 lines)
- One-time data processing scripts
- Rapid prototype validation
- Learning new tech stacks
- Quick exploratory analysis

#### ❌ Not Suitable (Code > 500 lines)
- Long-term maintenance projects
- Team collaboration projects
- Core paper algorithms
- Production systems

### 1.4 Critical Pitfalls

| Pitfall | Description | Consequence |
|---------|-------------|-------------|
| **Scale Disaster** | After 500 lines, code becomes a "patch pile" | Maintenance cost grows exponentially |
| **Understanding Bias** | Domain term ambiguity (e.g., "building density" has 3 definitions) | AI lacks context and doesn't proactively clarify |
| **Documentation Drift** | Direct code modification without updating docs | "Code-doc mismatch", docs become useless |

---

## 2. Evolution: From Vibe to Spec-Driven

### 2.1 The Three Levels

```
Level 1: Vibe Coding          Level 2: Spec-First           Level 3: Spec-as-Source
────────────────────────────────────────────────────────────────────────────────────
• Dialogue-driven             • Definition-first            • Auto-generation
• Extreme speed               • Anchored iteration          • 100% consistency
• Unstable quality            • Reliable quality            • Team collaboration base
```

**Analogy:**
- **Vibe Coding** = Verbal communication for building a house ("Chat and modify on the fly")
  - Result: House may be crooked, details missed
- **Spec-Driven** = Blueprint-first construction ("All details in blueprints")
  - Result: Quality guaranteed, reproducible

### 2.2 Core Mindset Shift

> "Vibe Coding is the fast food of programming—tasty but unhealthy. Spec-driven is healthy fast food—both fast and reliable."

**Key Transformation:** From **dialogue-driven** → **specification-driven**

---

## 3. Tool Ecosystem (2025)

### 3.1 AI-Native IDEs

| Tool | Price | Key Features | Best For |
|------|-------|--------------|----------|
| **Cursor** | $20/mo Pro | Multi-model support, strong codebase understanding | General development |
| **Windsurf** | Credit-based | Flexible pricing, good for exploration | Budget-conscious users |
| **Antigravity** | Free | Completely free (needs Google account) | Zero-budget projects |
| **Trae** | Free | Local deployment option | Privacy-sensitive work |
| **Kiro** | Subscription | Spec-driven workflow | Enterprise standardization |

### 3.2 CLI Tools

| Tool | Model | Price | Strengths | Best For |
|------|-------|-------|-----------|----------|
| **Claude Code** | Claude 4.5 Sonnet/Opus | $20 Pro / $200 Max | Project memory, 200K context, multi-step decomposition | Large project refactoring, paper algorithm reproduction |
| **Gemini CLI** | Gemini 3.0 Pro | Free (60 req/min) | 1M context window, zero cost | Zero-budget, large text analysis, teaching |
| **Codex CLI** | GPT-5.2/5.1 | $20 Plus / $200 Pro | Native multimodal, real-time web, plugins | Rapid prototypes, API integration |
| **Droid** | Factory AI | Subscription | CI/CD integration, code isolation | Enterprise DevOps automation |

### 3.3 Recommended Combinations

| Budget | Combination |
|--------|-------------|
| **Zero Budget** | Antigravity + Trae + Gemini CLI |
| **Standard** | Cursor Pro ($20/mo) + Gemini CLI |
| **Enterprise** | Kiro (standardization) + Cursor Team |

**Core Principle:** Combination > Single choice

---

## 4. Prompt Engineering Essentials

### 4.1 The 5W1H Framework

Structure your prompts using this framework for clarity:

| Element | Question | Example |
|---------|----------|---------|
| **What** | What task to accomplish? | "Parse CSV and calculate statistics" |
| **Why** | What's the purpose? | "For monthly sales report" |
| **Where** | Which files/modules? | "In `src/analysis/` directory" |
| **When** | Constraints/conditions? | "Processing time < 10s" |
| **Who** | Role/expertise needed? | "As a GIS expert proficient in GeoPandas" |
| **How** | Technical approach? | "Use pandas, matplotlib only" |

### 4.2 Context Management

**Context Layering Strategy:**

```
├── Project Level (@codebase)
│   └── Full project understanding
├── Document Level (@docs)
│   └── Indexed documentation libraries
├── File Level (@filename.py)
│   └── Specific file context
└── Symbol Level (@function_name)
    └── Precise function/class reference
```

**Common @ References:**

| Reference | Purpose | Example |
|-----------|---------|---------|
| `@file` | Include specific file | `@model.py` |
| `@folder` | Include directory (use sparingly!) | `@src/` |
| `@code` | Reference specific function/class | `@calculate_kde` |
| `@docs` | Reference indexed documentation | `@Pandas` |
| `@web` | Web search specific URL | `@https://docs.python.org/...` |
| `@git` | Reference Git commits/diffs | `@diff` |

**Best Practices:**
- ⚠️ Avoid `@folder` abuse—large folders consume context window
- ✅ Always include your constitution/rules file
- ✅ Be specific with symbol references

### 4.3 Six Key Techniques

#### 1. Step-by-Step Description
Break complex tasks into logical chains.

```
❌ BAD: "Do data analysis"
✅ GOOD: "Step 1: Read CSV; Step 2: Calculate statistics; Step 3: Generate plot"
```

#### 2. Provide Examples (Few-shot)
Give concrete input/output samples.

```markdown
**Example:**
Input: {'name': 'Beijing', 'pop': 2154}
Output: 'Beijing population: 21.54 million'
```

#### 3. Role Setting
Specify expert identity to activate domain knowledge.

```
"You are a GIS expert, proficient in GeoPandas spatial indexing and CRS transformations..."
```

#### 4. Explicit Constraints
Set boundary conditions to prevent uncontrolled output.

```
"Use matplotlib only, no seaborn; processing time < 10s; no external API calls"
```

#### 5. Iterative Refinement
Don't aim for perfection in one shot.

```
Round 1: Basic function → Round 2: Error handling → Round 3: Performance → Round 4: Documentation
```

#### 6. AI Self-Review
Leverage AI's reflection capability before running.

```
"Please review the code above for potential memory leaks, edge cases, and logical errors."
```

---

## 5. Project Structure & Workflow

### 5.1 Recommended Project Structure

```
project-root/
├── .cursor/                    # Cursor IDE configurations
│   └── rules/                  # Project-specific rules
│       └── constitution.md     # Core project rules/principles
├── cache/                      # AI context documents
│   ├── model-design.md         # Model design specification
│   ├── tech-stack.md           # Technology stack decisions
│   ├── architecture.md         # Architecture documentation
│   ├── progress.md             # Development progress log
│   └── implementation-plan.md  # Detailed implementation plan
├── src/                        # Source code
│   ├── __init__.py
│   ├── model.py
│   └── agents.py
├── tests/                      # Test files
│   └── test_model.py
├── docs/                       # Documentation
├── pyproject.toml              # Project dependencies
├── Makefile                    # Common commands
└── README.md                   # Project overview
```

### 5.2 Documentation Strategy

**The `cache/` Directory Philosophy:**

This directory serves as the "shared memory" between you and AI agents. Keep these documents:

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `model-design.md` | Core model/algorithm specification | On design changes |
| `tech-stack.md` | Technology choices and rationale | On stack additions |
| `architecture.md` | File structure and responsibilities | After each phase |
| `progress.md` | What was done, for future developers | After each step |
| `implementation-plan.md` | Detailed step-by-step plan | On plan revisions |

**Key Principle:** Keep documents **concise, concise, concise!**

---

## 6. Step-by-Step Implementation Guide

### 6.1 Phase 1: Project Scaffolding

**Step 1:** Create repository from template
```bash
# Use a Python project template
# Example: https://github.com/SongshGeo/Python-Project-Template
git clone <template-repo> my-project
cd my-project
make setup
```

**Step 2:** Initial project planning prompt

```markdown
I will use Python to reproduce the classic NetLogo model ${MODEL_NAME} in this project.

Here is the NetLogo documentation:
${INSERT_NETLOGO_DOCUMENTATION}

Here is the NetLogo code for reference:
${INSERT_NETLOGO_CODE}

Please help me design a concise documentation including:

1. Model Description
2. Implementation Vision
3. Technology Stack
4. User Interface

My initial thoughts are:
${YOUR_INITIAL_THOUGHTS}

Please complete a concise project document in `cache/model-design.md`, explaining the
design vision and framework. Do NOT over-engineer—we will iterate continuously.
Then update `README.md` with the implementation vision and future roadmap.
```

**Step 3:** Manual review
- ✅ Verify generated docs match your vision
- ✅ Delete redundant content
- ✅ Keep it **concise**

**Step 4:** Refine technology stack

```markdown
Here is my model design @cache/model-design.md, and my rough tech stack
@cache/tech-stack.md:1-10. I'm designing the pure Python implementation version.

Please propose the **simplest yet most robust** technology stack and add it
to the tech documentation.
```

### 6.2 Phase 2: Detailed Planning

**Step 1:** Generate implementation plan (Plan Mode)

Feed design + tech docs to AI, generate detailed implementation plan, review, and incorporate into framework.

**Step 2:** Cross-validate with another AI agent

```markdown
Read all documents in @cache, then review
@.cursor/plans/implementation-plan.md

Is this plan 100% clear to you? What questions do you need me to clarify?

... [Your answers] ...
```

**Step 3:** Return to original agent with updates

```markdown
My colleague made some detailed modifications to the plan.
Are there any issues with these changes?

Please review all documents in @cache again.
Is there anything unclear that needs clarification?
```

**Step 4:** Finalize and update `implementation-plan.md`

### 6.3 Phase 3: Iterative Implementation

**Step 1:** Start execution

```markdown
Read all documents in @cache, then execute Step 1 of the implementation plan.

I will be responsible for running tests.
Do NOT proceed until I verify tests pass.
```

**Step 2:** Verify tests
```bash
make test
```

If failed, provide error output to AI:
```markdown
${PASTE_COMMAND_LINE_OUTPUT}

There are failing checks. Please investigate and fix.
```

**Step 3:** Verify pre-commit hooks
```bash
pre-commit run --all-files
```

**Step 4:** Update documentation after passing

```markdown
Your modifications all passed verification.

Please review @cache/ contents again:
1. Open `progress.md` and record what you did for future developers
2. Add new architecture insights to `architecture.md` explaining each file's role
3. If there are new tech stack items, declare them in @cache/tech-stack.md
4. Mark the current step as "completed" in the implementation plan
```

**Step 5:** Code Review (new agent or Review mode)

```markdown
Verify this issue exists and fix it: ...
```

**Step 6:** Commit to Git with standardized message

```bash
git add .
git commit -m "feat(model): implement basic agent behavior"
```

**Step 7:** Repeat for subsequent steps

Create new agent, use similar prompts to continue with next implementation steps.

### 6.4 Phase 4: Review & Documentation

After completing all planned steps:

1. Final code review across all changes
2. Update all documentation in `cache/`
3. Ensure README is current
4. Tag release version if applicable

---

## 7. Debugging Workflow

### The Structured 4-Step Debug Method

**Traditional (Bad):** Throw error at AI → Blind guessing → More chaos

**Structured (Good):**

```
Step 1: Analyze (1 min)
├── List top 3 most likely causes
└── Rank by probability

Step 2: Diagnose (2 min)
├── For each cause, define verification steps
└── (print variables, check specific lines)

Step 3: Design Fix (1 min)
├── Generate multiple fix options (A/B)
├── Compare pros/cons
└── Select option with minimum side effects

Step 4: Implement
└── Apply the chosen fix
```

**Debug Prompt Template:**

```markdown
@debug_report.md  # Reference your error report

1. **Analyze**: Based on this report, list the 3 most likely causes of this error,
   ranked by probability.

2. **Diagnose**: For each possible cause, provide verification steps
   (e.g., print variables, check specific lines).

3. **Fix**: After confirming the cause, design a minimal-change fix and explain
   why you chose it.

⚠️ Note: Do NOT directly rewrite the entire file. Analyze first.
```

**Expected Output:** Logically reasoned analysis, not blind code patches.

---

## 8. Version Control & Experiment Tracking

### Git Workflow (Research-Adapted)

```
main        ← Stable version (paper submission code)
├── dev     ← Daily development branch
└── exp/*   ← Experiment branches (e.g., exp/attention-v1)
```

### AI-Assisted Commit Messages

```markdown
"I modified the attention module and fixed a memory leak.
Please generate a commit message following Conventional Commits format."
```

**Output:**
```
feat(model): add hierarchical attention module
fix(data): resolve data loader memory leak

- Implement HierarchicalAttention class
- Add garbage collection after epoch
```

### Experiment Tracking (Weights & Biases)

Stop relying on Excel for experiment results!

**AI Integration Prompt:**
```markdown
@wandb_init.py

Please add W&B logging code to the training script, automatically recording:
- Hyperparameters (lr, batch_size)
- Training curves (loss, accuracy)
```

**Auto-Tracked Dimensions:**
- Hyperparameters: lr, batch_size, optimizer
- System specs: GPU usage, RAM, Python version
- Metrics: Train/Val Loss, Accuracy, F1
- Artifacts: Best model (.pt), log files

---

## 9. Prompt Templates

### Template 1: Project Initialization

```markdown
# Project: ${PROJECT_NAME}

## Context
I'm building a ${PROJECT_TYPE} that ${MAIN_PURPOSE}.

## Requirements
1. ${REQUIREMENT_1}
2. ${REQUIREMENT_2}
3. ${REQUIREMENT_3}

## Constraints
- Language: Python 3.10+
- Dependencies: ${ALLOWED_DEPS}
- No external API calls
- Processing time < ${TIME_LIMIT}

## Expected Output
- Working code in `src/`
- Tests in `tests/`
- Documentation in `README.md`

Please start by creating the project structure and basic scaffolding.
```

### Template 2: Feature Implementation

```markdown
# Feature: ${FEATURE_NAME}

## Current State
@cache/architecture.md describes the current structure.
@src/model.py contains the main model class.

## Task
Implement ${FEATURE_DESCRIPTION} with the following behavior:
- Input: ${INPUT_SPEC}
- Output: ${OUTPUT_SPEC}
- Edge cases: ${EDGE_CASES}

## Approach
Please:
1. First explain your implementation approach
2. Then implement with tests
3. Update documentation

Do NOT proceed to Step 2 until I approve the approach.
```

### Template 3: Bug Fix Request

```markdown
# Bug Report

## Error Message
```
${PASTE_ERROR_MESSAGE}
```

## Context
- File: ${FILE_PATH}
- Function: ${FUNCTION_NAME}
- Last working state: ${DESCRIPTION}

## Steps to Reproduce
1. ${STEP_1}
2. ${STEP_2}

## Request
1. Analyze the root cause (do NOT fix yet)
2. Propose 2-3 fix options with trade-offs
3. Implement the best option after my approval
```

### Template 4: Code Review Request

```markdown
# Code Review Request

## Files to Review
@src/${FILE_1}
@src/${FILE_2}

## Review Focus
- [ ] Logic correctness
- [ ] Edge case handling
- [ ] Performance implications
- [ ] Code style consistency
- [ ] Documentation completeness

## Questions
1. Are there potential memory leaks?
2. Is the error handling sufficient?
3. Are there any race conditions?

Please provide specific line references for any issues found.
```

### Template 5: Documentation Update

```markdown
# Documentation Update

## Changes Made
${SUMMARY_OF_CHANGES}

## Files Modified
- ${FILE_1}: ${CHANGE_1}
- ${FILE_2}: ${CHANGE_2}

## Request
Please update the following documentation:
1. @cache/progress.md - Add entry for this session
2. @cache/architecture.md - Update if structure changed
3. @README.md - Update if user-facing behavior changed

Keep updates concise and factual.
```

---

## 10. Advanced Skills (2025 Latest)

### 10.1 Rules Files Configuration (.mdc / .cursorrules)

Rules files define project-specific AI behavior and coding standards. They act as "constitution" for your AI assistant.

**File Locations:**
```
project-root/
├── .cursor/
│   └── rules/
│       ├── project.mdc          # Project-wide rules
│       ├── python.mdc           # Python-specific rules
│       └── testing.mdc          # Testing conventions
├── .cursorrules                  # Legacy format (still supported)
└── constitution.md               # Human-readable project principles
```

**Example Rules File (.mdc format):**

```markdown
---
description: Python ABM Project Rules
globs: ["**/*.py"]
alwaysApply: true
---

# Project Rules

## Code Style
- Follow PEP 8 with 88-character line limit (Black formatter)
- Use type hints for all function signatures
- Write Google-style docstrings for all public functions

## Architecture
- All agents inherit from `BaseAgent` class
- Model parameters go in `config.yaml`, not hardcoded
- Use `@dataclass` for configuration objects

## Testing
- Every new function needs a corresponding test
- Use pytest fixtures for common setup
- Aim for >80% coverage on core modules

## Forbidden
- No `print()` statements in production code (use logging)
- No hardcoded file paths
- No `import *`
```

**Key Rules File Attributes:**

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `description` | Human-readable description | "Python coding standards" |
| `globs` | File patterns to apply | `["**/*.py", "**/*.pyx"]` |
| `alwaysApply` | Auto-include in context | `true` / `false` |

### 10.2 Multi-Agent Collaboration Strategy

Leverage multiple AI agents (different models or sessions) for better results.

**The "Dual-Agent" Pattern:**

```
┌──────────────────┐      ┌──────────────────┐
│   ARCHITECT      │      │   IMPLEMENTER    │
│   (Claude/GPT)   │      │   (Different     │
│                  │      │    Model)        │
│ • Design specs   │ ───▶ │ • Write code     │
│ • Review plans   │ ◀─── │ • Run tests      │
│ • Validate logic │      │ • Report issues  │
└──────────────────┘      └──────────────────┘
```

**When to Use Multi-Agent:**
- Complex architectural decisions
- Reducing single-model hallucination
- Cross-validating generated code
- Different models have different strengths

**Collaboration Prompts:**

```markdown
# Agent 1 (Architect) - Claude Opus/Sonnet
"Design the class hierarchy for a multi-agent simulation.
Output only the design, no implementation."

# Agent 2 (Implementer) - GPT/Gemini
"Here is the design from my colleague: [paste design]
Implement this design. Flag any concerns."

# Agent 1 (Review)
"My colleague implemented your design: [paste code]
Review for logical errors and design violations."
```

### 10.3 Background Agents & Async Workflows

Modern AI IDEs support background agents that work while you continue other tasks.

**Use Cases:**
- Running comprehensive code reviews
- Generating test suites
- Refactoring large codebases
- Documentation generation

**Best Practices:**
1. **Scope clearly** - Define exactly what the background agent should do
2. **Set boundaries** - Specify which files can/cannot be modified
3. **Review before merge** - Always review background agent changes
4. **Use for non-critical tasks** - Core algorithm work should be interactive

### 10.4 MCP (Model Context Protocol) Integration

MCP enables AI assistants to interact with external tools and services.

**Common MCP Tools:**

| Tool Category | Examples | Use Case |
|--------------|----------|----------|
| **Git Operations** | GitKraken MCP | Commit, branch, push without leaving chat |
| **Issue Tracking** | GitHub/Jira MCP | Create issues, link PRs |
| **Browser** | Browser MCP | Test web apps, scrape docs |
| **Database** | SQL MCP | Query databases directly |
| **Documentation** | Unblocked MCP | Access team knowledge base |

**Example MCP Workflow:**

```markdown
# Instead of manually switching to terminal
"Use git to create a new branch called 'feature/attention-module',
commit the current changes with message 'feat(model): add attention layer',
and push to origin."

# AI uses MCP tools to execute git commands directly
```

### 10.5 Security Considerations for AI-Generated Code

⚠️ **Critical**: AI-generated code can contain security vulnerabilities. Recent research shows increased risk in areas like:
- SQL injection
- Path traversal
- Insecure deserialization
- Hardcoded credentials

**Security Checklist:**

```markdown
□ Input validation on all user inputs
□ Parameterized queries for database operations
□ No hardcoded secrets (use environment variables)
□ Proper error handling (no stack traces to users)
□ Dependency vulnerability scan (pip-audit, safety)
□ HTTPS for all external communications
```

**Security Review Prompt:**

```markdown
Please perform a security audit on the following code:
@src/api/handlers.py

Check for:
1. Input validation vulnerabilities
2. SQL injection risks
3. Path traversal vulnerabilities
4. Hardcoded secrets or credentials
5. Insecure data handling

For each issue found, provide:
- Severity (Critical/High/Medium/Low)
- Location (file:line)
- Recommended fix
```

### 10.6 Context Window Optimization

Effective context management is crucial for quality AI responses.

**Context Budget Strategy:**

```
Total Context Window: ~128K-200K tokens (varies by model)

Recommended Allocation:
├── 20% - System prompt & rules
├── 30% - Relevant code context
├── 20% - Documentation & specs
├── 20% - Conversation history
└── 10% - Buffer for response
```

**Optimization Techniques:**

1. **Selective Inclusion**
   ```markdown
   # Instead of @src/ (entire directory)
   @src/model.py @src/agents.py  # Only relevant files
   ```

2. **Summary Layers**
   ```markdown
   # Create architecture.md with file summaries
   "Read @cache/architecture.md for project overview,
   then dive into @src/model.py for specific implementation."
   ```

3. **Progressive Disclosure**
   ```markdown
   # Start with overview, then zoom in
   Step 1: "Explain the overall architecture"
   Step 2: "Now focus on the Agent class specifically"
   ```

4. **Context Refresh**
   - Start new sessions for new tasks
   - Re-provide critical context at session start
   - Don't assume AI remembers from compressed history

### 10.7 Agentic Workflow Patterns

Modern AI coding involves "agentic" behaviors where AI takes autonomous actions.

**The OODA Loop for AI Coding:**

```
    ┌─────────────────────────────────────────┐
    │                                         │
    ▼                                         │
┌───────┐    ┌───────┐    ┌────────┐    ┌─────┴─┐
│OBSERVE│───▶│ORIENT │───▶│ DECIDE │───▶│  ACT  │
│       │    │       │    │        │    │       │
│Read   │    │Analyze│    │Plan    │    │Execute│
│code & │    │context│    │approach│    │changes│
│errors │    │& reqs │    │        │    │       │
└───────┘    └───────┘    └────────┘    └───────┘
```

**Agentic Prompt Pattern:**

```markdown
# Give AI clear authority and boundaries
You have permission to:
- Read any file in src/ and tests/
- Modify files in src/utils/
- Create new test files
- Run pytest commands

You must NOT:
- Modify files in src/core/ without explicit approval
- Delete any files
- Change configuration files

Task: Refactor the utility functions in src/utils/ to reduce code duplication.
Proceed step by step, showing me each change before moving to the next.
```

### 10.8 Test-Driven AI Development (TDAD)

Combine TDD principles with AI assistance for higher quality code.

**TDAD Workflow:**

```
1. Write Test First (Human + AI)
   "Write a pytest test for a function that calculates
   pairwise agent distances. Cover edge cases."

2. Verify Test Fails
   Run: pytest tests/test_distances.py -v
   (Should fail - function doesn't exist)

3. AI Implements
   "Now implement the function to make this test pass.
   Minimum code only."

4. Verify Test Passes
   Run: pytest tests/test_distances.py -v

5. Refactor with Safety Net
   "Refactor for readability. Tests must still pass."
```

**Benefits:**
- AI has clear success criteria
- Automatic validation of AI output
- Catches hallucinations immediately
- Documents expected behavior

### 10.9 Prompt Versioning & Experimentation

Treat prompts as code - version them and track what works.

**Prompt Library Structure:**

```
prompts/
├── templates/
│   ├── feature_implementation.md
│   ├── bug_fix.md
│   ├── code_review.md
│   └── refactoring.md
├── experiments/
│   ├── exp_001_chain_of_thought.md
│   └── exp_002_few_shot_examples.md
└── proven/
    ├── debug_workflow_v2.md      # Tested, works well
    └── architecture_review_v3.md
```

**Prompt Experimentation Log:**

```markdown
# prompts/experiments/exp_003_role_playing.md

## Hypothesis
Adding specific expert role improves GIS code quality

## Prompt A (Control)
"Write a function to calculate spatial autocorrelation"

## Prompt B (Treatment)
"You are a GIS expert with 10 years experience in spatial statistics.
Write a function to calculate spatial autocorrelation using Moran's I."

## Results
- Prompt A: Generic implementation, missed edge cases
- Prompt B: Included weight matrix options, proper normalization

## Conclusion
Role-playing improves domain-specific output. Add to proven templates.
```

---

## 11. Best Practices & Tips

### Golden Rules

1. **Always Ask/Plan First**
   - Use "Ask" or "Plan" mode before "Agent" mode
   - Confirm satisfaction before execution

2. **Multi-Model Validation**
   - Use different models to cross-check
   - Reduces hallucination probability

3. **Context is King**
   - Don't assume compressed context maintains quality
   - Re-provide important context when starting new sessions

4. **Iterative > Monolithic**
   - Small, verified steps > Large, unverified changes
   - Each step should be testable independently

5. **Document As You Go**
   - Update docs immediately after each successful step
   - Future you (and AI) will thank present you

### Common Mistakes to Avoid

| Mistake | Why It's Bad | Better Approach |
|---------|--------------|-----------------|
| Dumping entire codebase to AI | Exceeds context, loses focus | Use specific `@file` references |
| Skipping tests | Bugs compound quickly | Test after each step |
| Ignoring AI's questions | Leads to wrong assumptions | Always clarify ambiguities |
| One-shot complex features | High failure rate | Break into 3-5 sub-tasks |
| Not versioning prompts | Can't reproduce results | Save effective prompts |

### Efficiency Multipliers

1. **Keyboard Shortcuts**
   - Learn your IDE's AI shortcuts
   - Common: `Cmd+K` (edit), `Cmd+L` (chat), `Cmd+I` (inline)

2. **Snippet Library**
   - Build a personal prompt template library
   - Reuse proven patterns

3. **Context Presets**
   - Create `.cursor/rules/` files for common contexts
   - Auto-include relevant docs

4. **Parallel Validation**
   - Run tests in background while reviewing code
   - Don't wait sequentially

---

## References

### Official Documentation
- [Cursor Documentation](https://docs.cursor.com/)
- [Claude Documentation](https://docs.anthropic.com/)
- [Mesa ABM Framework](https://mesa.readthedocs.io/)

### Community Resources
- [Awesome Cursor Rules](https://github.com/PatrickJS/awesome-cursorrules)
- [Cursor Best Practices](https://github.com/digitalchild/cursor-best-practices)
- [Vibe Coding Best Practice 2025](https://github.com/2025Emma/vibe-coding-cn)

### Project Templates
- [Python Project Template](https://github.com/SongshGeo/Python-Project-Template)

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────────────┐
│                     VIBE CODING CHEATSHEET                       │
├──────────────────────────────────────────────────────────────────┤
│  MODES                                                           │
│  ├── Ask        → Understand, explore, plan                      │
│  ├── Plan       → Generate detailed implementation plan          │
│  ├── Agent      → Execute with autonomy                          │
│  ├── Review     → Check and validate code                        │
│  └── Background → Async tasks while you work                     │
├──────────────────────────────────────────────────────────────────┤
│  WORKFLOW                                                        │
│  1. Plan → 2. Implement → 3. Test → 4. Document → 5. Repeat      │
├──────────────────────────────────────────────────────────────────┤
│  CONTEXT REFS                                                    │
│  @file.py    → Include file                                      │
│  @folder/    → Include directory (careful!)                      │
│  @function   → Include symbol                                    │
│  @docs       → Include documentation                             │
│  @web        → Web search                                        │
├──────────────────────────────────────────────────────────────────┤
│  DEBUG FLOW                                                      │
│  Analyze → Diagnose → Design Fix → Implement                     │
├──────────────────────────────────────────────────────────────────┤
│  GIT BRANCHES                                                    │
│  main (stable) → dev (daily) → exp/* (experiments)               │
├──────────────────────────────────────────────────────────────────┤
│  ADVANCED 2025                                                   │
│  • Use .mdc rules files for project standards                    │
│  • Multi-agent validation reduces hallucinations                 │
│  • TDAD: Write tests first, then let AI implement                │
│  • Security audit all AI-generated code                          │
│  • Version your effective prompts                                │
└──────────────────────────────────────────────────────────────────┘
```

---

*Last Updated: January 2025*
*Version: 2.0 - Added Advanced Skills Section*
