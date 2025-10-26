ARCHITECTURE.md — ClimateCircle System Design

System Overview
ClimateCircle is a three-stage AI research system for climate anxiety that processes qualitative data through mechanistic reasoning, memory, and therapeutic evolution.

text
┌─────────────────────────────────────────────────────────────────┐
│                    CLIMATECIRCLE ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────────┘

INPUT LAYER: Listen Labs
├─ Recruits 50+ climate-anxious youth (18-35)
├─ Conducts AI-moderated voice interviews (30 min each)
├─ Produces transcripts + audio
└─ Output: Raw qualitative data (50-75 interviews)

         ↓ STAGE 1: CAUSAL ANALYSIS

GROQ LAYER: Mechanistic Reasoning
├─ Engine: causal_reasoning_engine.py
├─ Model: Mixtral 8x7b-32768 (ultra-fast)
├─ Process:
│  ├─ Step 1: Extract cause-effect pairs
│  ├─ Step 2: Generate implicit causal chains
│  ├─ Step 3: Evaluate confidence scores
│  └─ Step 4: Identify intervention ROI points
└─ Output: Structured causal graphs + intervention recommendations

         ↓ STAGE 2: MEMORY & LEARNING

LETTA LAYER: Self-Editing Agent Memory
├─ Engine: letta_trauma_agent.py
├─ Model: Letta agent with 4 memory blocks
├─ Process:
│  ├─ Initialize: Create per-participant memory
│  ├─ Session 1: Store trauma timeline + coping inventory
│  ├─ Session 2+: Agent self-edits memory (tool-calling)
│  └─ Progress: Generate journey summary
└─ Output: Evolved participant memory + therapeutic insights

         ↓ STAGE 3: PROTOCOL EVOLUTION

CLAUDE LAYER: Persistent Therapeutic Protocol
├─ Engine: claude_persistent_protocol.py
├─ Model: Claude 3.5 Sonnet with extended thinking
├─ Process:
│  ├─ Read: All persistent memory files
│  ├─ Respond: Generate personalized therapeutic response
│  ├─ Update: Autonomously curate what to remember
│  └─ Evolve: Modify therapeutic approach based on effectiveness
└─ Output: Evolved protocol + therapeutic narrative

OUTPUT LAYER: Base44 Dashboard
├─ Beautiful glassmorphic UI
├─ Displays: Causal chains + memory evolution + protocol adaptation
├─ Shows: Real-time research insights
└─ Enables: Launch support groups based on findings
Component Relationships
Data Flow Between Stages
text
STAGE 1: Groq Causal Analysis
├─ Input: Raw transcript
├─ Processing:
│  ├─ LLM identifies cause-effect pairs
│  ├─ Iteratively builds causal chains
│  ├─ Scores confidence per link
│  └─ Calculates intervention ROI
├─ Output: JSON
│  └─ {
│      "causal_pairs": [{"cause": "X", "effect": "Y", "explicit": true}],
│      "chains": ["climate news → anxiety → insomnia → work issues"],
│      "confidence": {"chain_1": {"overall": 0.86, "links": [...]}},
│      "interventions": [{"link": "anxiety→insomnia", "roi": 0.92}]
│    }
└─ Passed to: Letta (context for memory)

STAGE 2: Letta Memory Tracking
├─ Input: Groq causal analysis + new session transcript
├─ Processing:
│  ├─ Read: Existing participant memory (if session 2+)
│  ├─ Listen: Extract new information from transcript
│  ├─ Edit: Tool-call memory_replace to update understanding
│  ├─ Learn: Identify what coping strategies work
│  └─ Store: Archival record (searchable)
├─ Output: JSON
│  └─ {
│      "memory_updates": ["Updated trauma_timeline", "Added coping strategy"],
│      "session_analysis": "Breakthrough moment: User joined action group",
│      "progress_metrics": {"mood_improvement": 0.34, "engagement_increase": 0.72},
│      "next_steps": ["Deepen climate action involvement"]
│    }
└─ Passed to: Claude (participant journey for therapeutic adaptation)

STAGE 3: Claude Protocol Evolution
├─ Input: Letta memory + session transcript
├─ Processing:
│  ├─ Read: Persistent memory files (assessment.md, sessions.md, etc.)
│  ├─ Reason: Extended thinking (2000 tokens) about therapeutic approach
│  ├─ Respond: Generate personalized therapeutic response
│  ├─ Update: Autonomously decide what to remember
│  └─ Evolve: Modify protocol version if approach changed
├─ Output: JSON + Updated memory files
│  └─ {
│      "therapeutic_response": "I noticed you shifted from feeling hopeless...",
│      "memory_updates": {
│        "sessions.md": "Session 3: User now leading meetings",
│        "protocol_evolution.md": "Approach evolved: From crisis management to purpose-building"
│      },
│      "protocol_evolved": true,
│      "new_protocol_version": 3
│    }
└─ Passed to: Base44 Dashboard (visualization)
System Interactions
How Groq and Letta Talk
text
Groq's Output → Letta's Context

