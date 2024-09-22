# What_Game ? : The Game Recommender System

## Overview
This project is a **Game Recommender System** that suggests video games based on the similarity of a user's input game to other games in the dataset. The system uses a similarity matrix to recommend the most similar games and displays relevant information such as game covers, storyline and summary.

## Features
- **Game Recommendations**: Based on input, the system recommends up to 30 similar games.
- **Game Covers**: Fetches and displays the cover image of each recommended game.
- **Game Details**: Displays the storyline and summary of selected games.
- **Grid Display**: Shows recommendations in a 5x6 grid format.
  
## How It Works
1. **Input**: The user enters their favourite game and the gaming console they're using (e.g., Xbox One, PlayStation).
2. **Recommendation**: The system calculates similarity scores between the input game and others in the dataset using a pre-computed similarity matrix.
3. **Display**: It shows the recommended games in a grid format, with game covers and details (storyline and summary).
4. **Game Details**: The user can select a game to view more detailed information such as storyline and summary.

## So What? — The Purpose and Impact of This Project

The **Game Recommender System** was created to solve a common problem faced by gamers today: **discovering new games based on personal preferences**. With an overwhelming number of titles across platforms, players often struggle to find games that match their tastes. This project aims to simplify the process of game discovery by providing personalized recommendations based on the similarity of games.

### Why This Matters:

1. **Personalized Game Discovery**:
   Gamers typically rely on friends, reviews, or browsing through massive online stores to find new games. This project automates the discovery process by analyzing a player’s favorite games and recommending similar titles. It narrows down the choices, saving time and providing a more tailored gaming experience.

2. **Data-Driven Recommendations**:
   Unlike traditional recommendation methods that may rely solely on user ratings or sales data, this system leverages a **similarity matrix** that compares various attributes of games, such as genre, platform, and storyline. By using data-driven insights, the recommendations are more relevant to the user's actual preferences.

3. **Cross-Platform Compatibility**:
   In a world where players often switch between gaming platforms like Xbox, PlayStation, and PC, this recommender system accounts for platform preferences. It helps users find games that not only align with their tastes but are also available on their desired system, making cross-platform gaming more accessible.

4. **Enhancing User Engagement**:
   Game studios and developers benefit when players stay engaged within their gaming ecosystem. A robust recommendation engine like this can drive user engagement by helping players continuously discover and play games they are likely to enjoy, increasing satisfaction and loyalty to particular platforms or franchises.

### Broader Impact:

- **Reducing Choice Paralysis**: 
   In today’s gaming landscape, where thousands of games are released across multiple platforms, the sheer volume of choices can overwhelm players. This project addresses that issue by narrowing down the selection to games that match a user’s preferences, making game discovery more manageable.

- **Supporting the Indie Game Market**:
   Many indie game developers struggle to gain visibility against large, AAA game releases. By recommending games based purely on similarity rather than marketing or popularity, this system can help expose users to lesser-known titles that align with their tastes, potentially supporting smaller developers.

- **A Prototype for Broader Recommendation Systems**:
   While the current scope is limited to games, this project demonstrates the potential for **data-driven recommendation systems** across other industries. Whether for movies, music, or books, this kind of recommendation algorithm can be adapted to various media to help users discover new content in a personalized and efficient way.

### Conclusion:
The **Game Recommender System** bridges the gap between players and game discovery in a data-centric way, leveraging modern technology to provide personalized, cross-platform recommendations. As gaming continues to expand into new realms, such as cloud gaming and virtual reality, projects like this will become increasingly valuable in helping players explore and enjoy the vast world of games.

## Requirements

To run this project, you need the following:

- Python 3.8 or higher
- The following Python packages:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `requests`
  - `difflib`

You can install the required dependencies using the following command:

```bash
pip install streamlit pandas numpy requests difflib
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/game-recommender-system.git
   cd game-recommender-system
   ```

2. **Set up the IGDB API**:
   - Sign up for an IGDB API account [here](https://api.igdb.com/).
   - Get your `Client-ID` and `Access Token`.
   - Update the `streamlitapp.py` script with your credentials:
     ```python
     client_id = 'your_client_id'
     access_token = 'your_access_token'
     ```

3. **Run the Streamlit App**:
   After installing dependencies, navigate to the project directory and run the Streamlit app:
   ```bash
   streamlit run streamlitapp.py
   ```

4. **Explore the Application**:
   - Enter your favorite game and console in the input fields.
   - View the recommended games in a grid format and select a game to see its details.

## Project Structure

```bash
.
├── README.md                # This file
├── recommender-system.ipynb          # Main script to with data cleaning and the recommender system without streamlit application
├── streamlitapp.py          # Main streamlit script to run the recommender system
├── filtered_igdb_games_data.csv  # Game data (filtered)
├── igdb_games_data.csv  # All game data (unfiltered)
├── similarity_matrix.npy     # Precomputed similarity matrix ( This file was too large, run the .ipynb file to get the matrix) 
├── cover_cache/             # Cached game covers (generated automatically)
```

## Example

### Input
- **Favorite Game**: *The Legend of Zelda: Breath of the Wild*
- **Console**: *Nintendo Switch*

### Output
- A grid of recommended games with their cover images.
- Clicking on a game shows its storyline and summary.

## Key Functions

### `fetch_cover_image(cover_id)`
- Fetches the game cover image using the IGDB API.
- Caches the image locally for faster future loads.

### `get_close_match_game(user_input_game)`
- Finds the closest matching game in the dataset based on user input using `difflib`.

### `load_similarity_matrix()`
- Loads the precomputed similarity matrix from a `.npy` file, which is used to calculate game recommendations.

## Troubleshooting

### Common Issues
- **API Quota Limit**: If you exceed the API call limit, you may need to wait for the quota to reset or consider batching requests.
- **Long Load Times**: Ensure you are caching the images correctly to avoid making repeated API calls.

## Future Enhancements
- **Improve Algorithm**: Experiment with different similarity algorithms to improve recommendation accuracy.
- **Add Filters**: Allow users to filter recommendations by genre, release year, or rating.
- **Personalized Recommendations**: Use machine learning to tailor recommendations based on user preferences.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss potential improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
