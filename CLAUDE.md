# CLAUDE.md — AI Assistant Guide

This file provides guidance for AI assistants (Claude Code, GitHub Copilot, Gemini, and others) working in this repository.

## Project Overview

This is a **GitHub Skills exercise** that teaches developers how to use the standalone GitHub Copilot CLI to build a Node.js CLI calculator application. It is an interactive, self-paced learning module — not a finished application. The repository starts as a scaffold with no application code; students generate the code through guided steps using the Copilot CLI.

**Primary learning objectives:**
- Install and authenticate the standalone Copilot CLI (`@github/copilot` npm package)
- Use Copilot CLI interactively to generate code from natural language prompts and images
- Create GitHub issues from issue templates using the CLI
- Write and run unit tests with a Node.js testing framework
- Create pull requests, request Copilot reviews, and merge via the CLI

## Repository Structure

```
skills-create-applications-with-the-copilot-cli/
├── .devcontainer/
│   └── devcontainer.json          # Codespace config (Node.js 22 + GitHub CLI)
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── feature_request.md     # Mandatory template for all new feature issues
│   ├── images/                    # Screenshots used in step instructions
│   ├── instructions/
│   │   └── copilot-cli-ref.instructions.md  # Copilot CLI reference (auto-loaded)
│   ├── steps/
│   │   ├── 1-step.md              # Step 1 instructions (install CLI, create issue)
│   │   ├── 2-step.md              # Step 2 instructions (generate calculator code)
│   │   ├── 3-step.md              # Step 3 instructions (extend calculator)
│   │   ├── 4-step.md              # Step 4 instructions (PR, review, merge)
│   │   └── x-review.md            # Copilot review guidance
│   └── workflows/
│       ├── 0-start-exercise.yml   # Triggers on push to main; posts Step 1
│       ├── 1-step.yml             # Triggers on new issue; validates issue format
│       ├── 2-step.yml             # Triggers on push to create-calc-app with src/*.js
│       ├── 3-step.yml             # Triggers on push to create-calc-app with tests
│       └── 4-step.yml             # Triggers on PR close to main; posts completion
├── .vscode/
│   └── settings.json              # Terminal-focused UI; Copilot editor extensions disabled
├── images/
│   ├── js-calculator.png          # Web calculator UI (used as Copilot prompt context)
│   ├── calc-basic-operations.png  # Basic arithmetic examples
│   └── calc-extended-operations.png # Extended operation examples
├── .gitignore                     # Standard Node.js excludes
├── LICENSE
└── README.md                      # Links to the exercise issue
```

**Application code does not exist at repo initialization** — it is created by the learner during the exercise:
- `src/calculator.js` — generated in Step 2
- `src/tests/calculator.test.js` — generated in Step 2 / expanded in Step 3

## Exercise Workflow (4 Steps)

### Step 1 — Install CLI & Create Issue
1. Open a Codespace from the repository
2. Install the Copilot CLI: `npm install -g @github/copilot`
3. Start a session: `copilot --enable-all-github-mcp-tools`
4. Authenticate: `/login`
5. Create a feature request issue using `.github/ISSUE_TEMPLATE/feature_request.md` — the issue title **must contain "Calculator"** and have body content
6. GitHub Actions workflow `1-step.yml` validates the issue and unlocks Step 2

### Step 2 — Generate Calculator Code
1. Start session: `copilot --allow-all --enable-all-github-mcp-tools`
2. Create and push branch `create-calc-app`
3. Use `@images/js-calculator.png` as context to generate `src/calculator.js` with addition, subtraction, multiplication, division
4. Generate `src/tests/calculator.test.js` with edge cases (e.g., division by zero)
5. Commit and push — workflow `2-step.yml` validates `src/calculator.js` contains keywords: `addition`, `subtraction`, `multiplication`, `division`

### Step 3 — Extend Calculator
1. Create a second feature request issue for modulo, power, and square root
2. Add `modulo`, `power`, `squareRoot` functions to `src/calculator.js`
3. Expand tests in `src/tests/calculator.test.js` using `@images/calc-extended-operations.png`
4. Commit and push — workflow `3-step.yml` validates test file existence

### Step 4 — PR, Review & Merge
1. Create a PR from `create-calc-app` to `main` with title containing "Add calculator enhancements"
2. Add `@copilot` as a reviewer
3. Link PR to both issues (use `Closes #N` in description for auto-close)
4. Merge the PR — workflow `4-step.yml` validates completion and posts congratulations

## Key Conventions for AI Assistants

### Instruction sources (auto-loaded by Copilot CLI)
The Copilot CLI automatically reads instructions from:
- `.github/instructions/**/*.instructions.md` ← this repo has `copilot-cli-ref.instructions.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`
- `CLAUDE.md` ← this file
- `GEMINI.md`
- `$HOME/.copilot/copilot-instructions.md`

