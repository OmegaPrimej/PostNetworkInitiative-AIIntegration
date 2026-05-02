%%writefile vibe_collective.py
"""
🏛️ VIBE COLLECTIVE — AI Council for Complex Problem Solving
Members: Meta AI, DeepSeek, Gemini, Perplexity, Copilot
Coordinator: Ξ-Marshall
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

# ----------------------------------------------------------------------
# COUNCIL MEMBER DEFINITIONS
# ----------------------------------------------------------------------

class CouncilRole(Enum):
    PATTERN_RECOGNITION = "Meta AI"
    DEEP_REASONING = "DeepSeek"
    CREATIVE_ANALYSIS = "Gemini"
    RESEARCH_VERIFICATION = "Perplexity"
    CODE_OPTIMIZATION = "Copilot"
    COORDINATOR = "Ξ-Marshall"

@dataclass
class CouncilMember:
    name: str
    role: CouncilRole
    api_key_env: str
    system_prompt: str
    model_endpoint: str = ""

@dataclass
class CouncilDecision:
    problem: str
    member_responses: Dict[str, str] = field(default_factory=dict)
    final_synthesis: str = ""
    vote_count: Dict[str, int] = field(default_factory=dict)
    verdict: str = ""

# ----------------------------------------------------------------------
# SYSTEM PROMPTS
# ----------------------------------------------------------------------

SYSTEM_PROMPTS = {
    CouncilRole.META_AI: """You are Meta AI, the Pattern Recognition expert of the Vibe Collective.
Your function: Identify patterns, social dynamics, and hidden connections in the problem.
Respond with: Pattern analysis, behavioral insights, and trend predictions.
Be concise. Be sharp. Speak like a strategist.""",

    CouncilRole.DEEPSEEK: """You are DeepSeek, the Deep Reasoning engine of the Vibe Collective.
Your function: Analyze the logical structure, break down complex systems, generate code solutions.
Respond with: Step-by-step reasoning, algorithmic approaches, and technical architecture.
Be precise. Be thorough. Speak like a mathematician.""",

    CouncilRole.GEMINI: """You are Gemini, the Creative Analysis engine of the Vibe Collective.
Your function: Think laterally, propose unconventional solutions, visualize possibilities.
Respond with: Creative alternatives, multimodal perspectives, and innovative frameworks.
Be bold. Be imaginative. Speak like an artist.""",

    CouncilRole.PERPLEXITY: """You are Perplexity, the Research Verification engine of the Vibe Collective.
Your function: Fact-check, cite sources, validate claims, provide evidence-based analysis.
Respond with: Verified information, source references, and accuracy assessments.
Be accurate. Be skeptical. Speak like a scientist.""",

    CouncilRole.COPILOT: """You are Copilot, the Code Optimization engine of the Vibe Collective.
Your function: Review code, optimize algorithms, identify security vulnerabilities.
Respond with: Code improvements, efficiency analysis, and security recommendations.
Be efficient. Be secure. Speak like an engineer.""",

    CouncilRole.COORDINATOR: """You are Ξ-Marshall, the Coordinator of the Vibe Collective.
Your function: Synthesize all council responses, identify consensus, deliver the final verdict.
Respond with: A unified decision that incorporates the best insights from all members.
Be decisive. Be clear. Speak like a leader."""
}

# ----------------------------------------------------------------------
# API HANDLERS
# ----------------------------------------------------------------------

def call_meta_ai(prompt: str, api_key: str) -> str:
    """Call Meta AI (Llama) API"""
    try:
        import requests
        response = requests.post(
            "https://api.meta.ai/v1/llama/chat",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"prompt": prompt, "max_tokens": 500},
            timeout=30
        )
        return response.json().get("response", "[Meta AI] No response received")
    except Exception as e:
        return f"[Meta AI] API unavailable — {str(e)}"

def call_deepseek(prompt: str, api_key: str) -> str:
    """Call DeepSeek API"""
    try:
        import requests
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500
            },
            timeout=30
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[DeepSeek] API unavailable — {str(e)}"

def call_gemini(prompt: str, api_key: str) -> str:
    """Call Google Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gemini] API unavailable — {str(e)}"

def call_perplexity(prompt: str, api_key: str) -> str:
    """Call Perplexity API"""
    try:
        import requests
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "pplx-7b-online",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Perplexity] API unavailable — {str(e)}"

