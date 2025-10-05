import streamlit as st
import os
from nasa_client import NASAClient
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

client = NASAClient(API_KEY)

st.set_page_config(page_title="Cosmic Canvas", layout="wide")
st.title("🪐 Cosmic Canvas: Explore NASA's Universe")

tabs = st.tabs(["🌠 Picture of the Day", "🔭 Image Search"])

# --- APOD Tab ---
with tabs[0]:
    st.header("Astronomy Picture of the Day")
    selected_date = st.date_input("Select a date", value=date.today())
    hd = st.toggle("Load in High Definition", value=True)

    if st.button("Fetch APOD"):
        with st.spinner("Fetching APOD..."):
            try:
                apod = client.get_apod(date=selected_date.isoformat(), hd=hd)
                st.subheader(apod.get("title", ""))
                if apod.get("media_type") == "image":
                    st.image(apod["url"], use_column_width=True)
                elif apod.get("media_type") == "video":
                    st.video(apod["url"])
                st.markdown(f"*Date:* {apod.get('date')}")
                st.markdown(f"*Explanation:*\n{apod.get('explanation')}")
            except Exception as e:
                st.error(f"Error fetching APOD: {e}")

# --- Image Search Tab ---
with tabs[1]:
    st.header("Search NASA's Image Library")

    col1, col2 = st.columns(2)
    with col1:
        query = st.text_input("Enter a keyword (e.g. galaxy, Mars, nebula)")
    with col2:
        media_types = st.multiselect("Media Types", ["image", "video"], default=["image"])

    page = st.number_input("Page Number", min_value=1, step=1, value=1)

    if st.button("Search Images"):
        with st.spinner("Searching..."):
            try:
                results = client.search_images(query=query, media_type=media_types, page=page)
                items = results.get("collection", {}).get("items", [])
                if not items:
                    st.warning("No results found.")
                else:
                    for item in items:
                        data = item.get("data", [{}])[0]
                        links = item.get("links", [{}])
                        image_url = next((l.get("href") for l in links if l.get("render") == "image"), None)

                        st.subheader(data.get("title", "No Title"))
                        st.caption(f"📅 {data.get('date_created', '')}")
                        if image_url:
                            st.image(image_url, width=500)
                        st.markdown(data.get("description", "No Description Available"))
                        st.markdown("---")
            except Exception as e:
                st.error(f"Search error: {e}")