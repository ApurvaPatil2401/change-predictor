# Product Requirements Document 

# Change Predictor

> Know what will break before you change your code.

---
**Version:** v0.1

**Status:** Draft

---

# Vision

Software engineers spend hours understanding the impact of code changes before making them. Existing AI coding assistants explain code and generate code, but they rarely answer the most important engineering question:

> **"If I change this, what will happen?"**

Change Predictor aims to answer that question before developers modify their code.

---

# Mission

Build an AI-powered Engineering Decision Engine that predicts the impact of software changes using static analysis, dependency graphs, call graphs, and LLM reasoning.

Instead of helping developers write code, Change Predictor helps them make safer engineering decisions.

---

# Problem Statement

Modern software systems contain thousands of files, complex dependencies, multiple services, and interconnected modules.

Before making even a small change, developers often need to answer questions like:

- What files depend on this?
- Which APIs will be affected?
- Which tests should I run?
- Is this a safe refactor?
- Can I remove this module?
- Will this change break another service?

Today, developers answer these questions manually using:

- Code search
- IDE references
- Documentation
- Team knowledge
- Trial and error

This process is slow, error-prone, and difficult for new contributors.

---

# Proposed Solution

Change Predictor analyzes an entire repository and predicts the engineering consequences of a proposed code change.

Instead of simply explaining existing code, it simulates the potential impact of modifications before they happen.

---

# Target Users

## Primary Users

- Software Engineers
- Backend Developers
- Full Stack Developers
- Open Source Contributors

## Secondary Users

- Engineering Managers
- Tech Leads
- Software Architects
- New Team Members

---

# Core Value Proposition

Before you change your code...

Know what will break.

---

# Design Principles

## Facts Before AI

AI should reason using verified facts generated from static analysis.

It should never hallucinate dependencies.

---

## Prediction Over Explanation

The goal is not explaining code.

The goal is predicting engineering impact.

---

## Evidence Driven

Every prediction must explain why it was made.

Example:

Risk: High

Reason:

- Imported by 14 files
- Used in authentication flow
- Public API
- Referenced in 8 tests

---

## Trust

If confidence is low, the system should say:

"I don't know."

instead of guessing.

---

# User Stories

## Engineering

As a developer,

I want to know what files depend on a module before modifying it.

---

As a developer,

I want to estimate the impact of changing a function signature.

---

As a developer,

I want to know which APIs will be affected.

---

As a developer,

I want to know which tests should be executed.

---

As a developer,

I want to safely rename a class.

---

As a developer,

I want to understand whether a module can be removed safely.

---

As a developer,

I want to estimate refactoring risk before starting work.

---

As a developer,

I want to know if my change affects public APIs.

---

## Onboarding

As a new engineer,

I want to understand the architecture of the repository quickly.

---

As a new engineer,

I want to know the most important files first.

---

## Code Review

As a reviewer,

I want to estimate the risk of a pull request.

---

As a reviewer,

I want to identify high-impact modifications.

---

# Non Goals

Version 1 will NOT include:

- AI code generation
- AI autocomplete
- AI chatbot
- Documentation generation
- PR writing
- Bug fixing
- Deployment automation

The project focuses only on engineering impact prediction.

---

# MVP Features

Version 1 will include:

- Repository parser
- AST generation
- Dependency graph
- Call graph
- File relationship graph
- Impact prediction
- Risk score
- Confidence score
- Human-readable explanation

---

# Future Features

Potential future capabilities include:

- VS Code Extension
- GitHub Integration
- Pull Request Risk Analysis
- CI/CD Integration
- Repository Timeline
- Change Simulation
- Architecture Visualization
- Migration Planner

---

# Success Metrics

A successful prediction should provide:

- Affected files
- Affected modules
- Affected APIs
- Suggested tests
- Risk score
- Confidence score
- Reasoning

within a few seconds.

---

# High-Level Architecture

Repository

↓

Parser

↓

AST Generator

↓

Dependency Graph

↓

Impact Engine

↓

LLM Reasoner

↓

Developer

---

# Competitive Position

Change Predictor does not compete directly with:

- Cursor
- GitHub Copilot
- Sourcegraph
- Semgrep
- OpenRewrite

Instead, it focuses on answering a different question:

> "What are the engineering consequences of this change before I make it?"

---

# Long-Term Vision

Become the engineering decision engine that developers consult before modifying production code.

Instead of asking AI:

"Write this code."

Developers ask:

"If I change this code...

what happens next?"