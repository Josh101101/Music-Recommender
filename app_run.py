import streamlit as st
import pandas as pd
from numpy import load
from scipy.sparse import load_npz
from content_based_filtering import content_recommendation
from hybrid_recommendations import HybridRecommenderSystem

# --- Load Data ---
cleaned_data_path = "data/cleaned_data.csv"
songs_data = pd.read_csv(cleaned_data_path)

transformed_data_path = "data/transformed_data.npz"
transformed_data = load_npz(transformed_data_path)

track_ids_path = "data/track_ids.npy"
track_ids = load(track_ids_path, allow_pickle=True)

filtered_data_path = "data/collab_filtered_data.csv"
filtered_data = pd.read_csv(filtered_data_path)

interaction_matrix_path = "data/interaction_matrix.npz"
interaction_matrix = load_npz(interaction_matrix_path)

transformed_hybrid_data_path = "data/transformed_hybrid_data.npz"
transformed_hybrid_data = load_npz(transformed_hybrid_data_path)

# --- Streamlit Config ---
st.set_page_config(page_title="Music Recommender", layout="wide")

st.title('🎶 Welcome to the Music Recommender!')

st.markdown("""
<style>
[data-testid="stSidebar"] > div:first-child {padding-top: 2rem;}
.block-container {padding-top: 1.5rem;}
thead tr th:first-child {display: none}
tbody th {display: none}
</style>
""", unsafe_allow_html=True)

# --- Two-column Layout ---
col_input, col_main = st.columns([1, 2], gap="large")

with col_input:
    st.header("Your Search")

    # Popular examples for user help (optional, can be made dynamic)
    with st.expander("Examples"):
        st.write("Try: ")
        st.write("- Song: **Immigrant song**, Artist: **led zeppelin**")
        st.write("- Song: **Blinding Lights**, Artist: **The Weeknd**")
        st.write("- Song: **Bohemian Rhapsody**, Artist: **Queen**")
        st.write("- Song: **One more night**, Artist: **Maroon 5**")
        st.write("- Song: **Roar**, Artist: **Katy Perry**")

    # Form for input (prevents UI refresh on every keystroke)
    with st.form(key="search_form"):
        # Song/artist selectbox (with search) or fallback to text input
        song_options = songs_data['name'].unique()
        artist_options = songs_data['artist'].unique()
        song_name = st.selectbox('Song name', options=song_options, index=0)
        # Only show artists for selected song (if possible)
        possible_artists = songs_data.loc[songs_data['name'] == song_name, 'artist'].unique()
        artist_name = st.selectbox('Artist name', options=possible_artists if len(possible_artists) > 0 else artist_options, index=0)

        # Number of recommendations
        k = st.selectbox('Number of recommendations', [5, 10, 15, 20], index=1)

        # Hybrid/content-based check
        song_name_proc = song_name.lower().strip()
        artist_name_proc = artist_name.lower().strip()
        in_hybrid = ((filtered_data["name"].str.lower() == song_name_proc) & (filtered_data["artist"].str.lower() == artist_name_proc)).any()
        filtering_type = "Hybrid Recommender System" if in_hybrid else "Content-Based Filtering"

        # Diversity slider for hybrid
        diversity = None
        content_based_weight = None
        if filtering_type == "Hybrid Recommender System":
            diversity = st.slider(label="Diversity in Recommendations", min_value=1, max_value=9, value=5, step=1)
            content_based_weight = 1 - (diversity / 10)
            chart_data = pd.DataFrame({"type": ["Personalized", "Diverse"], "ratio": [10 - diversity, diversity]})
            st.bar_chart(chart_data, x="type", y="ratio")

        submitted = st.form_submit_button("Get Recommendations")

with col_main:
    st.subheader('Recommendations')
    if "song_name" in locals() and song_name:
        st.write(f"**Song:** {song_name}")
    if "artist_name" in locals() and artist_name:
        st.write(f"**Artist:** {artist_name}")

    if "submitted" in locals() and submitted:
        with st.spinner("Generating recommendations..."):
            recommendations = None
            if filtering_type == "Content-Based Filtering":
                mask = (songs_data["name"].str.lower() == song_name_proc) & (songs_data["artist"].str.lower() == artist_name_proc)
                if mask.any():
                    st.info(f"Recommendations for **{song_name}** by **{artist_name}**")
                    recommendations = content_recommendation(
                        song_name=song_name_proc,
                        artist_name=artist_name_proc,
                        songs_data=songs_data,
                        transformed_data=transformed_data,
                        k=k
                    )
                else:
                    st.error(f"Sorry, we couldn't find '{song_name}' by '{artist_name}' in our database. Please try another song.")
            elif filtering_type == "Hybrid Recommender System":
                st.info(f"Recommendations for **{song_name}** by **{artist_name}**")
                recommender = HybridRecommenderSystem(
                    number_of_recommendations=k,
                    weight_content_based=content_based_weight,
                )
                recommendations = recommender.give_recommendations(
                    song_name=song_name_proc,
                    artist_name=artist_name_proc,
                    songs_data=filtered_data,
                    transformed_matrix=transformed_hybrid_data,
                    track_ids=track_ids,
                    interaction_matrix=interaction_matrix
                )

            # Show recommendations
            if recommendations is not None and not recommendations.empty:
                # Top 1-2: card style
                for ind, recommendation in recommendations.iterrows():
                    rec_song = recommendation['name'].title()
                    rec_artist = recommendation['artist'].title()
                    preview_url = recommendation.get('spotify_preview_url', None)
                    if ind == 0:
                        st.markdown("## Currently Playing")
                        st.markdown(f"#### **{rec_song}** by **{rec_artist}**")
                        if preview_url: st.audio(preview_url)
                        st.write('---')
                    elif ind == 1:
                        st.markdown("### Next Up 🎵")
                        st.markdown(f"#### {ind}. **{rec_song}** by **{rec_artist}**")
                        if preview_url: st.audio(preview_url)
                        st.write('---')
                    else:
                        st.markdown(f"#### {ind}. **{rec_song}** by **{rec_artist}**")
                        if preview_url: st.audio(preview_url)
                        st.write('---')
                # Compact table for the rest (optional)
                # st.dataframe(recommendations[["name", "artist", "album"]])
            elif recommendations is not None:
                st.warning("No recommendations available for this input.")
