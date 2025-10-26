API_REFERENCE.md — Complete ClimateCircle API Documentation

1. CausalReasoningEngine (Groq)
Location: src/causal_reasoning_engine.py
Mechanistic causal reasoning pipeline for climate anxiety transcripts.

Initialization
python
from src.causal_reasoning_engine import CausalReasoningEngine

engine = CausalReasoningEngine(groq_api_key="sk-...")
Parameters:

groq_api_key (str, required): Groq API key from console.groq.com

Method: extract_causal_pairs(transcript)
Extract all cause-effect pairs from interview transcript.

Signature:

python
def extract_causal_pairs(self, transcript: str) -> dict
Returns:

python
{
  "pairs": [
    {"cause": "climate news", "effect": "anxiety", "explicit": True},
    {"cause": "anxiety", "effect": "insomnia", "explicit": True}
  ]
}
Example:

python
result = engine.extract_causal_pairs("Climate news makes me anxious and I can't sleep")
print(f"Found {len(result['pairs'])} pairs")
Method: generate_implicit_causal_chains(pairs)
Connect cause-effect pairs into longer chains.

Signature:

python
def generate_implicit_causal_chains(self, pairs: list) -> list
Returns:

python
[
  "climate news → anxiety → insomnia → work issues",
  "catastrophe thinking → helplessness → social withdrawal"
]
Method: evaluate_causal_confidence(transcript, chains)
Score confidence for each causal link (0-1 scale).

Signature:

python
def evaluate_causal_confidence(self, transcript: str, chains: list) -> dict
Returns:

python
{
  "chain_1": {
    "chain": "climate news → anxiety → insomnia",
    "links": [
      {"connection": "climate news→anxiety", "confidence": 0.95, "evidence": "..."},
      {"connection": "anxiety→insomnia", "confidence": 0.78, "evidence": "..."}
    ],
    "overall_confidence": 0.86
  }
}
Confidence Scale:

0.9-1.0: Explicit ("Because X, I feel Y")

0.7-0.9: Clear temporal sequence

0.5-0.7: Implied, needs inference

0.3-0.5: Weak connection

<0.3: Speculative

Method: identify_intervention_points(chains, confidence_data)
Find highest-ROI intervention points in causal chains.

Signature:

python
def identify_intervention_points(self, chains: list, confidence_data: dict) -> dict
Returns:

python
{
  "highest_roi_interventions": [
    {
      "link": "anxiety → insomnia",
      "confidence": 0.95,
      "roi_score": 0.92,
      "modifiability": "high",
      "leverage_blocked_effects": 3,
      "suggested_interventions": ["CBT for sleep", "meditation", "peer support"],
      "reasoning": "High confidence + modifiable + blocks 3 effects"
    }
  ]
}
Method: analyze_transcript_end_to_end(transcript)
Complete 4-step pipeline on single transcript.

Signature:

python
def analyze_transcript_end_to_end(self, transcript: str) -> dict
Returns:

python
{
  "transcript_summary": "First 200 chars...",
  "causal_pairs_found": 5,
  "pairs": [...],
  "causal_chains": [...],
  "confidence_analysis": {...},
  "intervention_recommendations": {...},
  "processing_model": "mixtral-8x7b-32768",
  "reasoning_depth": "4-step mechanistic causal reasoning"
}
Latency: 20-40 seconds (multiple LLM calls)

Example:

python
full_analysis = engine.analyze_transcript_end_to_end(transcript)
print(f"Pairs: {full_analysis['causal_pairs_found']}")
print(f"Best intervention: {full_analysis['intervention_recommendations']['highest_roi_interventions']['link']}")
2. TraumaJourneyAgent (Letta)
Location: src/letta_trauma_agent.py
Self-editing agent memory for multi-session participant tracking.

Initialization
python
from src.letta_trauma_agent import TraumaJourneyAgent

agent = TraumaJourneyAgent(
    letta_api_key="...",
    participant_id="P_001"
)
Parameters:

letta_api_key (str, required): Letta API key

participant_id (str, required): Unique identifier (e.g., "P_001")

Method: initialize_agent(participant_name, intake_summary)
Create new Letta agent with 4 memory blocks.

Signature:

python
def initialize_agent(self, participant_name: str, intake_summary: str) -> Agent
Memory Blocks:

