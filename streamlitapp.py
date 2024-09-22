import streamlit as st
import difflib as dl
import pandas as pd
import numpy as np
import requests

# IGDB API credentials
client_id = '2s6fe3ts3br2aikeue6v2mvpspjkf3'
access_token = 'lvc89f0f0fl8xzxo62ovegnz1dqik4'

# IGDB API headers
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}',
}

# Cache the game cover fetching function
@st.cache_data
def fetch_cover_image(cover_id):
    try:
        response = requests.post(
            'https://api.igdb.com/v4/covers',
            headers=headers,
            data=f'fields id, image_id; where id = {cover_id};'
        )
        if response.status_code == 200:
            data = response.json()
            if data and 'image_id' in data[0]:
                image_id = data[0]['image_id']
                return f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg"
        st.error(f"Failed to fetch cover for ID {cover_id}: {response.text}")
    except Exception as e:
        st.error(f"Error fetching cover: {e}")
    return None

# Cache the CSV and similarity matrix loading
@st.cache_data
def load_games_data():
    return pd.read_csv('filtered_igdb_games_data.csv')

@st.cache_data
def load_similarity_matrix():
    return np.load('similarity_matrix.npy')

# Load the games data and similarity matrix
games_dat = load_games_data()
similarity_matrix = load_similarity_matrix()

# Function to find a close match of a game
def get_close_match_game(user_input_game):
    games_list = games_dat['Name'].tolist()
    return dl.get_close_matches(user_input_game, games_list, n=1)[0] if games_list else None

# Streamlit User Inputs
st.title("Game Recommendation System")
user_input_game = st.text_input('Enter your favorite game name:')
console_input = st.text_input('Enter the system you are using (e.g., Xbox One, PlayStation #, PC):')

# Check user input and proceed with recommendations
if user_input_game and console_input:
    close_match = get_close_match_game(user_input_game)

    if close_match:
        st.subheader(f"Recommendations based on \"{close_match}\" on {console_input}:")

        # Display the user-input game separately
        index_of_the_game = games_dat[games_dat['Name'] == close_match].index[0]

        # Get details of the user-input game
        game_name = games_dat['Name'][index_of_the_game]
        cover_id = games_dat['Cover'][index_of_the_game]
        storyline = games_dat['Storyline'][index_of_the_game]
        summary = games_dat['Summary'][index_of_the_game]

        # Fetch cover image for the user-input game or use placeholder
        cover_image_url = fetch_cover_image(cover_id) if pd.notna(cover_id) else 'https://via.placeholder.com/150'

        # Display the user-input game in its own row
        st.write("### Your game of choice:")
        st.image(cover_image_url, width=150, caption=game_name)
        with st.expander(f"More info about {game_name}"):
            st.write(f"**Storyline**: {storyline}")
            st.write(f"**Summary**: {summary}")

        # Get similarity scores for similar games (excluding the user-input game)
        similarity_scores = sorted(enumerate(similarity_matrix[index_of_the_game]), key=lambda x: x[1], reverse=True)
        similarity_scores = [score for score in similarity_scores if score[0] != index_of_the_game]

        # Collect the names and indices of the recommended games
        recommended_games = []
        max_results = 30
        for score in similarity_scores[:max_results]:
            index = score[0]
            game_name = games_dat['Name'][index]
            recommended_games.append((game_name, index))

        # Create a selectbox to select a game from recommended games
        options = [('Select a game', None)] + recommended_games
        selected_option = st.selectbox('Select a game to see more details:', options, format_func=lambda x: x[0])

        # If a game is selected, display the detailed view right below the select box
        if selected_option[1] is not None:
            selected_game_name, selected_game_index = selected_option
            selected_cover_id = games_dat['Cover'][selected_game_index]
            selected_storyline = games_dat['Storyline'][selected_game_index]
            selected_summary = games_dat['Summary'][selected_game_index]

            selected_cover_image_url = fetch_cover_image(selected_cover_id) if pd.notna(selected_cover_id) else 'https://via.placeholder.com/150'

            # Create a detailed view
            st.write(f"### {selected_game_name}")
            st.image(selected_cover_image_url, width=300)  # Larger image

            st.write(f"**Storyline**:")
            st.write(selected_storyline)
            st.write(f"**Summary**:")
            st.write(selected_summary)

        # Display the grid of images after the detailed view
        st.write("### Similar Games:")
        rows, cols_per_row = 6, 5
        for row in range(rows):
            columns = st.columns(cols_per_row)
            for col_idx in range(cols_per_row):
                game_idx = row * cols_per_row + col_idx
                if game_idx >= len(recommended_games):
                    break
                index = recommended_games[game_idx][1]
                game_name = recommended_games[game_idx][0]
                cover_id = games_dat['Cover'][index]
                cover_image_url = fetch_cover_image(cover_id) if pd.notna(cover_id) else 'https://via.placeholder.com/150'

                with columns[col_idx]:
                    st.image(cover_image_url, width=150, caption=game_name)

    else:
        st.warning(f'No close match found for "{user_input_game}". Please try another game.')

else:
    st.info("Please enter a game name and console to get recommendations.")