import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

st.set_page_config(page_title="SEO Analyzer", layout="wide")

st.title("🚀 SEO Analyzer Tool")
st.write("Analyze your website and get instant SEO insights")

url = st.text_input("Enter Website URL (with https://)")

if st.button("Analyze"):
    if not url:
        st.warning("Please enter a URL")
    else:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # TITLE
            title = soup.title.string if soup.title else ""

            # META
            meta_desc = ""
            meta = soup.find("meta", attrs={"name": "description"})
            if meta:
                meta_desc = meta.get("content")

            # HEADINGS
            h1 = [h.text.strip() for h in soup.find_all("h1")]
            h2 = [h.text.strip() for h in soup.find_all("h2")]

            # IMAGES
            images = soup.find_all("img")
            missing_alt = [img for img in images if not img.get("alt")]

            # KEYWORDS
            text = soup.get_text().lower()
            words = re.findall(r'\b\w+\b', text)
            keywords = Counter(words).most_common(10)

            # SEO SCORE
            score = 100
            if not title: score -= 20
            if not meta_desc: score -= 20
            if len(h1) == 0: score -= 20
            if len(missing_alt) > 0: score -= 10

            # DISPLAY
            st.subheader("📊 SEO Results")

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Title")
                st.write(title if title else "Missing")

                st.write("### Meta Description")
                st.write(meta_desc if meta_desc else "Missing")

                st.write("### H1 Tags")
                st.write(h1 if h1 else "None")

                st.write("### H2 Tags")
                st.write(h2 if h2 else "None")

            with col2:
                st.write("### Images")
                st.write(f"Total: {len(images)}")
                st.write(f"Missing Alt: {len(missing_alt)}")

                st.write("### Top Keywords")
                st.write(keywords)

                st.write("### SEO Score")
                st.success(f"{score}/100")

            # RECOMMENDATIONS
            st.subheader("📌 Recommendations")

            if not title:
                st.warning("Add a proper title tag")
            if not meta_desc:
                st.warning("Add a meta description")
            if len(h1) == 0:
                st.warning("Add at least one H1 tag")
            if len(missing_alt) > 0:
                st.warning("Add alt text to images")

        except Exception as e:
            st.error(f"Error: {e}")
