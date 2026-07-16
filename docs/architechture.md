# Architecture

# Change Predictor

> Know what will break before you change your code.

---

# Version

v0.1

---

# Overview

Change Predictor is an engineering decision engine that predicts the impact of software changes before developers modify their code.

Unlike traditional AI coding assistants, Change Predictor combines deterministic program analysis with AI reasoning.

The system is built around one principle:

> Facts first. AI second.

Static analysis generates facts.

LLMs explain those facts.

---

# High Level Architecture

                    Repository
                         │
                         ▼
               Language Detection
                         │
                         ▼
                 Repository Parser
                         │
                         ▼
                  AST Generation
                         │
                         ▼
                Dependency Builder
                         │
                         ▼
                  Knowledge Graph
                         │
                         ▼
                  Impact Analyzer
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
     Risk Engine                  LLM Reasoner
          │                             │
          └──────────────┬──────────────┘
                         ▼
                   CLI / VS Code

---

# Core Components

## 1. Repository Parser

Purpose

Read and understand the repository structure.

Responsibilities

- Scan files
- Detect supported language
- Ignore vendor/build folders
- Build project inventory

Output

Repository Model

---

## 2. AST Generator

Purpose

Convert source files into Abstract Syntax Trees.

Responsibilities

- Parse syntax
- Extract functions
- Extract classes
- Extract imports
- Extract exports

Output

AST for every source file.

---

## 3. Dependency Builder

Purpose

Understand relationships between components.

Relationships include

- Imports
- Function calls
- Class inheritance
- Interface implementation
- Module dependencies

Output

Dependency Graph

---

## 4. Knowledge Graph

Purpose

Store repository relationships in graph form.

Nodes

- Files
- Functions
- Classes
- Modules
- APIs

Edges

- Imports
- Calls
- Defines
- Uses
- Extends

This graph becomes the foundation of impact prediction.

---

## 5. Impact Analyzer

Purpose

Predict consequences of a code change.

Example

Developer asks

"What happens if I modify auth.py?"

Analyzer identifies

- impacted files
- downstream dependencies
- affected APIs
- affected modules

---

## 6. Risk Engine

Purpose

Estimate engineering risk.

Example output

Risk

High

Confidence

92%

Reason

- Public API
- Imported by 21 files
- Authentication module
- Used in middleware

---

## 7. LLM Reasoner

Purpose

Explain analysis results in natural language.

Important

The LLM does NOT discover dependencies.

It explains deterministic results.

Example

Instead of

Risk = High

The LLM says

"This module is used by multiple authentication flows and changing it may require updates to middleware and session handling."

---

# Data Flow

Repository

↓

Parser

↓

AST

↓

Dependency Graph

↓

Knowledge Graph

↓

Impact Analysis

↓

Risk Score

↓

LLM Explanation

↓

Developer

---

# Design Principles

## Facts Before AI

Never ask the LLM to discover dependencies.

Use deterministic analysis first.

---

## Modular

Every component should be replaceable.

Parser

↓

Graph

↓

Analyzer

↓

LLM

should be independent modules.

---

## Language Independent

Architecture should support multiple languages.

Each language gets its own parser.

---

## Explain Every Prediction

Every prediction should include evidence.

Never output

"High Risk"

Instead output

High Risk

Reason

- Used by 18 files

- Public API

- Called by LoginService

---

# Supported Languages (MVP)

Version 1

Python

Future

TypeScript

JavaScript

Java

Go

Rust

---

# Non Goals

Version 1 will NOT include

- Code generation
- AI autocomplete
- Bug fixing
- PR review
- Documentation generation
- Runtime execution
- Automatic refactoring

---

# Future Architecture

Repository

↓

Repository Graph

↓

Change Simulator

↓

Impact Prediction

↓

Migration Planner

↓

Risk Timeline

↓

IDE Integration

---

# Technology (Tentative)

Language

Python

Parser

Tree-sitter

Knowledge Graph

NetworkX (initially)

LLM

Model agnostic

Frontend

CLI

Future

VS Code Extension

---

# Architecture Summary

The architecture separates deterministic program analysis from AI reasoning.

Static analysis provides reliable facts.

Graph analysis predicts impact.

The LLM explains the results.

This separation makes Change Predictor trustworthy, extensible, and language independent.