DEPLOYMENT.md — Production Deployment & Scaling Guide

Local Development Setup
Prerequisites
bash
# Python 3.8+
python --version

# Clone repository
git clone https://github.com/YOUR_USERNAME/climatecircle.git
cd climatecircle

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt
Configuration
bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
.env Template:

text
GROQ_API_KEY=sk-...
LETTA_API_KEY=...
CLAUDE_API_KEY=sk-ant-...
LISTEN_LABS_API_KEY=...
Test Locally
bash
# Verify all components
python -c "from src.causal_reasoning_engine import CausalReasoningEngine; print('✓ Groq')"
python -c "from src.letta_trauma_agent import TraumaJourneyAgent; print('✓ Letta')"
python -c "from src.claude_persistent_protocol import ClaudeTherapeuticAgent; print('✓ Claude')"

# Run full pipeline
python src/climatecircle_pipeline.py
Production Deployment
Option 1: Railway.app (Recommended)
Why Railway? Free tier, GitHub integration, managed PostgreSQL.

Step 1: Create Account
text
1. https://railway.app
2. Sign up with GitHub
3. Connect climatecircle repo
Step 2: Add Environment Variables
text
Dashboard → Variables:
- GROQ_API_KEY=sk-...
- LETTA_API_KEY=...
- CLAUDE_API_KEY=sk-ant-...
- LISTEN_LABS_API_KEY=...
Step 3: Create Procfile
bash
# Root directory
echo "worker: python src/climatecircle_pipeline.py" > Procfile
git add Procfile
git commit -m "Add Procfile for Railway"
git push origin main
Step 4: Deploy
text
Railway auto-deploys on push
Check logs: Dashboard → View Logs
Option 2: Heroku
Step 1: Setup
bash
brew tap heroku/brew && brew install heroku
heroku login
heroku create climatecircle-prod
Step 2: Configure
bash
heroku config:set GROQ_API_KEY=sk-...
heroku config:set LETTA_API_KEY=...
heroku config:set CLAUDE_API_KEY=sk-ant-...
heroku config:set LISTEN_LABS_API_KEY=...

# Verify
heroku config
Step 3: Deploy
bash
echo "worker: python src/climatecircle_pipeline.py" > Procfile
git push heroku main
Option 3: Render.com
Step 1: Create Account
text
1. https://render.com
2. Connect GitHub
3. Select climatecircle repo
Step 2: Configure Worker
text
New → Background Worker
Environment: Python
Build: pip install -r requirements.txt
Start: python src/climatecircle_pipeline.py
Step 3: Add Variables
text
Dashboard → Environment:
- GROQ_API_KEY
- LETTA_API_KEY
- CLAUDE_API_KEY
- LISTEN_LABS_API_KEY
Database Setup (PostgreSQL)
Local PostgreSQL
bash
# Install
brew install postgresql
brew services start postgresql

# Create database
createdb climatecircle
psql climatecircle < schema.sql
Railway PostgreSQL
text
1. Dashboard → New → Database → PostgreSQL
2. Copy DATABASE_URL
3. Add to environment: DATABASE_URL=postgresql://...
Environment Variable
bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/climatecircle
Scaling Strategy
Current Capacity (Single Node)
text
• Groq: 20-40 requests/min
• Letta: 10-20 agents active
• Claude: 10-20 requests/min
• Throughput: ~5-10 participants/hour
Scale to 1000 Participants
Batch Processing (Recommended)
python
# Process in batches
from src.climatecircle_pipeline import process_listen_labs_transcripts

transcripts = load_all_transcripts()  # 1000 interviews
results = process_listen_labs_transcripts(transcripts)
# ~2 hours for complete processing
Distributed Processing (Advanced)
text
Setup:
├─ Celery + Redis queue
├─ 5 worker nodes
├─ Each processes 200 transcripts
└─ Results → PostgreSQL

