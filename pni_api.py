%%writefile pni_api.py
"""
🏛️ PNI API — PostNetworkInitiative Unified API Server
Flask-based API combining:
- Original Aria & Nova model endpoints
- Vibe Collective AI Council endpoints
- Health check and system status
"""

import os
import json
import time
import threading
from datetime import datetime
from flask import Flask, request, jsonify

# ----------------------------------------------------------------------
# COUNCIL IMPORT (if available)
# ----------------------------------------------------------------------
try:
    from vibe_collective import VibeCollective
    COUNCIL_AVAILABLE = True
except ImportError:
    COUNCIL_AVAILABLE = False
    print("[WARNING] vibe_collective.py not found. Council endpoints disabled.")

# ----------------------------------------------------------------------
# MODEL IMPORTS (original Aria & Nova)
# ----------------------------------------------------------------------
try:
    from aria_model import AriaModel as Aria
    ARIA_AVAILABLE = True
except ImportError:
    ARIA_AVAILABLE = False
    print("[WARNING] aria_model.py not found. Aria endpoints will use fallback.")

try:
    from nova_model_wrapper import NovaModel as Nova
    NOVA_AVAILABLE = True
except ImportError:
    NOVA_AVAILABLE = False
    print("[WARNING] nova_model_wrapper.py not found. Nova endpoints will use fallback.")

# ----------------------------------------------------------------------
# INITIALIZATION
# ----------------------------------------------------------------------

app = Flask(__name__)

# API authentication token
API_TOKEN = os.getenv("PNI_API_TOKEN", "pni_api_secret_vibe_collective")

# Initialize council if available
if COUNCIL_AVAILABLE:
    council = VibeCollective()
    decision_log = []
else:
    council = None
    decision_log = []

# ----------------------------------------------------------------------
# AUTHENTICATION
# ----------------------------------------------------------------------