persona: Agent's therapeutic approach

participant_profile: Understanding of participant

trauma_timeline: Key anxiety milestones

coping_inventory: Strategies that work

Example:

python
agent.initialize_agent(
    "Alex",
    "22yo college student, climate anxiety 1 year, insomnia"
)
Method: run_session(session_number, session_transcript)
Process single session, trigger self-editing of memory.

Signature:

python
def run_session(self, session_number: int, session_transcript: str) -> dict
Returns:

python
{
  "session_number": 1,
  "agent_response": "Warm therapeutic response...",
  "memory_updates_triggered": [
    "Updated trauma_timeline with new anxiety milestone",
    "Added breathing exercise to coping_inventory"
  ],
  "tool_calls": [
    {"tool": "memory_replace", "input": "..."},
    {"tool": "memory_insert", "input": "..."}
  ]
}
Example:

python
result = agent.run_session(1, transcript)
print(f"Memory updated: {len(result['memory_updates_triggered'])} times")

# Session 2 (3 weeks later) - Agent reads Session 1 memory automatically
result2 = agent.run_session(2, new_transcript)
print(f"Agent adapted: {result2['agent_response'][:100]}...")
Method: generate_progress_report()
Agent searches own memory to generate progress summary.

Signature:

python
def generate_progress_report(self) -> dict
Returns:

python
{
  "participant_id": "P_001",
  "sessions_completed": 3,
  "trauma_timeline": [
    "Session 1: Climate anxiety onset identified",
    "Session 2: Breakthrough - joined action group",
    "Session 3: Now leading meetings in action group"
  ],
  "working_strategies": [
    "Breathing exercises (67% effective)",
    "Community action/activism (89% effective)",
    "Nature walks (45% effective)"
  ],
  "progress_indicators": {
    "mood_baseline": "hopelessness (Session 1)",
    "mood_current": "agency + purpose (Session 3)",
    "coping_skill_gains": "3 new strategies adopted"
  },
  "breakthrough_moments": [
    "Session 2: Joined climate action group",
    "Session 3: Volunteered to lead group"
  ],
  "recommended_next_steps": [
    "Deepen climate action involvement",
    "Develop leadership skills",
    "Connect to broader climate movement"
  ]
}
Example:

python
report = agent.generate_progress_report()
for milestone in report['trauma_timeline']:
    print(f"  • {milestone}")
Method: trigger_cross_session_learning(all_participant_ids)
Share anonymized learnings across participants.

Signature:

python
def trigger_cross_session_learning(self, all_participant_ids: list) -> Response
Example:

python
all_participants = ["P_001", "P_002", "P_003"]
agent.trigger_cross_session_learning(all_participants)
# Agent now knows: "Other participants benefited from nature-based coping"
3. ClaudeTherapeuticAgent (Claude)
Location: src/claude_persistent_protocol.py
Persistent therapeutic protocol with autonomous evolution.

Initialization
python
from src.claude_persistent_protocol import ClaudeTherapeuticAgent

agent = ClaudeTherapeuticAgent(
    claude_api_key="sk-ant-...",
    participant_id="P_001",
    memory_dir="./protocols"  # Optional
)
Parameters:

claude_api_key (str, required): Claude API key

participant_id (str, required): Unique participant ID

memory_dir (str, optional): Directory for persistent files (default: "./protocols")

Memory Files Created:

assessment.md: Initial clinical assessment

sessions.md: Timestamped session notes

therapeutic_goals.md: Evolving goals + progress

interventions_tested.md: What's worked, what hasn't

protocol_evolution.md: How approach has changed

Method: run_session(session_number, participant_input)
Run therapy session with autonomous memory updates.

Signature:

python
def run_session(self, session_number: int, participant_input: str) -> dict
Returns:

python
{
  "session_number": 1,
  "therapeutic_response": "Claude's warm, validating response...",
  "memory_updates_applied": [
    "assessment.md",
    "sessions.md",
    "therapeutic_goals.md"
  ],
  "protocol_evolved": False,
  "timestamp": "2025-10-26T15:30:00"
}
Example:

python
agent = ClaudeTherapeuticAgent(claude_api_key="...", participant_id="P_001")

# Session 1
result1 = agent.run_session(1, "I feel hopeless about climate. Can't sleep.")
print(f"Response: {result1['therapeutic_response']}")