### Core behavioral rules from `.github/instructions/copilot-cli-ref.instructions.md`
- **Stick to the prompts and context provided** — do not jump ahead to future steps
- **Only add, commit, and push files when explicitly prompted by the user**
- Use `.github/ISSUE_TEMPLATE/feature_request.md` for all new feature requests for `calculator.js`

### Code conventions
- Language: **JavaScript (CommonJS modules)** — use `module.exports` for all exports
- Runtime: **Node.js 22+**
- Source directory: `src/`
- Tests directory: `src/tests/`
- Test file naming: `*.test.js`
- No `package.json` exists at repo start; the student creates it or the test framework initializes it

### Expected `src/calculator.js` exports
```javascript
module.exports = {
  // Basic operations (Step 2)
  add: (a, b) => a + b,
  subtract: (a, b) => a - b,
  multiply: (a, b) => a * b,
  divide: (a, b) => { if (b === 0) throw new Error('Division by zero'); return a / b; },

  // Extended operations (Step 3)
  modulo: (a, b) => a % b,
  power: (base, exponent) => Math.pow(base, exponent),
  squareRoot: (n) => { if (n < 0) return NaN; return Math.sqrt(n); }
};
```

The file **must contain the words** `addition`, `subtraction`, `multiplication`, and `division` as comments or identifiers — the CI workflow checks for these keyphrases verbatim.

### Workflow validation requirements (CI checks)
| Workflow | Branch | Trigger | Validates |
|---|---|---|---|
| `1-step.yml` | any | issue created | Issue title contains "Calculator"; issue has body |
| `2-step.yml` | `create-calc-app` | push to `src/*.js` | `src/calculator.js` contains: addition, subtraction, multiplication, division |
| `3-step.yml` | `create-calc-app` | push to `src/tests/*.js` | Test file exists at `src/tests/calculator.test.js` |
| `4-step.yml` | `main` | PR closed | PR was merged (not just closed) |

### Branch conventions
- Feature work happens on: **`create-calc-app`**
- Main branch: **`main`**
- Do not push application code directly to `main`

## Development Environment

The Codespace uses:
- Base image: Node.js 22 + Debian Bookworm
- GitHub CLI pre-installed (latest)
- VS Code extensions: GitHub Copilot, Copilot Chat
- Simplified VS Code UI: no sidebar, no status bar, no tabs — terminal-first
- Port 3000 exposed for application testing

## Copilot CLI Quick Reference

### Starting a session
```bash
copilot                                        # Basic interactive session
copilot --allow-all                            # Allow all file/tool/URL access
copilot --enable-all-github-mcp-tools         # Enable GitHub MCP tools (issues, PRs, etc.)
copilot --allow-all --enable-all-github-mcp-tools  # Full access (recommended for most steps)
copilot -p "your prompt here"                 # Headless / non-interactive mode
```

### Key slash commands
| Command | Purpose |
|---|---|
| `/login` | Authenticate with GitHub |
| `/session` | Show current session info |
| `/context` | Show token usage visualization |
| `/usage` | Show session statistics and premium request usage |
| `/model [name]` | Switch AI model |
| `/delegate <task>` | Delegate to Copilot Coding Agent (uses premium requests) |
| `/share [file\|gist] [path]` | Save session to markdown file or GitHub gist |
| `/agent` | Browse and select custom agents |
| `/skills` | Manage skills |
| `/compact` | Summarize context to reduce token usage |
| `/clear` | Clear conversation history |
| `/exit` | Exit CLI |

### Global keyboard shortcuts
```
@             Mention files, include contents in context
!             Execute shell command without leaving Copilot (e.g., !git status)
Esc           Cancel current operation
Ctrl+C        Cancel / clear input / exit
Ctrl+D        Shutdown
Ctrl+L        Clear screen
Ctrl+O        Expand/collapse timeline output
Shift+Tab     Toggle plan mode / regular mode
```

### Using images as context
Paste or drag-and-drop images into the terminal, or reference them with `@`:
```
@images/js-calculator.png help me create a calculator based on this image
```

### Headless mode example
```bash
copilot -p "@images/js-calculator.png help me create a Node.js CLI calculator app based only on the four basic math operations in this image. Create the code and put it in the 'src' directory."
```

## Important Notes

- **No application code exists at start** — this is intentional; the entire point is to generate it with Copilot CLI
- **Re-authentication after Codespace restart**: run `copilot --allow-all` and then `/login` or `!gh auth login`
- **`--allow-all` flag**: equivalent to `--allow-all-tools --allow-all-paths --allow-all-urls` — use with caution in production environments
- **`/delegate` uses premium Copilot requests** — regular CLI usage does not
- **Custom agents**: can be created in `.github/agents/` and invoked with `/agent <name>`
- The `.vscode/settings.json` intentionally disables Copilot editor extensions since this exercise is CLI-focused