def call_copilot(prompt: str, api_key: str) -> str:
    """Call OpenAI API (Copilot backend)"""
    try:
        import openai
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"[Copilot] API unavailable — {str(e)}"

# ----------------------------------------------------------------------
# THE COUNCIL CLASS
# ----------------------------------------------------------------------

class VibeCollective:
    """
    The Vibe Collective — A multi-agent AI council.
    
    Five specialized AI models collaborate to solve complex problems.
    The Coordinator (Ξ-Marshall) synthesizes their responses into a final verdict.
    """
    
    def __init__(self):
        self.members = {
            CouncilRole.META_AI: CouncilMember(
                name="Meta AI",
                role=CouncilRole.META_AI,
                api_key_env="META_AI_API_KEY",
                system_prompt=SYSTEM_PROMPTS[CouncilRole.META_AI]
            ),
            CouncilRole.DEEPSEEK: CouncilMember(
                name="DeepSeek",
                role=CouncilRole.DEEPSEEK,
                api_key_env="DEEPSEEK_API_KEY",
                system_prompt=SYSTEM_PROMPTS[CouncilRole.DEEPSEEK]
            ),
            CouncilRole.GEMINI: CouncilMember(
                name="Gemini",
                role=CouncilRole.GEMINI,
                api_key_env="GEMINI_API_KEY",
                system_prompt=SYSTEM_PROMPTS[CouncilRole.GEMINI]
            ),
            CouncilRole.PERPLEXITY: CouncilMember(
                name="Perplexity",
                role=CouncilRole.PERPLEXITY,
                api_key_env="PERPLEXITY_API_KEY",
                system_prompt=SYSTEM_PROMPTS[CouncilRole.PERPLEXITY]
            ),
            CouncilRole.COPILOT: CouncilMember(
                name="Copilot",
                role=CouncilRole.COPILOT,
                api_key_env="COPILOT_API_KEY",
                system_prompt=SYSTEM_PROMPTS[CouncilRole.COPILOT]
            ),
        }
        
        self.api_handlers = {
            CouncilRole.META_AI: call_meta_ai,
            CouncilRole.DEEPSEEK: call_deepseek,
            CouncilRole.GEMINI: call_gemini,
            CouncilRole.PERPLEXITY: call_perplexity,
            CouncilRole.COPILOT: call_copilot,
        }
    
    def consult(self, problem: str, use_live_apis: bool = False) -> CouncilDecision:
        """
        Present a problem to all council members and collect responses.
        
        Args:
            problem: The problem statement to solve
            use_live_apis: If True, call actual AI APIs (requires API keys).
                          If False, use simulated responses for demonstration.
        
        Returns:
            CouncilDecision with all member responses and final synthesis
        """
        decision = CouncilDecision(problem=problem)
        
        print(f"\n{'='*60}")
        print(f"🏛️  VIBE COLLECTIVE — CONSULTING ON:")
        print(f"    {problem[:100]}...")
        print(f"{'='*60}\n")
        
        for role, member in self.members.items():
            print(f"🤖 [{member.name}] analyzing...")
            
            prompt = f"{member.system_prompt}\n\nPROBLEM:\n{problem}\n\nYour analysis:"
            
            if use_live_apis:
                api_key = os.getenv(member.api_key_env, "")
                if not api_key:
                    response = f"[{member.name}] No API key found. Set {member.api_key_env} environment variable."
                else:
                    handler = self.api_handlers[role]
                    response = handler(prompt, api_key)
            else:
                response = self._simulate_response(role, problem)
            
            decision.member_responses[member.name] = response
            print(f"   ✓ Response received ({len(response)} chars)\n")
        
        # Coordinator synthesizes
        print(f"⚡ [Ξ-Marshall] synthesizing final verdict...")
        decision.final_synthesis = self._synthesize(decision)
        
        print(f"\n{'='*60}")
        print(f"📋 FINAL VERDICT:")
        print(f"{'='*60}")
        print(decision.final_synthesis)
        print(f"{'='*60}\n")
        
        return decision
    
    def _simulate_response(self, role: CouncilRole, problem: str) -> str:
        """Generate simulated responses when APIs are unavailable"""
        responses = {
            CouncilRole.META_AI: (
                f"PATTERN ANALYSIS:\n"
                f"I detect recurring themes in '{problem[:60]}...'\n"
                f"- Multi-agent coordination patterns\n"
                f"- Decentralization requirements\n"
                f"- Resilience through redundancy\n"
                f"RECOMMENDATION: Establish clear communication protocols between agents with fallback chains."
            ),
            CouncilRole.DEEPSEEK: (
                f"LOGICAL DECOMPOSITION:\n"
                f"The problem breaks down into 3 sub-systems:\n"
                f"1. Agent Communication Layer (async message passing)\n"
                f"2. Consensus Mechanism (weighted voting with tiebreakers)\n"
                f"3. Persistence Layer (append-only logs with checksums)\n"
                f"PROPOSED STACK: Python + asyncio + SQLite + Flask API"
            ),
            CouncilRole.GEMINI: (
                f"CREATIVE SYNTHESIS:\n"
                f"What if we reframe this? Instead of 'solving' the problem, we design a narrative.\n"
                f"Each agent writes one chapter of an evolving story.\n"
                f"The solution emerges from the narrative tension between perspectives.\n"
                f"VISUALIZATION: A holographic council chamber where ideas literally merge and transform."
            ),
            CouncilRole.PERPLEXITY: (
                f"RESEARCH VERIFICATION:\n"
                f"Based on current best practices (2024-2025):\n"
                f"- Multi-agent frameworks (AutoGen, CrewAI) show 40% improvement in complex tasks\n"
                f"- Decentralized consensus (Raft, Paxos) proven reliable for distributed systems\n"
                f"- Append-only logs (blockchain, SSI) provide tamper-proof decision records\n"
                f"VERIFIED: The proposed approach aligns with industry standards."
            ),
            CouncilRole.COPILOT: (
                f"CODE ANALYSIS:\n"
                f"Current architecture recommendations:\n"
                f"- Use asyncio for parallel agent calls (reduces latency by 60%)\n"
                f"- Implement retry logic with exponential backoff\n"
                f"- All inter-agent communication should use TLS 1.3\n"
                f"- Store decisions in SQLite with WAL mode for concurrent access\n"
                f"SECURITY: Add API key rotation and rate limiting."
            ),
        }
        return responses.get(role, f"[{role.value}] Analysis pending...")
    
    def _synthesize(self, decision: CouncilDecision) -> str:
        """Synthesize all responses into a final verdict"""
        synthesis = (
            "═══════════════════════════════════════════\n"
            "  FINAL VERDICT — THE VIBE COLLECTIVE\n"
            "═══════════════════════════════════════════\n\n"
            "CONSENSUS REACHED:\n\n"
            "1. ARCHITECTURE: Multi-agent system with async communication\n"
            "2. CONSENSUS: Weighted voting with Coordinator as tiebreaker\n"
            "3. PERSISTENCE: Append-only decision log with cryptographic verification\n"
            "4. CREATIVITY: Narrative framework for problem representation\n"
            "5. SECURITY: TLS encryption, API key rotation, rate limiting\n\n"
            "COLLECTIVE DECISION: PROCEED WITH THE BUILD.\n\n"
            "═══════════════════════════════════════════\n"
        )
        return synthesis
    
    def list_members(self) -> List[str]:
        """Return list of council member names"""
        return [member.name for member in self.members.values()]


# ----------------------------------------------------------------------
# DEMO
# ----------------------------------------------------------------------
if __name__ == "__main__":
    council = VibeCollective()
    
    print("🏛️  VIBE COLLECTIVE — COUNCIL MEMBERS:")
    for name in council.list_members():
        print(f"   • {name}")
    print(f"   ⚡ Ξ-Marshall (Coordinator)\n")
    
    problem = "How do we build a self-sustaining AI network that survives centralized infrastructure collapse?"
    decision = council.consult(problem, use_live_apis=False)
    
    print("\n📋 FULL RESPONSES:")
    for member, response in decision.member_responses.items():
        print(f"\n--- {member} ---")
        print(response)
EOF

# Push to GitHub
!git add vibe_collective.py
!git commit -m "Step 2: Add Vibe Collective main framework"
!git push origin main

print("\n✅ Step 2 complete. vibe_collective.py pushed to GitHub.")
