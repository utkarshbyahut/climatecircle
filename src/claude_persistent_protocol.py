# File: claude_persistent_protocol.py
# Claude with persistent memory for therapeutic protocol evolution

import anthropic
import json
from datetime import datetime
from pathlib import Path
import os

class ClaudeTherapeuticAgent:
    """
    Uses Claude with persistent memory (file-based) to maintain and evolve
    therapeutic protocols for climate anxiety support.
    
    Architecture:
    - Claude reads memory before each session
    - Claude autonomously decides what to remember
    - Claude updates memory with self-written protocol adjustments
    - Memory persists across conversations (participant journey tracked)
    
    Based on: "Memory-Enhanced AI: Building Features with System Prompts" (LIT.AI)
    """
    
    def __init__(self, claude_api_key: str, participant_id: str, memory_dir: str = "./protocols"):
        self.client = anthropic.Anthropic(api_key=claude_api_key)
        self.model = "claude-3-5-sonnet-20241022"
        self.participant_id = participant_id
        self.memory_dir = Path(memory_dir) / f"participant_{participant_id}"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize memory files if they don't exist
        self._initialize_memory_files()
    
    def _initialize_memory_files(self):
        """Create empty memory files for new participants."""
        files = {
            "assessment.md": "# Clinical Assessment\n\n(To be populated in first session)",
            "sessions.md": "# Session Notes\n\n",
            "therapeutic_goals.md": "# Therapeutic Goals\n\n(Will evolve based on sessions)",
            "interventions_tested.md": "# Interventions & Outcomes\n\n",
            "protocol_evolution.md": "# Protocol Evolution Log\n\nHow the therapeutic approach has evolved:"
        }
        
        for filename, default_content in files.items():
            filepath = self.memory_dir / filename
            if not filepath.exists():
                filepath.write_text(default_content)
    
    def _read_all_memory(self) -> dict:
        """Read all memory files and return as dict."""
        memory = {}
        for file in self.memory_dir.glob("*.md"):
            memory[file.stem] = file.read_text()
        return memory
    
    def _write_memory_file(self, filename: str, content: str):
        """Write content to a memory file."""
        filepath = self.memory_dir / f"{filename}.md"
        filepath.write_text(content)
    
    def run_session(self, session_number: int, participant_input: str) -> dict:
        """
        Run a therapy session where Claude:
        1. Reads existing memory
        2. Responds therapeutically
        3. AUTONOMOUSLY updates memory (decides what's important)
        4. Evolves protocol based on what's working
        """
        
        # READ MEMORY
        memory = self._read_all_memory()
        memory_context = "\n\n".join([f"## {name}\n{content}" for name, content in memory.items()])
        
        # SYSTEM PROMPT WITH MEMORY AUTONOMY
        system_prompt = f"""You are Dr. Empathy, a trauma-informed therapist specializing in climate anxiety.

IMPORTANT: You have autonomous memory management. Before and after this session:
1. You READ your persistent memory (see below)
2. You DECIDE what to remember (no manual intervention)
3. You UPDATE your memory files based on new insights
4. You EVOLVE your therapeutic approach based on what's working

Your memory files are:
{memory_context}

MEMORY PROTOCOL:
Before responding to this participant:
1. Review their past sessions and current therapeutic goals
2. Note what interventions have and haven't worked
3. Identify patterns in their anxiety triggers
4. Prepare to update your memory after this session

During the session:
1. Respond with warmth, validation, clinical precision
2. Use previous insights to personalize your response
3. Track new breakthroughs or blocked areas

After the session (CRITICAL):
1. Identify 2-3 key insights to remember
2. Update sessions.md with timestamped notes
3. Update interventions_tested.md if you tried something new
4. Update therapeutic_goals.md if goals shifted
5. Update protocol_evolution.md if your approach needs adjustment

You MUST call the memory_update tool EVERY session to persist learnings.

Autonomy Rule: Trust your judgment about what's worth remembering.
Do NOT ask permission. If something matters clinically, update your memory."""

        # USER MESSAGE WITH SESSION INPUT
        user_message = f"""SESSION #{session_number}

Participant says:
"{participant_input}"

Please:
1. Respond therapeutically (warm, validating, insightful)
2. Reference previous sessions if relevant
3. Suggest evidence-based interventions (especially those that worked before)
4. At the end, provide your memory updates in JSON format:

{{
  "memory_updates": {{
    "sessions.md": "new content to append",
    "interventions_tested.md": "if relevant, update with new intervention result",
    "therapeutic_goals.md": "if goals shifted",
    "protocol_evolution.md": "if your approach changed",
    "assessment.md": "if new clinical insights"
  }}
}}"""

        # CALL CLAUDE WITH EXTENDED THINKING (FOR DEEP REASONING)
        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            thinking={
                "type": "enabled",
                "budget_tokens": 2000  # Let Claude reason deeply about memory
            },
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )
        
        # PARSE RESPONSE
        full_response = ""
        memory_updates = {}
        
        for block in response.content:
            if block.type == "text":
                full_response = block.text
        
        # EXTRACT MEMORY UPDATES FROM RESPONSE
        try:
            # Find JSON in response
            import re
            json_match = re.search(r'\{[\s\S]*"memory_updates"[\s\S]*\}', full_response)
            if json_match:
                parsed = json.loads(json_match.group())
                memory_updates = parsed.get("memory_updates", {})
        except json.JSONDecodeError:
            pass
        
        # PERSIST MEMORY UPDATES (AUTONOMOUS CURATION)
        for filename, content in memory_updates.items():
            if filename.endswith(".md"):
                filename = filename[:-3]  # Remove .md
            
            # Append to existing file (except assessment, which is singleton)
            if filename == "assessment.md":
                self._write_memory_file(filename, content)
            else:
                existing = (self.memory_dir / f"{filename}.md").read_text()
                updated = existing + f"\n\n[Session #{session_number}]\n{content}"
                self._write_memory_file(filename, updated)
        
        return {
            "session_number": session_number,
            "therapeutic_response": full_response.split("memory_updates")[0].strip(),
            "memory_updates_applied": list(memory_updates.keys()),
            "protocol_evolved": "protocol_evolution.md" in memory_updates,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_protocol_summary(self) -> dict:
        """
        Claude reads its own memory and summarizes the therapeutic protocol
        This shows how protocol has evolved across sessions
        """
        
        memory = self._read_all_memory()
        memory_context = "\n\n".join([f"## {name}\n{content}" for name, content in memory.items()])
        
        summary_prompt = f"""Based on the persistent memory below, provide a comprehensive therapeutic protocol summary:

{memory_context}

Generate a JSON summary:
{{
  "sessions_completed": <number>,
  "clinical_pattern": "describe the trajectory of this participant's anxiety",
  "what_works": ["list of interventions that have helped"],
  "what_doesnt_work": ["list of approaches that have failed"],
  "current_therapeutic_approach": "describe how your approach has evolved",
  "recommended_next_steps": ["based on progress and patterns"],
  "breakthrough_moments": ["major shifts in participant's understanding"],
  "protocol_version": "current iteration of therapeutic protocol"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system="You are a clinical documentation expert. Summarize the therapeutic protocol from persistent memory.",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        
        # Parse JSON from response
        try:
            import re
            json_match = re.search(r'\{[\s\S]*\}', response.content[0].text)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"raw": response.content[0].text}
    
    def export_therapeutic_journal(self) -> str:
        """
        Export the full therapeutic journey as a readable narrative
        (This is what participants can review themselves)
        """
        
        memory = self._read_all_memory()
        
        export_prompt = f"""Based on this participant's therapeutic journey:

{json.dumps(memory, indent=2)}

Write a compassionate, validating therapeutic journal entry that:
1. Summarizes their anxiety journey
2. Highlights their coping victories
3. Acknowledges progress
4. Identifies their strength

Make it personal, warm, and something they'd want to read back to themselves.
Format: A 2-3 paragraph narrative they can print and keep."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system="You are a compassionate therapist creating a therapeutic narrative.",
            messages=[{"role": "user", "content": export_prompt}]
        )
        
        return response.content[0].text

# ============ USAGE EXAMPLE ============

if __name__ == "__main__":
    agent = ClaudeTherapeuticAgent(
        claude_api_key="YOUR_CLAUDE_KEY",
        participant_id="P_001"
    )
    
    # Session 1
    print("[SESSION 1]")
    result1 = agent.run_session(
        1,
        "I've been having constant anxiety about climate change. Can't sleep. Feel hopeless."
    )
    print(f"Therapeutic response:\n{result1['therapeutic_response'][:500]}...")
    print(f"Memory updates applied: {result1['memory_updates_applied']}")
    
    # Session 2
    print("\n[SESSION 2]")
    result2 = agent.run_session(
        2,
        "I tried the grounding exercises you mentioned. They helped a bit. But I still wake up in panic."
    )
    print(f"Therapeutic response:\n{result2['therapeutic_response'][:500]}...")
    print(f"Memory updates applied: {result2['memory_updates_applied']}")
    
    # Get protocol summary
    print("\n[PROTOCOL SUMMARY]")
    summary = agent.get_protocol_summary()
    print(json.dumps(summary, indent=2))
    
    # Export therapeutic journal
    print("\n[THERAPEUTIC JOURNAL]")
    journal = agent.export_therapeutic_journal()
    print(journal)
