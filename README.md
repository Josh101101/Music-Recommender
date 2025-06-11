# Music Recommender System

A hybrid music recommender system built with Python and Streamlit. This project combines collaborative filtering and content-based filtering to provide personalized music recommendations.


---

## Features

- **Collaborative Filtering:** Recommends music based on user interaction patterns.
- **Content-Based Filtering:** Suggests tracks similar to those a user likes, based on track features.
- **Hybrid Recommendations:** Combines both approaches for improved accuracy.
- **Interactive Web App:** Built with Streamlit for easy user interaction.
- **Dockerized:** Easily deployable anywhere with Docker.

---

## Getting Started

### Prerequisites

- Python 3.11+
- [Docker](https://www.docker.com/get-started) (optional, for containerized deployment)
- [DVC](https://dvc.org/) (if using data versioning)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/music-recommender.git
   cd music-recommender
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **(Optional) Pull data with DVC:**
   ```sh
   dvc pull
   ```

### Running Locally

```sh
streamlit run app.py
```

The app will be available at [http://localhost:8501](http://localhost:8501) by default.

---

## Running with Docker

1. **Build the Docker image:**
   ```sh
   docker build -t music-recommender .
   ```

2. **Run the Docker container:**
   ```sh
   docker run -p 8000:8000 music-recommender
   ```

3. **Access the app:**  
   Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Project Structure

```
.
├── app.py
├── collaborative_filtering.py
├── content_based_filtering.py
├── hybrid_recommendations.py
├── data_cleaning.py
├── transform_filtered_data.py
├── requirements.txt
├── DockerFile
└── data/
```

---

## Testing

Run tests using pytest:

```sh
pytest test_app.py
```

---

## Deployment

This project supports CI/CD with GitHub Actions and deployment to AWS using Docker and CodeDeploy. See `.github/workflows/ci.yaml` for details.

---
<!--
## License

MIT License

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [DVC](https://dvc.org/)
- [AWS](https://aws.amazon.com/)

---

Feel free to open issues or contribute!
--!>
