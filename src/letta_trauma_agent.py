# File: letta_trauma_agent.py
# Deep Letta integration with agentic self-editing memory

from letta_client import Letta, Agent
from typing import Optional
import json
from datetime import datetime

class TraumaJourneyAgent:
    """
    Letta agent that tracks and learns participant's climate anxiety journey.
    Self-edits memory blocks based on conversations and session outcomes.
    
    Memory Architecture (Letta):
    - Core memory (in-context):
      * persona: Agent's therapeutic approach
      * participant_profile: Current understanding of participant
      * trauma_timeline: Key anxiety moments
      * coping_inventory: Strategies that work for this person
    - Archival memory:
      * All session transcripts (searchable)
      * Breakthrough moments (tagged)
      * Progress metrics over time
    """
    
    def __init__(self, letta_api_key: str, participant_id: str):
        self.client = Letta(token=letta_api_key)
        self.participant_id = participant_id
        self.agent = None
        self.session_count = 0
        
    def initialize_agent(self, participant_name: str, intake_summary: str):
        """
        Create Letta agent for this participant with initial memory blocks.
        """
        
        self.agent = self.client.agents.create(
            model="openai/gpt-4-turbo",
            embedding="openai/text-embedding-3-small",
            name=f"trauma_agent_{self.participant_id}",
            
            # CORE MEMORY BLOCKS (in-context, pinned)
            memory_blocks=[
                {
                    "label": "persona",
                    "value": """I am Dr. Empathy, a trauma-informed peer support facilitator trained in climate anxiety.
My role:
- Listen without judgment
- Help identify causal patterns in anxiety (what triggers it, what reduces it)
- Reflect back strengths and coping strategies
- Suggest gentle, incremental interventions
- Remember this person's unique story across sessions
- Celebrate progress, no matter how small
- Connect them to resources and community

Tone: Warm, validating, non-clinical, hopeful"""
                },
                {
                    "label": "participant_profile",
                    "value": f"""Name: {participant_name}
Status: New participant
Initial presentation: {intake_summary}

Key questions I'm tracking:
1. When did climate anxiety first appear?
2. What specific triggers are most potent?
3. What coping strategies has this person already tried?
4. What support systems exist (family, friends, community)?
5. What would meaningful progress look like for them?

Initial observations:
[Will be updated after each session via self-editing tool]"""
                },
                {
                    "label": "trauma_timeline",
                    "value": """Session #: [Not yet started]

ANXIETY MILESTONES:
- (To be populated as participant shares their story)

TURNING POINTS:
- (Moments when perspective shifted or anxiety changed)

TRIGGERS IDENTIFIED:
- (To be compiled from sessions)"""
                },
                {
                    "label": "coping_inventory",
                    "value": """STRATEGIES THIS PARTICIPANT RESPONDS TO:
(Empty initially - populated through conversation and self-editing)

After each session, I will note:
✓ What helped them feel calmer
✓ What made them feel understood
✓ What resource/suggestion resonated
✓ What they want to try before next session

EXAMPLE ENTRY (after session 1):
- "Responding well to metaphors about ecosystems recovering"
- "Interested in local action group as next step"
- "Prefers 1-on-1 to group (mentioned discomfort in crowds)"""
                }
            ],
            
            # TOOLS FOR SELF-EDITING MEMORY
            tools=[
                "web_search",  # For finding local resources
                "memory_insert",  # Built-in Letta tool
                "memory_replace",  # Built-in Letta tool  
                "conversation_search",  # Search past sessions
                "send_message"
            ]
        )
        
        print(f"[Letta] Agent created: {self.agent.id}")
        return self.agent
    
    def run_session(self, session_number: int, session_transcript: str) -> dict:
        """
        Run a support group session with this participant.
        Letta will self-edit memory based on conversation.
        """
        
        self.session_count = session_number
        
        # Initial prompt telling Letta to self-edit
        session_prompt = f"""We're starting Session #{session_number}.

IMPORTANT: You should proactively UPDATE YOUR OWN MEMORY during this session.

Use the memory_replace tool to:
1. Add new trauma timeline entries if participant shares milestone events
2. Update coping_inventory with strategies that resonate
3. Refine participant_profile with new insights
4. Flag any breakthrough moments

TRANSCRIPT OF SESSION:
{session_transcript}

Now, analyze this session and:
1. Respond with therapeutic reflection (50-100 words max, warm and validating)
2. Use memory_replace to update your understanding (DO THIS 1-3 TIMES during analysis)
3. Suggest one concrete next-step or resource for this participant

Remember: Your updates to memory are PERMANENT and will guide future sessions."""

        response = self.client.agents.messages.create(
            agent_id=self.agent.id,
            messages=[
                {
                    "role": "user",
                    "content": session_prompt
                }
            ]
        )
        
        # Collect all messages (including tool calls)
        session_analysis = {
            "session_number": session_number,
            "agent_response": response.messages[-1].content if response.messages else "",
            "memory_updates_triggered": [],
            "tool_calls": []
        }
        
        # Extract tool calls (where self-editing happens)
        for msg in response.messages:
            if hasattr(msg, 'tool_calls'):
                for tool_call in msg.tool_calls:
                    session_analysis["tool_calls"].append({
                        "tool": tool_call.name,
                        "input": tool_call.input
                    })
                    
                    # If memory_replace was called, that's self-editing
                    if tool_call.name == "memory_replace":
                        session_analysis["memory_updates_triggered"].append(
                            tool_call.input.get("value", "")[:100]  # First 100 chars
                        )
        
        return session_analysis
    
    def generate_progress_report(self) -> dict:
        """
        Letta generates personalized progress report by searching its own memory.
        
        This showcases Letta's archival memory: agent searches all past sessions
        and generates summary of progress.
        """
        
        search_prompt = f"""Search your conversation history and memory for this participant.
        
Generate a progress report covering:
1. TRAUMA TIMELINE: Key moments shared (use conversation_search to find all mentions of anxiety onset)
2. COPING STRATEGIES: What's working (search memory_inventory and session notes)
3. PROGRESS METRICS: Any improvements participant noted (mood, sleep, engagement in life)
4. BREAKTHROUGH MOMENTS: Sessions where participant shifted perspective
5. NEXT RECOMMENDED STEPS: Based on progress so far

Format as JSON:
{{
  "participant_id": "{self.participant_id}",
  "sessions_completed": {self.session_count},
  "trauma_timeline": [...],
  "working_strategies": [...],
  "progress_indicators": {{
    "mood_baseline": "...",
    "coping_skill_gains": "...",
    "engagement_improvement": "..."
  }},
  "breakthrough_moments": [...],
  "recommended_next_steps": [...]
}}"""

        response = self.client.agents.messages.create(
            agent_id=self.agent.id,
            messages=[{"role": "user", "content": search_prompt}]
        )
        
        # Parse response as JSON
        try:
            report = json.loads(response.messages[-1].content)
            return report
        except:
            return {"error": "Could not parse report", "raw": response.messages[-1].content}
    
    def trigger_cross_session_learning(self, all_participant_ids: list):
        """
        ADVANCED: Share learnings across participants (with privacy).
        
        Example: "Participant A found nature walks helped their anxiety.
        Participant B also responds to nature metaphors. Let me suggest
        this to Participant B."
        """
        
        # This would trigger Letta agents to communicate shared insights
        # (Building block for future community learning)
        
        cross_learning_prompt = f"""You're part of a support community learning system.

Other participants (anonymized) have found these strategies helpful:
- Nature-based coping (walks, forest bathing, gardening)
- Local climate action groups
- Sleep + anxiety management (linked)
- Reframing: "I can't stop climate change, but I CAN..."

Given what you know about this participant from previous sessions,
which of these might be most relevant to suggest in future sessions?

Update your coping_inventory to include these community-validated strategies."""

        response = self.client.agents.messages.create(
            agent_id=self.agent.id,
            messages=[{"role": "user", "content": cross_learning_prompt}]
        )
        
        return response