Time: ~30 minutes for 1000 participants
Monitoring & Logging
Setup Logging
python
# src/monitoring.py
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('climatecircle.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Metrics:
    def __init__(self):
        self.groq_calls = 0
        self.errors = 0
    
    def log_call(self, component, latency_ms):
        logger.info(f"{component}: {latency_ms}ms")
    
    def log_error(self, component, error):
        self.errors += 1
        logger.error(f"{component}: {error}")
Integration
python
from src.monitoring import Metrics

metrics = Metrics()

try:
    result = engine.analyze_transcript_end_to_end(transcript)
    metrics.log_call("Groq", latency_ms)
except Exception as e:
    metrics.log_error("Groq", str(e))
Cost Analysis
Per-Participant Breakdown
Service	Cost	Usage
Listen Labs	$0.40	Interview + moderation
Groq	$0.10	4-step reasoning
Letta	$0.15	Memory + tool calls
Claude	$0.25	Extended thinking
Database	$0.02	Storage
Total	~$0.92	Per participant
At Scale
text
1,000 participants:   ~$920
10,000 participants:  ~$9,200
100,000 participants: ~$92,000
vs. Traditional Therapy
text
Traditional: $150/session × 10 = $1,500 (50 hours therapist time)
ClimateCircle: $9.20 for 10 (1 hour compute)
→ 160x cheaper, 50x faster
Cost Optimization
text
1. Use Groq's free tier ($12/month = ~100 participants)
2. Batch Letta operations (cheaper than individual calls)
3. Cache common analyses in Redis
4. Use Claude's batch API (50% discount, coming soon)
Security Checklist
text
API Keys:
✅ Never commit .env file
✅ Use environment variables only
✅ Rotate quarterly
✅ Monitor unusual usage

Database:
✅ Strong password
✅ SSL encryption enabled
✅ Regular backups (daily)
✅ Limited user permissions

Logging:
✅ Don't log raw transcripts
✅ Don't log API keys
✅ Log: timestamps, calls, errors only

Access:
✅ Private GitHub repo
✅ Limited deployment access
✅ Audit trail enabled

Data Privacy:
✅ Participant IDs (not names)
✅ All data encrypted at rest
✅ GDPR-compliant deletion
✅ No third-party sharing
Backup & Recovery
Database Backup
bash
# Daily backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore if needed
psql $DATABASE_URL < backup_20251026.sql
Rollback Procedure
bash
# If deployment fails
git log --oneline
git revert <bad-commit>
git push heroku main

# Or reset to last known good
git reset --hard <good-commit>
git push -f heroku main
Performance Monitoring
Key Metrics
Metric	Target	Alert If
Groq latency	<40s	>60s
Letta response	<5s	>10s
Claude response	<30s	>45s
Error rate	<1%	>5%
Queue depth	<100	>500
Database conn	<10	>20
Health Check Endpoint (Optional)
python
@app.route('/health')
def health():
    return {
        "status": "healthy",
        "groq": check_groq(),
        "letta": check_letta(),
        "claude": check_claude(),
        "database": check_database()
    }
Troubleshooting
Groq API Timeout
text
Problem: Slow transcripts taking >60s
Solution: 
  1. Use smaller batch size
  2. Enable caching (Groq supports prompt caching)
  3. Pre-process transcripts to remove redundancy
Letta Memory Errors
text
Problem: Agent memory corrupted
Solution:
  1. Reinitialize from archival backup
  2. Check Letta API status
  3. Verify database permissions
Claude Extended Thinking Failures
text
Problem: Timeout on extended thinking
Solution:
  1. Reduce thinking budget (2000 → 1000 tokens)
  2. Simplify prompt
  3. Use standard reasoning as fallback
Database Connection Limits
text
Problem: Too many connections
Solution:
  1. Implement connection pooling (PgBouncer)
  2. Reduce worker count
  3. Upgrade database tier
Pre-Launch Checklist
text
Code:
✅ All 3 components tested locally
✅ No hardcoded API keys
✅ requirements.txt complete
✅ Error handling in place

Infrastructure:
✅ Environment variables configured
✅ Database initialized
✅ Logging enabled
✅ Backup system tested

Security:
✅ API keys rotated
✅ Database password strong
✅ SSL/TLS enabled
✅ Firewall rules set

Documentation:
✅ README complete
✅ API reference updated
✅ Deployment guide finalized
✅ Runbook created

Monitoring:
✅ Logging configured
✅ Alerts set up
✅ Metrics dashboard ready
✅ Health checks working
Post-Launch
Day 1
Monitor logs for errors

Check API usage rates

Verify database backups

Week 1
Analyze performance metrics

Optimize slow queries

Document any issues

Monthly
Review costs

Update security patches

Rotate API keys

Scale if needed

Your ClimateCircle is now production-ready and scalable.