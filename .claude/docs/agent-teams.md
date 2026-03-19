# Orchestrate Teams of Claude Code Sessions

> Coordinate multiple Claude Code instances working together as a team, with shared tasks, inter-agent messaging, and centralized management.

> **Warning:** Agent teams are experimental and disabled by default. Enable them by adding `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to your settings.json or environment. Agent teams have [known limitations](#limitations) around session resumption, task coordination, and shutdown behavior.

Agent teams let you coordinate multiple Claude Code instances working together. One session acts as the team lead, coordinating work, assigning tasks, and synthesizing results. Teammates work independently, each in its own context window, and communicate directly with each other.

Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead.

> **Note:** Agent teams require Claude Code v2.1.32 or later. Check your version with `claude --version`.

---

## When to Use Agent Teams

Agent teams are most effective for tasks where parallel exploration adds real value:

- **Research and review**: multiple teammates can investigate different aspects of a problem simultaneously, then share and challenge each other's findings
- **New modules or features**: teammates can each own a separate piece without stepping on each other
- **Debugging with competing hypotheses**: teammates test different theories in parallel and converge on the answer faster
- **Cross-layer coordination**: changes that span frontend, backend, and tests, each owned by a different teammate

Agent teams add coordination overhead and use significantly more tokens than a single session. They work best when teammates can operate independently. For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective.

### Compare with Subagents

|                   | Subagents                                        | Agent teams                                         |
| :---------------- | :----------------------------------------------- | :-------------------------------------------------- |
| **Context**       | Own context window; results return to the caller | Own context window; fully independent               |
| **Communication** | Report results back to the main agent only       | Teammates message each other directly               |
| **Coordination**  | Main agent manages all work                      | Shared task list with self-coordination             |
| **Best for**      | Focused tasks where only the result matters      | Complex work requiring discussion and collaboration |
| **Token cost**    | Lower: results summarized back to main context   | Higher: each teammate is a separate Claude instance |

Use subagents when you need quick, focused workers that report back. Use agent teams when teammates need to share findings, challenge each other, and coordinate on their own.

---

## Enable Agent Teams

Agent teams are disabled by default. Enable them by setting the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable to `1`, either in your shell environment or through settings.json:

```json
// .claude/settings.json (project-level)
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## Start Your First Agent Team

After enabling agent teams, tell Claude to create an agent team and describe the task and the team structure you want in natural language. Claude creates the team, spawns teammates, and coordinates work based on your prompt.

Example prompt (works well because the three roles are independent):

```text
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

From there, Claude creates a team with a shared task list, spawns teammates for each perspective, has them explore the problem, synthesizes findings, and attempts to clean up the team when finished.

The lead's terminal lists all teammates and what they're working on. Use **Shift+Down** to cycle through teammates and message them directly. After the last teammate, Shift+Down wraps back to the lead.

---

## Control Your Agent Team

Tell the lead what you want in natural language. It handles team coordination, task assignment, and delegation based on your instructions.

### Choose a Display Mode

Agent teams support two display modes:

- **In-process**: all teammates run inside your main terminal. Use **Shift+Down** to cycle through teammates and type to message them directly. Works in any terminal, no extra setup required.
- **Split panes**: each teammate gets its own pane. You can see everyone's output at once and click into a pane to interact directly. Requires tmux or iTerm2.

> **Note:** `tmux` has known limitations on certain operating systems and traditionally works best on macOS. Using `tmux -CC` in iTerm2 is the suggested entrypoint into `tmux`.

The default is `"auto"`, which uses split panes if you're already running inside a tmux session, and in-process otherwise. To override, set `teammateMode` in settings.json:

```json
{
  "teammateMode": "in-process"
}
```

To force in-process mode for a single session, pass it as a flag:

```bash
claude --teammate-mode in-process
```

### Specify Teammates and Models

Claude decides the number of teammates to spawn based on your task, or you can specify exactly what you want:

```text
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

### Require Plan Approval for Teammates

For complex or risky tasks, you can require teammates to plan before implementing:

