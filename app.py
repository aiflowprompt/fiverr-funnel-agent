import streamlit as st
import time
from agent import generate_batch, PLATFORM_SPECS

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fiverr Funnel Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e6f0;
}

h1, h2, h3, .big-title {
    font-family: 'Syne', sans-serif;
}

.main-header {
    text-align: center;
    padding: 2.5rem 0 1rem;
}

.main-header h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    background: linear-gradient(135deg, #a78bfa, #f472b6, #fb923c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}

.main-header p {
    color: #6b7280;
    font-size: 1rem;
}

.platform-card {
    background: #13131a;
    border: 1px solid #2a2a3a;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}

.platform-label {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

.fb-label   { color: #60a5fa; }
.ig-label   { color: #f472b6; }
.li-label   { color: #34d399; }
.tw-label   { color: #38bdf8; }
.tt-label   { color: #fb923c; }

div[data-testid="stTextArea"] textarea {
    background: #0d0d14 !important;
    border: 1px solid #2a2a3a !important;
    color: #e8e6f0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] select {
    background: #13131a !important;
    border: 1px solid #2a2a3a !important;
    color: #e8e6f0 !important;
    border-radius: 8px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #db2777) !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.88 !important;
}

.stDownloadButton > button {
    background: #1e1e2e !important;
    color: #a78bfa !important;
    border: 1px solid #3a3a5c !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 1rem !important;
}

.success-banner {
    background: linear-gradient(135deg, #064e3b22, #065f4622);
    border: 1px solid #065f46;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: #6ee7b7;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    text-align: center;
    margin: 1rem 0;
}

.stat-pill {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    font-size: 0.78rem;
    color: #a78bfa;
    margin: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🚀 Fiverr Funnel Agent</h1>
    <p>Generate a full social media batch in one click — Facebook · Instagram · LinkedIn · Twitter · TikTok</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Input Form ────────────────────────────────────────────────────────────────
with st.form("batch_form"):
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 🎯 Your Fiverr Details")
        niche = st.text_input(
            "Your Niche",
            placeholder="e.g. E-commerce brands, SaaS startups, real estate agents"
        )
        service = st.text_input(
            "Service You're Selling",
            placeholder="e.g. SEO blog writing, logo design, video editing"
        )
        fiverr_url = st.text_input(
            "Your Fiverr Profile URL",
            placeholder="https://www.fiverr.com/yourusername"
        )

    with col2:
        st.markdown("#### ✍️ Content Settings")
        tone = st.selectbox("Tone of Voice", [
            "Professional yet approachable",
            "Bold & authoritative",
            "Friendly & conversational",
            "Educational / value-first",
            "Witty & entertaining",
            "Inspiring & motivational"
        ])
        angle = st.text_area(
            "Content Angle / Topic (optional)",
            height=100,
            placeholder="e.g. '3 mistakes clients make without a professional writer'\nor leave blank for auto-generated angle"
        )

    submitted = st.form_submit_button("⚡ Generate All 5 Posts Now", use_container_width=True)

# ── Generation ────────────────────────────────────────────────────────────────
if submitted:
    if not niche.strip() or not service.strip() or not fiverr_url.strip():
        st.error("Please fill in Niche, Service, and your Fiverr URL.")
    else:
        progress_bar = st.progress(0, text="Starting generation...")
        platforms = list(PLATFORM_SPECS.keys())
        results = {}

        # Generate one platform at a time to show live progress
        from agent import generate_batch as _gen_batch
        # Use per-platform approach for progress UX
        from agent import web_search, SYSTEM, client, PLATFORM_SPECS as specs
        import httpx
        from groq import Groq as _Groq

        research = web_search(f"{niche} {service} tips trends")

        icons = {"facebook": "🔵", "instagram": "💜", "linkedin": "🟢", "twitter": "🔷", "tiktok": "🟠"}
        labels = {k: v["label"] for k, v in specs.items()}

        for i, platform in enumerate(platforms):
            spec = specs[platform]
            progress_bar.progress(
                int((i / len(platforms)) * 100),
                text=f"{icons[platform]} Writing {spec['label']}..."
            )

            prompt = f"""
Niche: {niche}
Service being sold: {service}
Fiverr profile URL: {fiverr_url}
Content angle / topic: {angle or f"Why clients need {service} for their {niche} business"}
Tone: {tone}
Platform: {spec['label']}
Target word count: {spec['words']} words
Platform-specific rules: {spec['notes']}
Research context: {research}

Write ONE {spec['label']} NOW. Follow all platform rules exactly.
Self-review for conversion power, score 0-10. If below 8, revise once.
Return ONLY the final post — no commentary, no labels, no meta text.
"""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024
            )
            results[platform] = response.choices[0].message.content.strip()

        progress_bar.progress(100, text="Done!")
        time.sleep(0.4)
        progress_bar.empty()

        st.markdown('<div class="success-banner">✅ All 5 posts generated — ready to copy & schedule!</div>', unsafe_allow_html=True)

        # ── Output Grid ───────────────────────────────────────────────────────
        st.markdown("### 📋 Your Content Batch")

        color_map = {
            "facebook": "fb-label",
            "instagram": "ig-label",
            "linkedin": "li-label",
            "twitter": "tw-label",
            "tiktok": "tt-label"
        }

        col_left, col_right = st.columns(2, gap="large")
        platform_list = list(results.items())

        for idx, (platform, content) in enumerate(platform_list):
            col = col_left if idx % 2 == 0 else col_right
            with col:
                spec = PLATFORM_SPECS[platform]
                label_class = color_map[platform]
                st.markdown(f"""
<div class="platform-card">
    <div class="platform-label {label_class}">{icons[platform]} {spec['label']}</div>
</div>
""", unsafe_allow_html=True)
                st.text_area(
                    label=spec["label"],
                    value=content,
                    height=220,
                    key=f"output_{platform}",
                    label_visibility="collapsed"
                )
                st.download_button(
                    label=f"⬇️ Download {spec['label']}",
                    data=content,
                    file_name=f"{platform}_post.txt",
                    mime="text/plain",
                    key=f"dl_{platform}"
                )

        # ── Download All ──────────────────────────────────────────────────────
        st.divider()
        all_content = "\n\n".join([
            f"{'='*60}\n{PLATFORM_SPECS[p]['label'].upper()}\n{'='*60}\n{c}"
            for p, c in results.items()
        ])
        all_content = f"FIVERR FUNNEL CONTENT BATCH\nNiche: {niche} | Service: {service}\n\n" + all_content

        st.download_button(
            label="📦 Download All Posts as .txt",
            data=all_content,
            file_name="fiverr_funnel_batch.txt",
            mime="text/plain",
            use_container_width=True
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center; color:#4a4a6a; font-size:0.78rem; padding:1rem 0;">
    Fiverr Funnel Agent · Powered by Groq + Llama 3.3 70B · Free to run on Render
</div>
""", unsafe_allow_html=True)
