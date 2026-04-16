import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import pandas as pd

st.set_page_config(page_title="AI SEO Assistant", layout="wide")

st.title("🚀 AI SEO Assistant Dashboard")

url = st.text_input("Enter Your Website URL")
competitor_url = st.text_input("Enter Competitor URL (Optional)")

# ---------------- SEO ANALYSIS ---------------- #
def analyze_site(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else ""
    
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content")

    h1 = [h.text.strip() for h in soup.find_all("h1")]
    h2 = [h.text.strip() for h in soup.find_all("h2")]

    images = soup.find_all("img")
    missing_alt = [img for img in images if not img.get("alt")]

    text = soup.get_text().lower()
    words = re.findall(r'\b\w+\b', text)
    keywords = Counter(words).most_common(10)

    score = 100
    if not title: score -= 20
    if not meta_desc: score -= 20
    if len(h1) == 0: score -= 20
    if len(missing_alt) > 0: score -= 10

    return {
        "title": title,
        "meta": meta_desc,
        "h1": h1,
        "h2": h2,
        "missing_alt": len(missing_alt),
        "keywords": keywords,
        "score": score
    }

# ---------------- AI INSIGHTS ---------------- #
def generate_ai_insights(data):
    insights = []

    if data["score"] > 80:
        insights.append("Your website has strong SEO fundamentals but can be optimized further.")
    elif data["score"] > 50:
        insights.append("Your SEO is moderate. Focus on improving structure and metadata.")
    else:
        insights.append("Your SEO is weak. Immediate improvements are required.")

    if not data["title"]:
        insights.append("Missing title tag is hurting your search visibility.")
    if not data["meta"]:
        insights.append("Meta description is missing — this impacts click-through rate.")
    if len(data["h1"]) == 0:
        insights.append("No H1 tag found — content structure is weak.")
    if data["missing_alt"] > 0:
        insights.append("Images without alt text reduce accessibility and SEO.")

    return insights

# ---------------- CHATBOT ---------------- #
def chatbot_response(question, data):
    question = question.lower()

    if "score" in question:
        return f"Your SEO score is {data['score']}, which indicates overall site health."

    elif "improve" in question:
        return "Focus on adding meta tags, improving headings, and optimizing images."

    elif "keyword" in question:
        return f"Top keywords are: {data['keywords']}"

    elif "issues" in question:
        return f"Main issues: {data['missing_alt']} images missing alt, H1 problems, or missing metadata."

    else:
        return "Ask about SEO score, keywords, or improvements."

# ---------------- MAIN ---------------- #

if st.button("Analyze"):
    if url:
        data = analyze_site(url)

        # ----------- DASHBOARD METRICS ----------- #
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("SEO Score", data["score"])
        col2.metric("H1 Tags", len(data["h1"]))
        col3.metric("H2 Tags", len(data["h2"]))
        col4.metric("Missing Alt Tags", data["missing_alt"])

        # ----------- SCORE FEEDBACK ----------- #
        if data["score"] > 80:
            st.success("🟢 Strong SEO Performance")
        elif data["score"] > 50:
            st.warning("🟡 Moderate SEO Performance")
        else:
            st.error("🔴 Poor SEO Performance")

        # ----------- KEYWORD CHART ----------- #
        st.subheader("📊 Keyword Analysis")
        df = pd.DataFrame(data["keywords"], columns=["Keyword", "Count"])
        st.bar_chart(df.set_index("Keyword"))

        # ----------- SEO BREAKDOWN ----------- #
        st.subheader("📌 SEO Breakdown")
        st.write({
            "Title": "Missing" if not data["title"] else "Good",
            "Meta Description": "Missing" if not data["meta"] else "Good",
            "H1 Tags": "Missing" if len(data["h1"]) == 0 else "Good",
            "Image SEO": f"{data['missing_alt']} missing alt tags"
        })

        # ----------- AI INSIGHTS ----------- #
        st.subheader("🧠 AI Insights")
        insights = generate_ai_insights(data)
        for i in insights:
            st.write("➤ " + i)

        # ----------- CHATBOT ----------- #
        st.subheader("🤖 Ask SEO Assistant")
        question = st.text_input("Ask something about your SEO")

        if question:
            answer = chatbot_response(question, data)
            st.info(answer)

        # ----------- COMPETITOR ----------- #
        if competitor_url:
            comp_data = analyze_site(competitor_url)

            st.subheader("⚔️ Competitor Comparison")
            comp_col1, comp_col2 = st.columns(2)

            comp_col1.metric("Your Score", data["score"])
            comp_col2.metric("Competitor Score", comp_data["score"])
