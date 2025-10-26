# File: causal_reasoning_engine.py
# Deep Groq integration for climate anxiety causal analysis

from groq import Groq
import json
import re

class CausalReasoningEngine:
    """
    Analyzes climate anxiety transcripts to identify causal chains.
    Uses Groq for ultra-fast multi-step reasoning.
    
    Based on research: "Assessing LLM Reasoning Through Implicit Causal Chain 
    Discovery in Climate Discourse" (arXiv:2510.13417)
    """
    
    def __init__(self, groq_api_key: str):
        self.client = Groq(api_key=groq_api_key)
        self.model = "mixtral-8x7b-32768"  # Fast, reasoning-capable
        
    def extract_causal_pairs(self, transcript: str) -> dict:
        """
        STEP 1: Identify all cause-effect pairs in the transcript
        Output: {"pairs": [{"cause": "X", "effect": "Y"}, ...]}
        """
        
        extraction_prompt = f"""Analyze this climate anxiety interview transcript and extract ALL cause-effect pairs.

TRANSCRIPT:
{transcript}

Return ONLY valid JSON with this structure:
{{
  "pairs": [
    {{"cause": "specific cause phrase", "effect": "specific effect phrase", "explicit": true/false}},
    ...
  ]
}}

Include both explicit causal statements ("because...") and implicit ones (temporal/logical connections).
Be exhaustive—find 5-10 pairs minimum."""

        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": extraction_prompt}],
            max_tokens=1000,
            temperature=0.3  # Low temp for precision
        )
        
        # Parse JSON from response
        try:
            pairs = json.loads(response.content[0].text)
            return pairs
        except json.JSONDecodeError:
            # Fallback: extract JSON from messy response
            json_match = re.search(r'\{.*\}', response.content[0].text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"pairs": []}
    
    def generate_implicit_causal_chains(self, pairs: list) -> list:
        """
        STEP 2: Connect cause-effect pairs into longer causal chains
        
        Input: [{"cause": "climate news", "effect": "anxiety"}, 
                {"cause": "anxiety", "effect": "insomnia"}]
        Output: ["climate news → anxiety → insomnia → work performance decline"]
        """
        
        pairs_text = "\n".join([f"- {p['cause']} → {p['effect']}" for p in pairs])
        
        chains_prompt = f"""Given these causal relationships, generate complete implicit causal chains.
        
CAUSAL RELATIONSHIPS:
{pairs_text}

Your task: Create longer chains that connect these pairs logically and sequentially.
For example: A → B, B → C, C → D becomes "A → B → C → D"

Rules:
1. Chain must follow logical sequence (B happens after A)
2. Include ALL transitive relationships
3. Return as numbered list: "1. A → B → C → D"
4. Generate 3-5 complete chains minimum

Output format:
CHAINS:
1. [full causal chain]
2. [full causal chain]
...

Be specific and use actual phrases from the pairs above."""

        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": chains_prompt}],
            max_tokens=1500,
            temperature=0.4
        )
        
        # Parse chains from response
        chains = re.findall(r'\d+\.\s*(.+?)(?=\n|$)', response.content[0].text)
        return chains
    
    def evaluate_causal_confidence(self, transcript: str, chains: list) -> dict:
        """
        STEP 3: Assign confidence scores to each causal link
        
        Returns: {
            "chain_1": {
                "chain": "A → B → C",
                "links": [
                    {"connection": "A→B", "confidence": 0.95, "evidence": "..."},
                    {"connection": "B→C", "confidence": 0.78, "evidence": "..."}
                ],
                "overall_confidence": 0.86
            }
        }
        """
        
        chains_text = "\n".join([f"- {chain}" for chain in chains])
        
        confidence_prompt = f"""For each causal chain, evaluate confidence in the causal connection.

TRANSCRIPT:
{transcript}

CAUSAL CHAINS:
{chains_text}

For EACH link in EACH chain, provide:
1. Confidence score (0-1): How strongly does evidence support this causal link?
2. Evidence: Direct quote or reasoning from transcript

Use these criteria:
- 0.9-1.0: Explicit statement ("Because X, I feel Y")
- 0.7-0.9: Clear temporal/logical sequence
- 0.5-0.7: Implied connection, needs inference
- 0.3-0.5: Weak connection, needs substantial reasoning
- <0.3: Speculative or unsupported

Return JSON:
{{
  "chain_1": {{
    "chain": "A → B → C",
    "links": [
      {{"connection": "A→B", "confidence": 0.95, "evidence": "exact quote"}},
      {{"connection": "B→C", "confidence": 0.78, "evidence": "reasoning"}}
    ],
    "overall_confidence": 0.86
  }}
}}"""

        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": confidence_prompt}],
            max_tokens=2000,
            temperature=0.3
        )
        
        try:
            confidence_data = json.loads(response.content[0].text)
            return confidence_data
        except:
            return {}
    
    def identify_intervention_points(self, chains: list, confidence_data: dict) -> dict:
        """
        STEP 4: Find the MOST IMPACTFUL points to intervene in causal chain
        
        Example: In "climate news → anxiety → insomnia → work issues"
        Intervening at "anxiety → insomnia" is higher ROI than "climate news"
        (can't stop climate news, but CAN help with anxiety/insomnia)
        
        Returns: {
            "highest_roi_interventions": [
                {
                    "link": "anxiety → insomnia",
                    "roi_score": 0.92,
                    "reasoning": "High confidence link, modifiable via therapy/sleep hygiene"
                }
            ]
        }
        """
        
        chains_json = json.dumps(chains)
        confidence_json = json.dumps(confidence_data)
        
        intervention_prompt = f"""Analyze these causal chains and identify high-ROI intervention points.

CHAINS:
{chains_json}

CONFIDENCE SCORES:
{confidence_json}

Task: Identify the 2-3 causal links where intervention would have HIGHEST impact.

Criteria for high ROI:
1. High confidence (0.8+) - we're sure this link exists
2. Modifiable - intervention is possible (not "stop climate crisis")
3. Leverage - fixing this link blocks other downstream effects
4. Feasible - interventions exist (therapy, sleep hygiene, community support, etc.)

Return JSON:
{{
  "highest_roi_interventions": [
    {{
      "link": "A → B",
      "confidence": 0.9,
      "roi_score": 0.92,
      "modifiability": "high",
      "leverage_blocked_effects": 3,
      "suggested_interventions": ["therapy", "sleep protocol", "peer support"],
      "reasoning": "Detailed explanation"
    }}
  ]
}}"""

        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": intervention_prompt}],
            max_tokens=1500,
            temperature=0.3
        )
        
        try:
            return json.loads(response.content[0].text)
        except:
            return {}
    
    def analyze_transcript_end_to_end(self, transcript: str) -> dict:
        """
        COMPLETE PIPELINE: All 4 steps in sequence
        
        Returns comprehensive causal analysis with:
        - All identified cause-effect pairs
        - Implicit causal chains
        - Confidence scores
        - Intervention recommendations
        """
        
        print("[Groq] Step 1/4: Extracting causal pairs...")
        pairs = self.extract_causal_pairs(transcript)
        pair_list = pairs.get("pairs", [])
        
        if not pair_list:
            return {"error": "No causal pairs found"}
        
        print(f"[Groq] Found {len(pair_list)} causal pairs")
        print(f"[Groq] Step 2/4: Generating implicit causal chains...")
        chains = self.generate_implicit_causal_chains(pair_list)
        
        print(f"[Groq] Found {len(chains)} causal chains")
        print(f"[Groq] Step 3/4: Evaluating causal confidence...")
        confidence = self.evaluate_causal_confidence(transcript, chains)
        
        print(f"[Groq] Step 4/4: Identifying intervention points...")
        interventions = self.identify_intervention_points(chains, confidence)
        
        # Assemble comprehensive output
        return {
            "transcript_summary": transcript[:200] + "...",
            "causal_pairs_found": len(pair_list),
            "pairs": pair_list[:5],  # Top 5 for brevity
            "causal_chains": chains,
            "confidence_analysis": confidence,
            "intervention_recommendations": interventions,
            "processing_model": self.model,
            "reasoning_depth": "4-step mechanistic causal reasoning"
        }

# ============ USAGE EXAMPLE ============

if __name__ == "__main__":
    engine = CausalReasoningEngine(groq_api_key="YOUR_GROQ_KEY")
    
    sample_transcript = """
    I've been really anxious lately. Every time I see climate news, I get this knot in my stomach.
    Then I can't sleep at night because I keep thinking about wildfires and flooding. 
    When I don't sleep, I can't focus at work, and I feel irritable with everyone around me.
    It's like this cycle that keeps feeding itself.
    """
    
    analysis = engine.analyze_transcript_end_to_end(sample_transcript)
    
    print("\n" + "="*60)
    print("CAUSAL REASONING ANALYSIS")
    print("="*60)
    print(json.dumps(analysis, indent=2))
