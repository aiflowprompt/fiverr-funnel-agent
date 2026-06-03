# 🚀 Fiverr Funnel Agent

Generate a full social media content batch in one click.  
**Facebook · Instagram · LinkedIn · Twitter/X · TikTok Script** — all funnelling clients to your Fiverr profile.

**Stack:** Streamlit UI · FastAPI · Groq (Llama 3.3 70B) · Render (free hosting)  
**Cost:** $0/month

---

## ⚡ Deploy in Under 10 Minutes

### Step 1 — Get a Free Groq API Key (2 min)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up (free) → click **API Keys** → **Create API Key**
3. Copy the key — you'll need it in Step 4

---

### Step 2 — Push to GitHub (3 min)

1. Go to [https://github.com/new](https://github.com/new)
2. Create a new **public** repo named `fiverr-funnel-agent`
3. In your terminal, run:

```bash
cd fiverr-funnel-agent
git init
git add .
git commit -m "Initial deploy"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fiverr-funnel-agent.git
git push -u origin main
```

---

### Step 3 — Deploy on Render (3 min)

1. Go to [https://render.com](https://render.com) and sign up (free)
2. Click **New +** → **Web Service**
3. Connect your GitHub account → select `fiverr-funnel-agent`
4. Render auto-detects `render.yaml` — confirm these settings:
   - **Name:** `fiverr-funnel-agent`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `bash start.sh`
5. Click **Advanced** → **Add Environment Variable**:
   - Key: `GROQ_API_KEY`
   - Value: *(paste your Groq key from Step 1)*
6. Click **Create Web Service**

Render builds and deploys in ~2 minutes. You'll get a live URL like:  
`https://fiverr-funnel-agent.onrender.com`

---

## 🎯 How to Use It

1. Open your live Render URL
2. Fill in:
   - **Your Niche** (e.g. "E-commerce brands")
   - **Service You're Selling** (e.g. "SEO blog writing")
   - **Your Fiverr Profile URL**
3. Pick a tone, optionally add a content angle
4. Click **⚡ Generate All 5 Posts Now**
5. Copy each post or download all as `.txt`

---

## 📦 File Structure

```
fiverr-funnel-agent/
├── agent.py          # AI generation logic (Groq + Llama 3.3)
├── app.py            # Streamlit web UI
├── api.py            # FastAPI REST endpoint
├── start.sh          # Starts both servers
├── render.yaml       # Render deployment config
├── requirements.txt  # Python dependencies
└── .gitignore
```

---

## 🔌 API Usage (Optional)

POST to `/generate-batch`:

```json
{
  "niche": "E-commerce brands",
  "service": "SEO blog writing",
  "fiverr_url": "https://www.fiverr.com/yourprofile",
  "tone": "Professional yet approachable",
  "angle": "Why brands lose sales without good content"
}
```

Returns all 5 posts in a JSON object.

---

## 💡 Tips for Maximum Conversions

- Run a new batch **every 2–3 days** per niche
- Post TikTok scripts first — video converts fastest
- On LinkedIn, post between **8–9am Tuesday–Thursday**
- On Instagram, post **Reels** using the TikTok script
- Pin your best-performing Facebook post and boost for $1/day
