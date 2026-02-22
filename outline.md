# AI Agents Tutorial

**Vibe:** 3 friends around a table, ~2 hours, casual
**Audience:** Non-technical knowledge workers
**Goal:** Build intuition for what agents are, then experience it firsthand

---

## Part 1: The Story (~40 min)

### 1A: Quick History (~3 min)

Just set the timeline so everyone's oriented:

- **2020-2021:** LLMs exist but only devs use them through APIs. Copilot launches as fancy autocomplete.
- **Nov 2022:** ChatGPT drops. Suddenly everyone can talk to AI. But it's still a chat window — ask, get answer, copy-paste.
- **2023-2024:** Tons of tools show up — Cursor, Devin, image generators, reasoning models. Things move fast.
- **2025-now:** The shift to agents. AI goes from answering questions to actually *doing things*. Karpathy coins "vibe coding." Claude Code launches.

---

### 1B: What Is an Agent? (~7 min)

Simon Willison nailed the definition:

> "An agent is an LLM that runs tools in a loop to achieve a goal."

Three things make something an agent:

1. **Tools** — it can *do* things (read files, run code, call APIs), not just generate text
2. **A loop** — it tries something, sees what happened, decides what to do next, keeps going
3. **A goal** — it's working toward an outcome, not just responding to your last message

The restaurant version of this:

- **Chatbot** = vending machine. Push button, get item.
- **Assistant** = waiter. You say what you want, they relay it.
- **Agent** = personal chef. You say "I'm in the mood for something Italian" and they check what's in the fridge, pick a recipe, cook it, taste it, adjust, serve it. If they're missing an ingredient they figure it out without bugging you.

Simple test: can you give it a task and walk away? If you have to sit there guiding every step, it's not an agent. If you can say "handle this" and come back to find it done (or find it asking you one specific question because it got stuck), that's an agent.

---

### 1C: The Autonomy Slider (~10 min)

