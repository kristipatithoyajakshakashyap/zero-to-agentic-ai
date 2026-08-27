# Module 04 - Built-in Tools

> **MLCourse - CrewAI Fundamentals - Built-in Tools**

CrewAI ships with a curated set of tools that agents can use to read files, scrape
websites, search the web, and more. This module catalogs the key built-in tools,
shows how to configure them, and demonstrates them inside a crew.

## What you'll learn

- Use FileReadTool to let agents read local files
- Use ScrapeWebsiteTool to fetch and parse web pages
- Use SerperDevTool for web search powered by Serper
- Configure tool parameters and API keys
- Attach multiple tools to a single agent

## Key concepts

- **Tool**: a callable that extends what an agent can do
- **Built-in tools**: pre-built integrations shipped with crewai-tools
- **Tool configuration**: API keys, parameters, and defaults
- **Multi-tool agents**: one agent using several tools simultaneously
- **Tool selection**: agents decide which tool to call based on context

## Contents

1. `01_file_read_tool.ipynb` - FileReadTool setup and usage
2. `02_scrape_website_tool.ipynb` - ScrapeWebsiteTool, URL fetching, parsing
3. `03_serper_search.ipynb` - SerperDevTool, web search, key configuration
4. `04_combining_tools.ipynb` - multiple tools per agent, agent picks the right one

After this module, continue to `05_research_assistant_crew` for the mini-capstone.