GROQ ANALYSIS:
{
  "causal_chains": [
    "climate news → anxiety → insomnia → work issues → social withdrawal"
  ],
  "interventions": [
    {
      "link": "anxiety → insomnia",
      "confidence": 0.95,
      "modifiability": "high",
      "suggested_interventions": ["CBT for sleep", "meditation", "peer support"]
    }
  ]
}

↓ Letta reads this and adds to memory:

LETTA MEMORY UPDATE:
{
  "trauma_timeline": "User identifies: climate news triggers cascade of anxiety",
  "coping_inventory": "Identified intervention points: anxiety mgmt, sleep hygiene, peer support",
  "support_gaps": "User has no coping strategies yet; all suggestions are novel"
}
How Letta and Claude Talk
text
Letta's Memory → Claude's Protocol Decisions

LETTA ARCHIVE (Session 1):
- Participant tried breathing exercises → helped
- Participant joined action group → breakthrough moment
- Mood shift: hopelessness → agency

CLAUDE'S PROTOCOL UPDATE:
{
  "previous_protocol": "General CBT approach",
  "new_protocol": "Action-oriented + community-based",
  "reasoning": "Data shows behavioral activation (group action) more effective than cognitive work alone",
  "next_recommendations": ["Deepen action group involvement", "Leadership opportunities"]
}
How Claude Reads Its Own Memory
text
PERSISTENT MEMORY FILES (File System)

assessment.md
├─ 22yo college student
├─ Climate anxiety onset: 1 year ago
├─ Current: Severe insomnia, work impact
└─ Initial impression: Trauma response

sessions.md
├─ Session 1: Presented hopelessness, no coping skills
├─ Session 2: Tried breathing → worked; joined action group
└─ Session 3: Now leading group meetings

therapeutic_goals.md
├─ Initial goal: "Reduce anxiety to manageable levels"
├─ Evolved goal: "Channel anxiety into climate action"
└─ Current goal: "Develop leadership skills in activism"

