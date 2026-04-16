import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

st.set_page_config(page_title="AI SEO Assistant", layout="wide")

st.title("🚀 AI SEO Assistant for Marketing Teams")

url = st.text_input("Enter Your Website URL")
competitor_url = st.text_input("Enter Competitor URL (Optional)")

def analyze_site(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else ""
    
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content")

    h1 = [h.text.strip() for h in soup.find_all("h1")]
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
        "missing_alt": len(missing_alt),
        "keywords": keywords,
        "score": score
    }

if st.button("Analyze"):
    if url:
        data = analyze_site(url)

        st.subheader("📊 SEO Score")
        st.success(f"{data['score']}/100")

        st.subheader("📌 SEO Breakdown")
        st.write({
            "Title": "Missing" if not data["title"] else "Good",
            "Meta Description": "Missing" if not data["meta"] else "Good",
            "H1 Tags": "Missing" if len(data["h1"]) == 0 else "Good",
            "Image SEO": f"{data['missing_alt']} missing alt tags"
        })

        st.subheader("🔍 Top Keywords")
        st.write(data["keywords"])

        st.subheader("⚡ Quick Wins")
        if not data["title"]:
            st.write("➤ Add a title tag to improve ranking")
        if not data["meta"]:
            st.write("➤ Add meta description to improve CTR")
        if len(data["h1"]) == 0:
            st.write("➤ Add H1 tag for better structure")
        if data["missing_alt"] > 0:
            st.write("➤ Add alt text to images")

        st.subheader("🧠 AI Suggestions")
        st.write("Improve keyword usage and ensure content matches search intent.")

        # Competitor Comparison
        if competitor_url:
            comp_data = analyze_site(competitor_url)

            st.subheader("⚔️ Competitor Comparison")
            st.write({
                "Your Score": data["score"],
                "Competitor Score": comp_data["score"]
            })
