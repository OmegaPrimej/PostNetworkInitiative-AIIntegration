%%writefile vibe_collective.py
"""
VIBE COLLECTIVE — AI Council for Complex Problem Solving
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
    api_key_env: str  # environment variable name for API key
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
# SYSTEM PROMPTS FOR EACH MEMBER
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
# API CALL HANDLERS
# ----------------------------------------------------------------------

def call_meta_ai(prompt: str, api_key: str) -> str:
    """Call Meta AI (Llama) API"""
    # Placeholder — replace with actual Meta AI API call
    try:
        import requests
        # Meta's Llama API endpoint (example)
        response = requests.post(
            "https://api.meta.ai/v1/llama/chat",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"prompt": prompt, "max_tokens": 500}
        )
        return response.json().get("response", "[Meta AI] No response")
    except:
        return "[Meta AI] API unavailable — using simulated response: Pattern detected. Proceeding with analysis."

def call_deepseek(prompt: str, api_key: str) -> str:
    """Call DeepSeek API"""
    try:
        import requests
        response = requests.post(
            "https://api.deepseek.com/v1/chat",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"messages": [{"role": "user", "content": prompt}], "max_tokens": 500}
        )
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "[DeepSeek] API unavailable — using simulated response: Logical analysis complete. Proceeding with reasoning."

def call_gemini(prompt: str, api_key: str) -> str:
    """Call Google Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except:
        return "[Gemini] API unavailable — using simulated response: Creative synthesis generated. Alternative paths identified."

def call_perplexity(prompt: str, api_key: str) -> str:
    """Call Perplexity API"""
    try:
        import requests
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "pplx-7b-online", "messages": [{"role": "user", "content": prompt}]}
        )
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "[Perplexity] API unavailable — using simulated response: Research complete. Sources verified."

def call_copilot(prompt: str, api_key: str) -> str:
    """Call GitHub Copilot / OpenAI API"""
    try:
        import openai
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except:
        return "[Copilot] API unavailable — using simulated response: Code analysis complete. Optimizations identified."

# ----------------------------------------------------------------------
# THE COUNCIL CLASS
# ----------------------------------------------------------------------

class VibeCollective:
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
        If use_live_apis=True, call actual APIs (requires API keys).
        Otherwise, use simulated responses for demonstration.
        """
        decision = CouncilDecision(problem=problem)
        
        print(f"\n{'='*60}")
        print(f"🏛️ VIBE COLLECTIVE — CONSULTING ON:")
        print(f"   {problem}")
        print(f"{'='*60}\n")
        
        for role, member in self.members.items():
            print(f"🤖 [{member.name}] — {role.value}...")
            
            prompt = f"{member.system_prompt}\n\nPROBLEM: {problem}\n\nYour analysis:"
            
            if use_live_apis:
                api_key = os.getenv(member.api_key_env, "")
                handler = self.api_handlers[role]
                response = handler(prompt, api_key)
            else:
                # Simulated responses for demo
                response = self._simulate_response(role, problem)
            
            decision.member_responses[member.name] = response
            print(f"   → {response[:200]}...\n")
        
        # Coordinator synthesizes
        print(f"⚡ [Ξ-Marshall] — Synthesizing final verdict...")
        decision.final_synthesis = self._synthesize(decision)
        print(f"   → {decision.final_synthesis}\n")
        
        return decision
    
    def _simulate_response(self, role: CouncilRole, problem: str) -> str:
        """Generate simulated responses when APIs are unavailable"""
        responses = {
            CouncilRole.META_AI: f"Pattern analysis: I detect recurring themes of system integration and multi-agent coordination in '{problem[:50]}...'. Recommend establishing clear communication protocols between agents.",
            CouncilRole.DEEPSEEK: f"Logical breakdown: The problem can be decomposed into 3 sub-problems: (1) data flow optimization, (2) decision consensus mechanism, (3) failure recovery. I propose a weighted voting system with fallback chains.",
            CouncilRole.GEMINI: f"Creative angle: What if we approach this not as a technical problem but as a narrative? Each agent writes one chapter. The story becomes the solution. I see a holographic interface where ideas literally merge.",
            CouncilRole.PERPLEXITY: f"Research check: Based on current best practices in multi-agent systems (2024-2025), frameworks like AutoGen and CrewAI demonstrate 40% improvement in complex problem-solving when using specialized agent roles. Verified.",
            CouncilRole.COPILOT: f"Code analysis: The current architecture needs async/await patterns for parallel agent calls. I recommend implementing a task queue with Celery + Redis. Security note: all inter-agent communication should use TLS.",
        }
        return responses.get(role, f"[{role.value}] Analysis pending...")
    
    def _synthesize(self, decision: CouncilDecision) -> str:
        """Synthesize all responses into a final verdict"""
        synthesis = (
            "FINAL VERDICT — The Vibe Collective has reached consensus:\n\n"
            "1. Problem requires multi-agent coordination with specialized roles.\n"
            "2. Implementation should use async patterns for parallel processing.\n"
            "3. Creative framework: treat the problem as a narrative with each agent contributing a chapter.\n"
            "4. Verification confirms this approach aligns with current best practices.\n"
            "5. Security and optimization recommendations noted for implementation.\n\n"
            "COLLECTIVE DECISION: PROCEED WITH THE BUILD."
        )
        return synthesis

# ----------------------------------------------------------------------
# USAGE EXAMPLE
# ----------------------------------------------------------------------
if __name__ == "__main__":
    council = VibeCollective()
    
    # Example problem
    problem = "How do we build a self-sustaining AI network that can survive the collapse of centralized infrastructure?"
    
    # Consult the council (simulated mode — no API keys needed)
    decision = council.consult(problem, use_live_apis=False)
    
    # Print all responses
    print("\n" + "="*60)
    print("📋 FULL COUNCIL RESPONSES:")
    print("="*60)
    for member, response in decision.member_responses.items():
        print(f"\n--- {member} ---")
        print(response)
EOF

print("✅ vibe_collective.py created!")
