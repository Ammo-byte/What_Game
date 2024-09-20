import streamlit as st
import difflib as dl
import pandas as pd
import numpy as np
import requests

# IGDB API credentials
client_id = '2s6fe3ts3br2aikeue6v2mvpspjkf3'
access_token = 'lvc89f0f0fl8xzxo62ovegnz1dqik4'

# Your IGDB API headers
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}',
}

# Function to fetch game cover by Cover ID
def fetch_cover_image(cover_id):
    try:
        # Query IGDB for the cover image
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
        else:
            st.error(f"Failed to fetch cover for ID {cover_id}: {response.text}")
    except Exception as e:
        st.error(f"Error fetching cover: {e}")
    return None

# Load the games data
games_dat = pd.read_csv('filtered_igdb_games_data.csv')

# Load the similarity matrix
similarity_matrix = np.load('similarity_matrix.npy')

# Function to find a close match of a game
def get_close_match_game(user_input_game):
    list_of_all_games = games_dat['Name'].tolist()
    find_close_match = dl.get_close_matches(user_input_game, list_of_all_games)
    if find_close_match:
        return find_close_match[0]
    return None

# Streamlit User Inputs
st.title("Game Recommendation System")

user_input_game = st.text_input('Enter your favorite game name:')
console_input = st.text_input('Enter the system you are using (e.g., Xbox One, PlayStation #, PC):')

# If user provides input
if user_input_game and console_input:
    close_match = get_close_match_game(user_input_game)

    if close_match:
        st.subheader(f"Games suggested for you based on \"{close_match}\" on {console_input}:")

        # Get the index of the matched game
        index_of_the_game = games_dat[games_dat['Name'] == close_match].index[0]

        # Calculate similarity scores
        similarity_scores = list(enumerate(similarity_matrix[index_of_the_game]))

        # Sort games by similarity score
        sorted_similar_games = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        displayed_games = set()  # Track displayed games to avoid duplicates
        max_results = 30  # Limit the number of results (5 by 6 grid)

        # Check if required columns exist in the DataFrame
        if 'Cover' not in games_dat.columns or 'Storyline' not in games_dat.columns or 'Summary' not in games_dat.columns:
            st.error("The DataFrame does not contain required columns (Cover, Storyline, or Summary).")
            st.stop()

        # Create a grid layout with 5 columns and 6 rows
        rows = 6
        cols_per_row = 5
        for row in range(rows):
            # Create a set of columns for each row
            columns = st.columns(cols_per_row)

            # Display 5 games in each row
            for col_idx in range(cols_per_row):
                game_idx = row * cols_per_row + col_idx
                if game_idx >= max_results:
                    break  # Stop if we reach the max number of games

                game = sorted_similar_games[game_idx]
                index = game[0]
                if index in displayed_games:
                    continue

                # Get game details
                game_name = games_dat['Name'][index]
                cover_id = games_dat['Cover'][index]  # Assuming 'Cover' contains the cover ID from IGDB
                storyline = games_dat['Storyline'][index]
                summary = games_dat['Summary'][index]

                # Fetch the cover image from IGDB if the Cover ID is valid
                cover_image_url = None
                if pd.notna(cover_id):
                    cover_image_url = fetch_cover_image(cover_id)

                if not cover_image_url:
                    # Use a placeholder if the cover image couldn't be fetched
                    cover_image_url = 'https://via.placeholder.com/150'

                try:
                    # Display the cover image and details in each column
                    with columns[col_idx]:
                        st.image(cover_image_url, width=150, caption=game_name)
                        with st.expander(f"More info about {game_name}"):
                            st.write(f"**Storyline**: {storyline}")
                            st.write(f"**Summary**: {summary}")
                except Exception as e:
                    st.error(f"Error displaying image for {game_name}: {e}")
                    continue

                displayed_games.add(index)

    else:
        st.warning(f'No close match found for "{user_input_game}". Please try another game.')

else:
    st.info("Please enter a game name and console to get recommendations.")