protocol_evolution.md
├─ Version 1: Generic CBT (didn't resonate)
├─ Version 2: Added behavioral activation → breakthrough
├─ Version 3: Emphasize action-oriented, community-based (current)

Claude reads ALL these files before Session 4, personalizes response based on evolution.
Information Flow Diagram
text
┌──────────────────┐
│ Listen Labs API  │
│ (50+ interviews) │
└────────┬─────────┘
         │ Raw Transcripts
         ▼
    ┌────────────────────────────────┐
    │  Parse & Validate             │
    │  (Check for quality)           │
    └────────┬─────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │ GROQ CAUSAL REASONING ENGINE           │
    ├─────────────────────────────────────────┤
    │ 4-Step Process:                        │
    │ 1. Extract cause-effect pairs          │
    │ 2. Generate causal chains              │
    │ 3. Evaluate confidence scores          │
    │ 4. Identify intervention ROI           │
    │                                        │
    │ Output: Causal JSON                    │
    └────────┬──────────────────────────────┘
             │ Causal Analysis (JSON)
             ▼
    ┌─────────────────────────────────────────┐
    │ LETTA TRAUMA AGENT                     │
    ├─────────────────────────────────────────┤
    │ Reads: Existing participant memory      │
    │ Processes: New session transcript       │
    │ Tool-calls: memory_replace (self-edit)  │
    │ Searches: Archival memory (progress)    │
    │                                        │
    │ Output: Memory JSON + Updates           │
    └────────┬──────────────────────────────┘
             │ Memory + Session Analysis
             ▼
    ┌─────────────────────────────────────────┐
    │ CLAUDE PERSISTENT PROTOCOL             │
    ├─────────────────────────────────────────┤
    │ Reads: All persistent memory files      │
    │ Thinks: Extended thinking (deep reason)│
    │ Responds: Therapeutic message           │
    │ Updates: Autonomously curates memory    │
    │                                        │
    │ Output: Protocol JSON + Memory Files    │
    └────────┬──────────────────────────────┘
             │ Therapeutic Response + Protocol
             ▼
    ┌─────────────────────────────────────────┐
    │ BASE44 DASHBOARD                       │
    ├─────────────────────────────────────────┤
    │ Visualizes:                            │
    │ • Causal chains (Groq)                 │
    │ • Memory evolution (Letta)             │
    │ • Protocol adaptation (Claude)         │
    │                                        │
    │ Outputs: Beautiful UI + Insights       │
    └─────────────────────────────────────────┘
Real Example: Complete Flow
text
INPUT: Raw transcript from Listen Labs interview
───────────────────────────────────────────────

PARTICIPANT: "I've been really anxious about climate. Every time I see 
news about wildfires, I get this knot in my stomach. Can't sleep. 
Can't focus at work. Feel hopeless."

STAGE 1: GROQ ANALYSIS
───────────────────────────────────────────────
Process:
├─ Extract pairs: [
│   {"cause": "climate news", "effect": "anxiety"},
│   {"cause": "anxiety", "effect": "insomnia"},
│   {"cause": "insomnia", "effect": "work issues"},
│   {"cause": "work issues", "effect": "hopelessness"}
│ ]
├─ Build chains: ["climate news → anxiety → insomnia → work issues → hopelessness"]
├─ Score confidence: 0.95 for climate→anxiety, 0.88 for anxiety→insomnia
└─ Identify interventions: [{"link": "anxiety→insomnia", "roi": 0.92}]

Output: Causal JSON with intervention roadmap

STAGE 2: LETTA MEMORY
───────────────────────────────────────────────
Letta reads Session 1 transcript and:
├─ Updates trauma_timeline: "Climate news → anxiety cascade onset"
├─ Adds to coping_inventory: "No current coping strategies identified"
├─ Notes support_gaps: "Needs: Sleep protocols, anxiety management, social support"
└─ Stores: Full session in archival memory (searchable)

Output: Memory blocks updated + session archived

STAGE 3: CLAUDE PROTOCOL
───────────────────────────────────────────────
Claude reads Letta's memory and:
├─ Initializes assessment: "Acute climate anxiety with trauma response"
├─ Creates therapeutic_goals: "Reduce insomnia + build coping skills"
├─ Sets protocol_v1: "Focus on CBT + grounding techniques"
└─ Generates response: "You're not alone in this. Let's start with one technique: 
   progressive muscle relaxation for sleep..."

Output: Therapeutic response + Protocol created

BASE44 DASHBOARD
───────────────────────────────────────────────
Displays:
├─ Causal chain: "Climate News → Anxiety → Insomnia → Work Issues"
├─ Intervention ROI: "Anxiety→Insomnia has highest impact (92/100)"
├─ Memory created: "Trauma timeline initialized"
└─ Protocol: "CBT-focused approach started"

───────────────────────────────────────────────
3 WEEKS LATER: Session 2
───────────────────────────────────────────────

PARTICIPANT: "I tried those exercises. They actually helped me sleep 
better. Also joined a local climate action group—feels good to do something."

STAGE 1: GROQ RE-ANALYSIS (New Input)
├─ New causal chain: "Climate action → Agency → Reduced anxiety"
├─ Detects contradiction: "Action reduces anxiety, not just coping"
└─ Updates interventions: "Behavioral activation now primary intervention"

STAGE 2: LETTA SELF-EDITS
├─ Reads: Previous session (Session 1 memory)
├─ Self-edits: trauma_timeline + "Session 2: Breakthrough! Joined action group"
├─ Tool-call: memory_replace("coping_inventory", "progressive muscle relaxation ✓, 
   community action ✓✓✓")
└─ Stores: Session 2 in archive

STAGE 3: CLAUDE EVOLVES
├─ Reads: Letta's updated memory ("previous hopeless → now taking action")
├─ Extended thinking: "User showing behavioral activation effectiveness"
├─ Updates protocol_v2: "Shift from defensive (CBT) to offensive (action-oriented)"
├─ Generates: "I see a major shift in you. Last week you felt hopeless, now you're 
   leading change. Let's build on that..."
└─ Stores: Updated protocol in persistent files

BASE44 DASHBOARD
├─ Shows: "Causal analysis updated based on Session 2"
├─ Shows: "Letta memory evolved: action now primary coping strategy"
├─ Shows: "Claude protocol adapted: behavioral activation emphasized"
└─ Shows: "Participant mood: hopeless → hopeful"
Architecture Principles
1. Separation of Concerns
text
GROQ: Answers "WHY?" (Cause-effect reasoning)
  ├─ Question: Why does climate anxiety happen?
  ├─ Method: Mechanistic causal reasoning
  └─ Output: Causal chains + intervention points

LETTA: Answers "WHAT?" (Memory & learning)
  ├─ Question: What helps this specific person?
  ├─ Method: Self-editing memory blocks
  └─ Output: Personalized memory + progress tracking

CLAUDE: Answers "HOW?" (Therapeutic approach)
  ├─ Question: How should we help them evolve?
  ├─ Method: Persistent protocol evolution
  └─ Output: Adaptive therapeutic approach
2. Information Asymmetry
text
Each layer reads what it needs, not everything:

GROQ sees: Raw transcripts only (doesn't need memory)
LETTA sees: Groq causal analysis + transcript (uses both)
CLAUDE sees: Letta memory + transcript + previous protocols (uses all)

This is intentional: each layer adds context sequentially.
3. Persistence & Learning
text
GROQ: Stateless (re-analyzes each transcript from scratch)
LETTA: Stateful (remembers across sessions, self-edits)
CLAUDE: Stateful + Autonomous (remembers + decides what matters)

This creates a learning system: data → analysis → memory → evolution
Scalability Architecture
Processing 1000 Participants
text
Batch Processing Pipeline:

├─ Listen Labs (Parallel)
│  └─ Conducts 1000 interviews simultaneously
│  └─ Outputs: 1000 transcripts
│
├─ Groq (Parallel, batched)
│  └─ Process 100 transcripts at once
│  └─ Outputs: 1000 causal analyses (3-5 min total)
│
├─ Letta (Parallel, per-participant)
│  └─ Initialize 1000 agents
│  └─ Each agent manages own memory
│  └─ Outputs: 1000 memory blocks + archives
│
├─ Claude (Parallel, per-participant)
│  └─ Process 50 participants at once
│  └─ Each reads own memory, writes own protocol
│  └─ Outputs: 1000 protocols
│
└─ Base44 (Aggregation)
   └─ Visualize all 1000 journeys
   └─ Show patterns: "80% of participants benefit from action"
Cost Scaling
text
Per-Participant Cost:
├─ Listen Labs: $0.40 (interview recruitment + moderation)
├─ Groq: $0.10 (4-step reasoning chain)
├─ Letta: $0.15 (memory storage + tool calls)
├─ Claude: $0.25 (extended thinking + persistent memory)
└─ Total: ~$0.90 per participant

vs. Traditional Therapy: $150 per session
vs. Paid Therapist: $100-300/hour, weeks to get appointment

ClimateCircle: 99.4% cheaper, instant access, personalized.
Error Handling & Robustness
text
Groq Component:
├─ Failure: Transcript too short
│  └─ Fallback: "Insufficient data for causal analysis"
├─ Failure: No cause-effect pairs found
│  └─ Fallback: "Participant expressing feelings, not analyzable for causality"
└─ Retry: Groq API timeout → exponential backoff

Letta Component:
├─ Failure: Memory file corrupted
│  └─ Fallback: Reinitialize from archive
├─ Failure: Tool call fails
│  └─ Fallback: Store as text note (manual review later)
└─ Retry: Letta API timeout → queue for retry

Claude Component:
├─ Failure: Extended thinking exceeds budget
│  └─ Fallback: Use standard reasoning
├─ Failure: Memory read permission denied
│  └─ Fallback: Initialize new memory
└─ Retry: Claude API timeout → queue for retry
Security & Privacy
text
Data Flow Privacy:

User Transcript
  ├─ Raw audio: Stays on Listen Labs servers (encrypted)
  ├─ Transcript: Sent to Groq (HTTPS TLS 1.3)
  │  └─ Groq: Processes, does NOT store
  ├─ Causal analysis: Sent to Letta (HTTPS)
  │  └─ Letta: Stores in encrypted DB
  ├─ Memory + analysis: Sent to Claude (HTTPS)
  │  └─ Claude: Processes, returns updated protocol
  └─ All outputs: Kept in local /protocols/ folder (encrypted at rest)

Participant Identity:
├─ Stored as: participant_ID (not name)
├─ All files keyed by: participant_ID
├─ Names kept in separate, encrypted index
└─ GDPR compliant: Users can request full data export/deletion

API Keys:
├─ Stored in: .env file (NOT committed to Git)
├─ Accessed by: Environment variables only
├─ Rotated: Quarterly
└─ Audited: All API calls logged with timestamp, user_ID (no PII)
Monitoring & Observability
text
What Gets Logged:

GROQ Calls:
├─ Timestamp, transcript_length, causal_pairs_found, chains_generated
├─ Latency (should be < 30 seconds)
├─ Model used, tokens consumed
└─ Any errors/retries

LETTA Calls:
├─ Agent initialized, sessions tracked, memory_bytes stored
├─ Tool calls executed, success/failure rate
├─ Archival search performance (should be < 100ms)
└─ Any errors/retries

CLAUDE Calls:
├─ Protocol created/updated, protocol_version incremented
├─ Thinking tokens used, response latency
├─ Memory files read/written, file sizes
└─ Any errors/retries

Real-Time Dashboard:
├─ Processing queue depth (should be < 1000 in queue)
├─ API latencies (p50, p95, p99)
├─ Error rate (should be < 1%)
└─ Memory usage (per participant, aggregate)