# Session 2 (Claude reads Session 1 memory automatically)
result2 = agent.run_session(2, "I joined a climate action group. It's helping.")
print(f"Protocol evolved: {result2['protocol_evolved']}")  # Likely True
Method: get_protocol_summary()
Claude summarizes therapeutic protocol and evolution.

Signature:

python
def get_protocol_summary(self) -> dict
Returns:

python
{
  "sessions_completed": 3,
  "clinical_pattern": "Initial crisis → effective action-based coping → leadership engagement",
  "what_works": [
    "Behavioral activation (joining action group)",
    "Community connection",
    "Sense of agency/contribution"
  ],
  "what_doesnt_work": [
    "Traditional CBT (user resistant)",
    "Solo coping strategies (too isolating)"
  ],
  "current_therapeutic_approach": "Action-oriented + community-based resilience building",
  "recommended_next_steps": [
    "Deepen leadership role in climate action",
    "Explore climate justice frameworks",
    "Consider mentoring role"
  ],
  "breakthrough_moments": [
    "Session 2: Joined climate action group",
    "Session 3: Volunteered to lead meetings"
  ],
  "protocol_version": 3
}
Example:

python
summary = agent.get_protocol_summary()
print(f"Protocol Version: {summary['protocol_version']}")
print(f"What works: {summary['what_works']}")
Method: export_therapeutic_journal()
Generate warm narrative of participant's journey.

Signature:

python
def export_therapeutic_journal(self) -> str
Returns: Narrative text suitable for printing/email

Example Output:

text
Dear Alex,

As I reflect on our journey together over these past weeks, I'm struck by 
the courage you've shown. You came to me feeling hopeless and overwhelmed. 
Every news story about climate felt like a personal attack.

And then something shifted. In our second session, you mentioned joining a 
climate action group. Your face lit up. For the first time, your anxiety 
had a direction—outward into meaningful action.

By our third session, you weren't just attending. You were leading them. 
That's not progress. That's transformation.

Your anxiety isn't a flaw. It's a signal that you care. And now you've 
channeled that care into something powerful.

Keep going. Lead. Build. Create change.

With deep respect,
Dr. Empathy
Example:

python
journal = agent.export_therapeutic_journal()
with open("my_journey.txt", "w") as f:
    f.write(journal)
Integration Example: Running All Three
python
import os
from src.causal_reasoning_engine import CausalReasoningEngine
from src.letta_trauma_agent import TraumaJourneyAgent
from src.claude_persistent_protocol import ClaudeTherapeuticAgent

# Setup
groq_key = os.getenv("GROQ_API_KEY")
letta_key = os.getenv("LETTA_API_KEY")
claude_key = os.getenv("CLAUDE_API_KEY")

transcript = "I've been really anxious about climate change..."

# STAGE 1: Groq Causal Analysis
groq = CausalReasoningEngine(groq_key)
causal_analysis = groq.analyze_transcript_end_to_end(transcript)
print(f"Causal pairs: {causal_analysis['causal_pairs_found']}")

# STAGE 2: Letta Memory
letta = TraumaJourneyAgent(letta_key, "P_001")
letta.initialize_agent("Alex", "22yo, climate anxiety")
letta_result = letta.run_session(1, transcript)
print(f"Memory updates: {len(letta_result['memory_updates_triggered'])}")

# STAGE 3: Claude Protocol
claude = ClaudeTherapeuticAgent(claude_key, "P_001")
claude_result = claude.run_session(1, transcript)
print(f"Protocol evolved: {claude_result['protocol_evolved']}")

# Get reports
letta_report = letta.generate_progress_report()
claude_summary = claude.get_protocol_summary()
Error Handling
python
from groq import APITimeoutError, AuthenticationError
import anthropic

# Groq errors
try:
    analysis = engine.analyze_transcript_end_to_end(transcript)
except APITimeoutError:
    print("Groq timeout, retrying...")
except AuthenticationError:
    print("Invalid API key")

# Claude errors
try:
    result = agent.run_session(1, transcript)
except anthropic.APIError as e:
    print(f"Claude error: {e}")

# Letta errors
try:
    agent.initialize_agent("Name", "summary")
except Exception as e:
    print(f"Letta error: {e}")
All methods are production-ready and error-tolerant.