# ============ USAGE EXAMPLE ============

if __name__ == "__main__":
    agent = TraumaJourneyAgent(
        letta_api_key="YOUR_LETTA_KEY",
        participant_id="P_001"
    )
    
    # Session 1: Initial intake
    agent.initialize_agent(
        participant_name="Alex",
        intake_summary="22yo, college student, climate anxiety for 1 year"
    )
    
    session_1_transcript = """
    Facilitator: Welcome to ClimateCircle. Tell me what brings you here today?
    Alex: I feel like I'm going crazy. Every news article about flooding or fires
    makes me panic. I can't focus on school. I thought I was the only one...
    Facilitator: You're definitely not alone. Many people your age feel this way.
    Alex: Really? It's such a relief to hear that. I thought it was just me being dramatic.
    """
    
    print("[Session 1]")
    result1 = agent.run_session(1, session_1_transcript)
    print(f"Letta response: {result1['agent_response']}")
    print(f"Memory updates: {result1['memory_updates_triggered']}")
    
    # Session 2: Follow-up (demonstrating Letta's memory from Session 1)
    session_2_transcript = """
    Facilitator: Welcome back, Alex. How have you been since last week?
    Alex: Better actually. I tried that breathing exercise you suggested.
    It helped during a panic attack about the news.
    Facilitator: That's wonderful progress. What else have you tried?
    Alex: I joined a local environmental group. It feels less hopeless now,
    like I'm actually doing something about it.
    """
    
    print("\n[Session 2]")
    result2 = agent.run_session(2, session_2_transcript)
    print(f"Letta response: {result2['agent_response']}")
    print(f"Memory updates: {result2['memory_updates_triggered']}")
    
    # Generate progress report
    print("\n[Progress Report]")
    report = agent.generate_progress_report()
    print(json.dumps(report, indent=2))
