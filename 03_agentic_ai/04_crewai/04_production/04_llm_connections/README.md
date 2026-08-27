# Module 04 - LLM Connections

> **MLCourse - Production Readiness - LLM Connections**

CrewAI uses LiteLLM under the hood to connect to dozens of LLM providers. This
module covers configuring Ollama, Groq, OpenAI, and other providers, plus model
selection strategies for different agent roles.

## What you'll learn

- Configure Ollama for local-first agent execution
- Connect to Groq for fast cloud inference
- Use OpenAI models when needed
- Select different models for different agent roles
- Manage API keys and provider switching

## Key concepts

- **LiteLLM**: the universal LLM adapter powering CrewAI's provider support
- **Provider configuration**: setting up each provider with correct credentials
- **Model selection**: choosing the right model for each agent's role
- **Local-first**: using Ollama for privacy and cost-free experimentation
- **Provider switching**: changing models with a single configuration change

## Contents

1. `01_ollama_setup.ipynb` - local Ollama, model pulling, configuration
2. `02_groq_setup.ipynb` - Groq cloud, free tier, speed optimization
3. `03_provider_switching.ipynb` - LiteLLM, model per agent, swap pattern

After this module, continue to `05_capstone_full_stack_app_builder` for the capstone.