This is a Karpathy concept from his [Latent Space interview](https://www.latent.space/p/s3) and it's the best way to make sense of all the different tools out there.

The idea: it's not "AI on/off." It's a slider from full human control to full AI autonomy. Think Tesla Autopilot — they didn't ship self-driving as a toggle. They shipped lane-keeping first, then adaptive cruise, then lane changes. You build trust gradually.

Here's where the products sit:

| Level | What it does | Example | Analogy |
|---|---|---|---|
| **1 — Suggestion** | Predicts your next action, you accept/reject | Copilot autocomplete, spell check | GPS suggesting a turn |
| **2 — Conversation** | You describe what you want, it generates it, you paste it in | ChatGPT, Claude chat | Calling a friend for advice |
| **3 — Integrated partner** | Edits your work directly, you review each change | Cursor, Microsoft 365 Copilot | Coworker making tracked changes in your doc |
| **4 — Supervised agent** | Plans and executes multi-step work, checks in at key moments | Claude Code, Cline | New hire who checks in before big decisions |
| **5 — Autonomous agent** | Works independently, comes back with results | Devin, Codex, background agents | Senior employee you delegate to |
| **6 — Proactive agent** | Notices things to do and acts without being asked | Scheduled agents, monitoring agents | Chief of staff who anticipates your needs |

What changes as you move up:

- **Autonomy:** How much can it do without asking?
- **Scope:** One action vs. multi-step workflow vs. ongoing responsibility?
- **Initiative:** Does it wait for you or notice things on its own?
- **Environment:** Chat window → your editor → your terminal → your whole computer → the internet?

Walk through the jumps — each one is a different "aha":

- **Suggestion → Conversation:** "Instead of guessing what I'll type, I can just describe what I want." This is when non-technical people got access.
- **Conversation → Integrated partner:** "Instead of copy-pasting from a chat window, the AI edits my actual files." The context barrier disappears.
- **Integrated partner → Supervised agent:** "Instead of approving each line, I describe the goal and it figures out the steps." The AI starts *planning*. This is the big jump.
- **Supervised → Autonomous:** "I kick off a task and close my laptop. It keeps working."
- **Autonomous → Proactive:** "I didn't ask it to do anything. It noticed something needed doing and did it." This one tends to blow people's minds.

Worth noting: we're not at full autonomy yet, and that's fine. The most useful products right now are partial autonomy — you stay in the loop. Karpathy's line: *"Demo is `works.any()`, product is `works.all()`"* — a demo just needs to work sometimes to impress, a product needs to work reliably. The slider lets you ratchet up trust over time.

---

### 1D: Why Does AI Start with Code? (~8 min)

This matters because otherwise it sounds like a programmer thing. It's not.

Five reasons code was the natural starting point:

1. **Training data:** All of GitHub, Stack Overflow, every tutorial ever — massive, high-quality, machine-readable.
2. **Verifiability:** Code runs or it doesn't. Tests pass or fail. The AI gets instant, objective feedback. Compare: "is this marketing copy good?" requires human judgment. Code has `assert`.
3. **Fast feedback loops:** Write → run → error → fix → run, in seconds. Most business domains have feedback loops measured in days.
4. **Digital-native:** No physical world needed. Just reading and writing files.
5. **Structured output:** Programming languages have grammars. The output space is constrained. Easier for AI than open-ended prose.

But here's the thing — most knowledge work is already software. You just don't think of it that way:

- Spreadsheets are programming (VLOOKUP is a function, pivot tables are data pipelines)
- Documents are structured data
- Business workflows are pipelines
- Most of your job is reading, thinking about, and producing digital files

The techniques AI learned on code — plan, execute, verify, iterate — transfer directly. The agent loop doesn't care if it's editing Python or analyzing a spreadsheet. Same pattern: read the input, figure out what to do, do it, check the result, iterate.

This is literally what happened with Claude Cowork (launched Jan 2026) — same agent architecture as Claude Code but for Excel files, PDFs, PowerPoints. Anthropic built it because people were already using Claude Code for non-coding tasks.

Karpathy's framing ties it together:

- **Software 1.0:** You write code
- **Software 2.0:** You train neural networks on data
- **Software 3.0:** You describe what you want in English

If English is the programming language, the line between "coding" and "knowledge work" disappears.

---

### 1E: Quick Live Demo (~5 min)

Before the exercise, do something fast and visual so they see the pattern:

1. Open a terminal, `cd` to an empty folder
2. Ask Claude Code: *"Create a beautiful HTML page that shows a dashboard with 3 charts showing fake quarterly sales data, with a dark theme"*
3. Watch it write the file (~30 seconds)
4. Open in browser

Point out what just happened in agent terms: it read the goal, planned the approach, wrote code, created a file — tools in a loop toward a goal. Same three properties from 1B.

---

### 1F: Where This Is Going (~5 min)

Quick forward look to close Part 1:

- We're early. The tools are rough and the patterns are still being figured out.
- But the trajectory is clear and things are moving fast.
- Getting comfortable with this now is like learning to use a spreadsheet in 1985 — the specific tool doesn't matter as much as the intuition you build.

---

## Part 2: The Exercise (~60 min)

### Setup (~5 min)

Show the setup slide. Everyone should have done this beforehand, but help anyone who didn't.

1. Claude account (Pro/Max sub or console.anthropic.com with $5 credits)
2. Claude Code installed — [code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup)
3. Clone the repo and cd into it:
   - `git clone https://github.com/tangdrew/claude-code-workshop.git`
   - `cd claude-code-workshop`
4. Run `claude` and make sure it responds

### The Task: Sales Data Analysis (~50 min)

A non-coding business task done through an agent. This is the "everything is software" point from Part 1 made real.

**The dataset:** CSV with ~600 rows of simulated quarterly sales data (regions, products, reps, revenue, dates). There are stories baked into the data — they don't need to know that, but it means their questions will get satisfying answers.

**Phase 1: Exploration (~10 min)**

Have them ask Claude Code to:
- "Read the sales data file and tell me what's in it"
- "Are there any data quality issues?"
- "Give me basic summary stats"

Thing to point out: you told it *what you wanted to know*, not *how to figure it out*. It decided on its own to write code, inspect the data, and report back.

**Phase 2: Analysis (~15 min)**

Prompts to try — roughly ordered from simple to more interesting:

Basic:
- "Which region has the highest total revenue?"
- "Who are the top 5 salespeople?"
- "Which product line sells the most?"

Comparisons:
- "Which product is growing fastest quarter over quarter?"
- "How does average deal size vary by region?"
- "Are there reps who crush it in one product but not others?"

Time and trends:
- "Is there a seasonal pattern?"
- "Are there any quarters where something weird happened — a big spike or dip?"
- "Is any rep's performance trending downward over time?"

Deeper:
- "How concentrated is our revenue — are we dependent on a few big deals or is it spread out?"
- "Are there any reps who only sell one product line? Is that specialization working for them?"
- "Is there a rep who started recently and is ramping up fast?"
- "Are units and revenue tightly correlated or is pricing all over the place?"

Strategic:
- "If we had to cut one product line, which would hurt least?"
- "Which rep would you clone if you could?"
- "What would Q1 2026 look like if current trends continue?"

Thing to point out: watch it write code, run it, sometimes hit an error, fix the error, try again. That's the loop — core agent behavior.

**Phase 3: Visualization (~10 min)**

- "Create a chart showing revenue by region over time"
- "Make a presentation-ready summary with the top 3 insights"
- Let them iterate: "change the colors" / "add a trend line" / etc.

Thing to point out: this is Level 4 on the slider. It's doing multi-step work but you're steering.

**Phase 4: Go Wild (~15 min)**

Let them loose. Ideas:
- Bring something from their own work (a spreadsheet, a document)
- "Write a memo summarizing these findings for my boss"
- "What would you recommend we do based on this data?"

If someone's agent gets stuck in a loop, that's a great teaching moment — "this is why we're at Level 4 and not Level 5 yet."

**What they'll find (cheat sheet for you):**

| Story | What's in the data |
|---|---|
| Jake Chen Q3 2025 spike | 23 deals avg $25.5k vs his usual ~$14.7k. Mostly big Enterprise deals. Makes West break the seasonal pattern. |
| Samantha Reed declining | Numbers trend down over the 2 years |
| Emily Nguyen is new | No data before Q3 2024, ramps from $21k to $81k/quarter |
| Aisha Patel is a specialist | 49 of 54 deals are Starter product |
| Q4 seasonal spike | Both years, Q4 has the most deals and highest revenue |
| Midwest underperforms | Lowest total revenue of any region |
| Southeast is growing | Highest total, upward trend |
| Maria Lopez is the star | $1.2M total, top rep by a margin |
| Dirty data | 8 rows "Jonh Martinez", 4 missing revenues, 1 duplicate row |

### Debrief (~5 min)

Quick round-the-table:
- What surprised you?
- What worked better than expected? What didn't?
- Did that feel like "programming"?

---

## Part 3: Wrap-Up (~15 min)

### Discussion

1. **"What in your work is secretly software?"** — What tasks are really just "read files, think, produce files"? Those are agent-ready.

2. **"Where on the slider would you want AI for your work?"** — Not everything needs Level 5. Some things you want to stay hands-on with. The point isn't max autonomy, it's the right level for each task.

3. **"What would you try next?"** — Something concrete they can do tomorrow.

### Resources

- Claude Code: install instructions, docs
- Things to look up: "AI agents," "agentic workflows," "vibe coding"

### Closing Thought

The tools will keep changing. The actual skill is learning to collaborate with AI — how to describe what you want, evaluate what you get back, and iterate. That transfers across everything.