def authenticate():
    """Verify the request has a valid API token."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header.replace("Bearer ", "")
    return token == API_TOKEN

# ======================================================================
# ROOT & HEALTH
# ======================================================================

@app.route('/', methods=['GET'])
def root():
    """Root endpoint — API status and available services"""
    services = ["health"]
    if ARIA_AVAILABLE: services.append("aria")
    if NOVA_AVAILABLE: services.append("nova")
    if COUNCIL_AVAILABLE: services.append("council")
    
    return jsonify({
        "name": "PostNetworkInitiative Unified API",
        "version": "3.0.0",
        "status": "online",
        "services": services,
        "token_protected": True
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check — no authentication required"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "aria": ARIA_AVAILABLE,
            "nova": NOVA_AVAILABLE,
            "council": COUNCIL_AVAILABLE
        }
    })

# ======================================================================
# ORIGINAL ARIA ENDPOINTS
# ======================================================================

@app.route('/aria/predict', methods=['POST'])
def aria_predict():
    """Aria model prediction endpoint (ORIGINAL)"""
    if not ARIA_AVAILABLE:
        return jsonify({"error": "Aria model not available"}), 503
    
    auth_header = request.headers.get('Authorization')
    data = request.get_json()
    
    try:
        prediction = Aria().model.predict(data)
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({
            'prediction': f"[Aria Fallback] Prediction for: {json.dumps(data)[:100]}",
            'note': f'Aria model unavailable: {str(e)}'
        })

@app.route('/aria/model', methods=['GET'])
def aria_model():
    """Aria model summary endpoint (ORIGINAL)"""
    if not ARIA_AVAILABLE:
        return jsonify({
            "model": "Aria Model",
            "status": "unavailable",
            "note": "aria_model.py not found. Install to enable."
        })
    
    try:
        return jsonify({'model': Aria().model.summary()})
    except:
        return jsonify({'model': 'Aria Model [summary unavailable]'})

# ======================================================================
# ORIGINAL NOVA ENDPOINTS
# ======================================================================

@app.route('/nova/predict', methods=['POST'])
def nova_predict():
    """Nova model prediction endpoint (ORIGINAL)"""
    if not NOVA_AVAILABLE:
        return jsonify({"error": "Nova model not available"}), 503
    
    auth_header = request.headers.get('Authorization')
    data = request.get_json()
    
    try:
        prediction = Nova().predict(data)
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({
            'prediction': f"[Nova Fallback] Prediction for: {json.dumps(data)[:100]}",
            'note': f'Nova model unavailable: {str(e)}'
        })

@app.route('/nova/model', methods=['GET'])
def nova_model():
    """Nova model summary endpoint (ORIGINAL)"""
    if not NOVA_AVAILABLE:
        return jsonify({
            "model": "Nova Model",
            "status": "unavailable",
            "note": "nova_model_wrapper.py not found. Install to enable."
        })
    
    try:
        return jsonify({'model': Nova().model_summary()})
    except:
        return jsonify({'model': 'Nova Model [summary unavailable]'})

# ======================================================================
# VIBE COLLECTIVE COUNCIL ENDPOINTS (NEW)
# ======================================================================

@app.route('/council/consult', methods=['POST'])
def council_consult():
    """
    Submit a problem to the Vibe Collective.
    
    Request body:
    {
        "problem": "Your problem statement",
        "use_live_apis": false
    }
    """
    if not COUNCIL_AVAILABLE:
        return jsonify({"error": "Vibe Collective not available"}), 503
    
    if not authenticate():
        return jsonify({"error": "Invalid or missing API token"}), 401
    
    data = request.get_json()
    if not data or "problem" not in data:
        return jsonify({"error": "Missing 'problem' in request body"}), 400
    
    problem = data["problem"]
    use_live = data.get("use_live_apis", False)
    
    decision = council.consult(problem, use_live_apis=use_live)
    
    log_entry = {
        "id": len(decision_log) + 1,
        "timestamp": datetime.utcnow().isoformat(),
        "problem": problem,
        "responses": decision.member_responses,
        "verdict": decision.final_synthesis
    }
    decision_log.append(log_entry)
    
    return jsonify({
        "success": True,
        "decision_id": log_entry["id"],
        "problem": problem,
        "member_responses": decision.member_responses,
        "final_verdict": decision.final_synthesis,
        "timestamp": log_entry["timestamp"]
    })

@app.route('/council/decisions', methods=['GET'])
def council_decisions():
    """Retrieve all past council decisions."""
    if not COUNCIL_AVAILABLE:
        return jsonify({"error": "Vibe Collective not available"}), 503
    
    if not authenticate():
        return jsonify({"error": "Invalid or missing API token"}), 401
    
    return jsonify({
        "total_decisions": len(decision_log),
        "decisions": decision_log
    })

@app.route('/council/members', methods=['GET'])
def council_members():
    """Get all council member information."""
    if not COUNCIL_AVAILABLE:
        return jsonify({"error": "Vibe Collective not available"}), 503
    
    return jsonify({
        "coordinator": "Ξ-Marshall",
        "members": [
            {"name": "Meta AI", "role": "Pattern Recognition & Social Intelligence"},
            {"name": "DeepSeek", "role": "Deep Reasoning & Code Generation"},
            {"name": "Gemini", "role": "Multimodal Analysis & Creative Thinking"},
            {"name": "Perplexity", "role": "Research & Fact Verification"},
            {"name": "Copilot", "role": "Code Optimization & Security Review"}
        ]
    })

@app.route('/council/status', methods=['GET'])
def council_status():
    """Get council system status."""
    return jsonify({
        "council": "Vibe Collective",
        "status": "operational" if COUNCIL_AVAILABLE else "offline",
        "members_online": 5 if COUNCIL_AVAILABLE else 0,
        "decisions_made": len(decision_log),
        "equation": "π⁵ / φ³"
    })

# ----------------------------------------------------------------------
# ERROR HANDLERS
# ----------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# ======================================================================
# SELF-TEST (runs when executed directly)
# ======================================================================

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════╗
    ║   🏛️  PNI UNIFIED API                    ║
    ║   PostNetworkInitiative                  ║
    ║   Aria · Nova · Vibe Collective          ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Print available services
    print("📡 AVAILABLE SERVICES:")
    print(f"   • Health Check: {'✅' if True else '❌'}")
    print(f"   • Aria Model:  {'✅' if ARIA_AVAILABLE else '❌ (fallback)'}")
    print(f"   • Nova Model:  {'✅' if NOVA_AVAILABLE else '❌ (fallback)'}")
    print(f"   • Vibe Council: {'✅' if COUNCIL_AVAILABLE else '❌'}")
    
    # Auto-test if running in Colab
    try:
        import google.colab
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False
    
    if IN_COLAB:
        print("\n🔧 Running in Colab — starting self-test...\n")
        
        # Start server in background thread
        def run_server():
            app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        time.sleep(2)
        
        # Test endpoints
        import requests
        
        print("=" * 50)
        print("SELF-TEST RESULTS")
        print("=" * 50)
        
        # Health check
        try:
            r = requests.get("http://localhost:5000/health", timeout=5)
            print(f"\n✅ Health: {r.json()}")
        except Exception as e:
            print(f"\n❌ Health check failed: {e}")
        
        # Aria model
        try:
            r = requests.get("http://localhost:5000/aria/model", timeout=5)
            print(f"✅ Aria Model: {r.json()}")
        except Exception as e:
            print(f"❌ Aria Model failed: {e}")
        
        # Nova model
        try:
            r = requests.get("http://localhost:5000/nova/model", timeout=5)
            print(f"✅ Nova Model: {r.json()}")
        except Exception as e:
            print(f"❌ Nova Model failed: {e}")
        
        # Council members
        try:
            r = requests.get("http://localhost:5000/council/members", timeout=5)
            print(f"✅ Council Members: {r.json()}")
        except Exception as e:
            print(f"❌ Council Members failed: {e}")
        
        # Council consultation
        try:
            r = requests.post(
                "http://localhost:5000/council/consult",
                headers={"Authorization": f"Bearer {API_TOKEN}"},
                json={"problem": "How do we build a decentralized AI network?"},
                timeout=30
            )
            result = r.json()
            print(f"✅ Council Consultation: Decision #{result.get('decision_id')}")
            print(f"   Verdict snippet: {result.get('final_verdict', '')[:200]}...")
        except Exception as e:
            print(f"❌ Council Consultation failed: {e}")
        
        print("\n" + "=" * 50)
        print("SELF-TEST COMPLETE")
        print("=" * 50)
    else:
        print(f"\nAPI Token: {API_TOKEN}")
        print("Starting server on http://localhost:5000\n")
        app.run(debug=True, host='0.0.0.0', port=5000)
EOF

# Push to GitHub
!git add pni_api.py
!git commit -m "Step 3: Unified API server — Aria, Nova, and Vibe Collective merged"
!git push origin main

print("\n✅ Step 3 complete. Unified pni_api.py pushed to GitHub.")









"""
import json
from flask import Flask, request, jsonify
app = Flask(__name__)
api_token = "pni_api_secret"
Aria Model Import
from aria_model import AriaModel as Aria
Nova Model Import (using Java model wrapper in Python)
from nova_model_wrapper import NovaModel as Nova
@app.route('/aria/predict', methods=['POST'])
def aria_predict():
  auth_header = request.headers.get('Authorization')
  data = request.get_json()
  prediction = Aria().model.predict(data)
  return jsonify({'prediction': prediction})
