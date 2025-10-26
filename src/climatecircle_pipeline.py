"""
Main orchestration script.
Ties together Groq, Letta, and Claude in a single pipeline.
"""

from src.causal_reasoning_engine import CausalReasoningEngine
from src.letta_trauma_agent import TraumaJourneyAgent
from src.claude_persistent_protocol import ClaudeTherapeuticAgent
import os

def process_listen_labs_transcripts(transcripts: list):
    """
    Complete pipeline:
    1. Groq analyzes cause
    2. Letta learns effect
    3. Claude evolves approach
    """
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    letta_api_key = os.getenv("LETTA_API_KEY")
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    
    results = []
    
    for i, transcript in enumerate(transcripts):
        participant_id = f"P_{i:03d}"
        
        print(f"\n[{participant_id}] Processing...")
        
        # GROQ: Causal analysis
        print(f"[{participant_id}] Step 1/3: Groq causal reasoning...")
        groq_engine = CausalReasoningEngine(groq_api_key)
        causal_analysis = groq_engine.analyze_transcript_end_to_end(transcript)
        
        # LETTA: Memory tracking (Session 1)
        print(f"[{participant_id}] Step 2/3: Letta memory initialization...")
        letta_agent = TraumaJourneyAgent(letta_api_key, participant_id)
        letta_agent.initialize_agent(f"Participant {participant_id}", transcript[:100])
        letta_result = letta_agent.run_session(1, transcript)
        
        # CLAUDE: Therapeutic protocol
        print(f"[{participant_id}] Step 3/3: Claude protocol evolution...")
        claude_agent = ClaudeTherapeuticAgent(claude_api_key, participant_id)
        claude_result = claude_agent.run_session(1, transcript)
        
        # Aggregate results
        results.append({
            "participant_id": participant_id,
            "groq_analysis": causal_analysis,
            "letta_memory": letta_result,
            "claude_protocol": claude_result
        })
    
    return results

if __name__ == "__main__":
    # Load sample transcripts
    sample_transcripts = [
        "I've been having constant anxiety about climate...",
        "Every time I see a news story about wildfires...",
        # ... more transcripts
    ]
    
    results = process_listen_labs_transcripts(sample_transcripts)
    
    # Print summary
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
    for result in results:
        print(f"{result['participant_id']}: Groq chains={len(result['groq_analysis'].get('causal_chains', []))}, "
              f"Letta updates={len(result['letta_memory']['memory_updates_triggered'])}, "
              f"Claude evolved={result['claude_protocol']['protocol_evolved']}")