```text
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

When a teammate finishes planning, it sends a plan approval request to the lead. The lead reviews and either approves or rejects with feedback. Once approved, the teammate exits plan mode and begins implementation.

### Talk to Teammates Directly

Each teammate is a full, independent Claude Code session. You can message any teammate directly.

- **In-process mode**: use **Shift+Down** to cycle through teammates, then type. Press **Enter** to view a teammate's session, then **Escape** to interrupt their current turn. Press **Ctrl+T** to toggle the task list.
- **Split-pane mode**: click into a teammate's pane to interact with their session directly.

### Assign and Claim Tasks

The shared task list coordinates work across the team. Tasks have three states: **pending**, **in progress**, and **completed**. Tasks can also depend on other tasks.

- **Lead assigns**: tell the lead which task to give to which teammate
- **Self-claim**: after finishing a task, a teammate picks up the next unassigned, unblocked task on its own

Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously.

### Shut Down Teammates

To gracefully end a teammate's session:

```text
Ask the researcher teammate to shut down
```

### Clean Up the Team

When you're done, ask the lead to clean up:

```text
Clean up the team
```

> **Warning:** Always use the lead to clean up. Teammates should not run cleanup because their team context may not resolve correctly, potentially leaving resources in an inconsistent state.

### Enforce Quality Gates with Hooks

Use hooks to enforce rules when teammates finish work or tasks complete:

- **`TeammateIdle`**: runs when a teammate is about to go idle. Exit with code 2 to send feedback and keep the teammate working.
- **`TaskCompleted`**: runs when a task is being marked complete. Exit with code 2 to prevent completion and send feedback.

---

## How Agent Teams Work

### Architecture

An agent team consists of:

| Component     | Role                                                                                       |
| :------------ | :----------------------------------------------------------------------------------------- |
| **Team lead** | The main Claude Code session that creates the team, spawns teammates, and coordinates work |
| **Teammates** | Separate Claude Code instances that each work on assigned tasks                            |
| **Task list** | Shared list of work items that teammates claim and complete                                |
| **Mailbox**   | Messaging system for communication between agents                                          |

Teams and tasks are stored locally:

- **Team config**: `~/.claude/teams/{team-name}/config.json`
- **Task list**: `~/.claude/tasks/{team-name}/`

### Permissions

Teammates start with the lead's permission settings. If the lead runs with `--dangerously-skip-permissions`, all teammates do too. After spawning, you can change individual teammate modes.

### Context and Communication

Each teammate has its own context window. When spawned, a teammate loads the same project context as a regular session: CLAUDE.md, MCP servers, and skills. It also receives the spawn prompt from the lead. The lead's conversation history does not carry over.

**How teammates share information:**

- **Automatic message delivery**: messages are delivered automatically to recipients
- **Idle notifications**: teammates automatically notify the lead when finished
- **Shared task list**: all agents can see task status and claim available work

**Teammate messaging:**

- **message**: send a message to one specific teammate
- **broadcast**: send to all teammates simultaneously (use sparingly, costs scale with team size)

### Token Usage

Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales with the number of active teammates. For research, review, and new feature work, the extra tokens are usually worthwhile. For routine tasks, a single session is more cost-effective.

---

## Use Case Examples

### Run a Parallel Code Review

```text
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

### Investigate with Competing Hypotheses

```text
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

---

## Best Practices

### Give Teammates Enough Context

Include task-specific details in the spawn prompt:

```text
Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."
```

### Choose an Appropriate Team Size

- **Token costs scale linearly**: each teammate consumes tokens independently
- **Coordination overhead increases**: more teammates = more communication
- **Diminishing returns**: beyond a certain point, additional teammates don't speed up work proportionally

**Start with 3-5 teammates** for most workflows. Having 5-6 tasks per teammate keeps everyone productive.

### Size Tasks Appropriately

- **Too small**: coordination overhead exceeds the benefit
- **Too large**: teammates work too long without check-ins
- **Just right**: self-contained units that produce a clear deliverable (a function, a test file, a review)

### Wait for Teammates to Finish

If the lead starts implementing tasks itself:

```text
Wait for your teammates to complete their tasks before proceeding
```

### Avoid File Conflicts

Two teammates editing the same file leads to overwrites. Break the work so each teammate owns a different set of files.

### Monitor and Steer

Check in on teammates' progress, redirect approaches that aren't working, and synthesize findings as they come in.

---

## Troubleshooting

### Teammates Not Appearing

- In in-process mode, press **Shift+Down** to cycle through active teammates
- Check that the task was complex enough to warrant a team
- For split panes, ensure tmux is installed: `which tmux`

### Too Many Permission Prompts

Pre-approve common operations in your permission settings before spawning teammates.

### Teammates Stopping on Errors

Check their output using Shift+Down, then give additional instructions or spawn a replacement.

### Lead Shuts Down Before Work Is Done

Tell it to keep going, or tell the lead to wait for teammates to finish before proceeding.

### Orphaned tmux Sessions

```bash
tmux ls
tmux kill-session -t <session-name>
```

---

## Limitations

- **No session resumption with in-process teammates**: `/resume` and `/rewind` do not restore in-process teammates
- **Task status can lag**: teammates sometimes fail to mark tasks as completed
- **Shutdown can be slow**: teammates finish their current request before shutting down
- **One team per session**: clean up the current team before starting a new one
- **No nested teams**: only the lead can manage the team
- **Lead is fixed**: you can't promote a teammate to lead
- **Permissions set at spawn**: all teammates start with the lead's permission mode
- **Split panes require tmux or iTerm2**: not supported in VS Code's integrated terminal, Windows Terminal, or Ghostty

> **Tip:** `CLAUDE.md` works normally — teammates read CLAUDE.md files from their working directory. Use this to provide project-specific guidance to all teammates.
