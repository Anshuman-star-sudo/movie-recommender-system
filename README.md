# 🎬 Movie Recommender System

A content-based movie recommendation web application built using Python, Scikit-Learn, and Streamlit. The application calculates structural and textual similarities between movies using the TMDB 5000 dataset to recommend the top 5 most similar movies based on a user's choice, complete with live poster fetching.

🌐 **Live Demo:** https://bookrecommender-fspsfits9shyukfsamgjxa.streamlit.app/

---

## 🚀 Features

* **Content-Based Filtering:** Uses textual tags (genres, keywords, cast, crew, overview) to map semantic similarities.
* **Dynamic Poster Fetching:** Integrated with **The Movie Database (TMDB) API** via asymmetric multi-threading (`ThreadPoolExecutor`) to render high-resolution posters concurrently without lagging the UI.
* **Efficient Caching:** Utilizes Streamlit's `@st.cache_data` engine to maintain heavy cosine-similarity matrices persistently in RAM, ensuring instantaneous search results.
* **Fully Responsive UI:** Interactive frontend built completely in Python with clean search auto-completes.

---

## 🛠️ Tech Stack & Concepts

* **Frontend & Hosting:** Streamlit Community Cloud
* **Data Processing:** Pandas, NumPy, Python Pickle
* **Machine Learning:** Vectorization (`CountVectorizer`), Text Preprocessing (Stemming), Cosine Similarity Scoring
* **Data Source:** TMDB 5000 Dataset

---

## 📂 Project Architecture

```text
📂 movie-recommender-system/
├── app.py                  # Streamlit application UI & inference orchestration
├── requirements.txt        # Managed server-side environment dependencies
├── .gitignore              # Configured deployment exclusions (.pkl and .csv optimization)
├── .gitattributes         # Git LFS pointer mapping tracking structural layers
├── movies.pkl              # Preprocessed DataFrame storage
├── movies_dict.pkl         # Serialized dictionary mapping indexes to titles
└── similarity.pkl          # Compressed 4806x4806 cosine similarity matrix
```