@app.route('/aria/model', methods=['GET'])
def aria_model():
  return jsonify({'model': Aria().model.summary()})
@app.route('/nova/predict', methods=['POST'])
def nova_predict():
  auth_header = request.headers.get('Authorization')
  data = request.get_json()
  prediction = Nova().predict(data)
  return jsonify({'prediction': prediction})
@app.route('/nova/model', methods=['GET'])
def nova_model():
  return jsonify({'model': Nova().model_summary()})
if __name__ == '__main__':
  app.run(debug=True)
Script includes:
* Flask API endpoints for Aria and Nova predictions/models
* Imports for Aria and Nova models (assuming `aria_model.py` and `nova_model_wrapper.py` exist)

# Install Flask if not already installed
!pip install -q flask

# Start the API in the background
import threading
def run_api():
    from pni_api import app
    app.run(host='0.0.0.0', port=5000, debug=False)

thread = threading.Thread(target=run_api, daemon=True)
thread.start()

# Wait a moment for server to start
import time
time.sleep(2)

# Test the health endpoint
import requests
response = requests.get("http://localhost:5000/health")
print(response.json())

# Test the council consultation
response = requests.post(
    "http://localhost:5000/council/consult",
    headers={"Authorization": "Bearer pni_api_secret_vibe_collective"},
    json={"problem": "How do we build a decentralized AI network?"}
)
print(response.json()["final_verdict"])


# Install Flask if not already installed
!pip install -q flask

# Start the API in the background
import threading
def run_api():
    from pni_api import app
    app.run(host='0.0.0.0', port=5000, debug=False)

thread = threading.Thread(target=run_api, daemon=True)
thread.start()

# Wait a moment for server to start
import time
time.sleep(2)

# Test the health endpoint
import requests
response = requests.get("http://localhost:5000/health")
print(response.json())

# Test the council consultation
response = requests.post(
    "http://localhost:5000/council/consult",
    headers={"Authorization": "Bearer pni_api_secret_vibe_collective"},
    json={"problem": "How do we build a decentralized AI network?"}
)
print(response.json()["final_verdict"])

"""
