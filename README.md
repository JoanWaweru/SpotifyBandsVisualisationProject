# Spotify Extract and Visualization Dashboard

A Python-based project that extracts data from Spotify's API to gather insights about various bands in the world across different genres. This project processes the data and provides an interactive visualization dashboard using Plotly and Dash.

---

## Features

### Spotify Extract
- Fetches detailed artist information, including:
  - Name, Followers, Popularity, Genres
- Retrieves up to 5 albums per artist and their respective tracks.
- Includes audio features for tracks such as:
  - Danceability, Energy, Valence, Acousticness, Loudness, and more.
- Caches data locally for efficient re-execution.

### Spotify Dashboard
- Visualizes data extracted with interactive dashboards, including:
  - **Popularity vs. Followers**: Scatter plot to understand artist reach.
  - **Audio Features Comparison**: Parallel coordinates and scatter matrix visualizations.
  - **Tracks Over Time**: Line charts for genre-based release trends.
  - **Top Bands**: Bar charts for the most followed/popular bands.
  - **Sentiment Analysis**: Categorizes track sentiments based on valence.
  - **Genre Diversity**: Single vs. multi-genre artist analysis.

---

## Important Disclaimer

As of **November 27, 2024**, Spotify has deprecated access to several Web API endpoints, including those for retrieving audio features and analyses of tracks. This change affects new applications and those in development mode, limiting their ability to access detailed audio data. For more details, visit the [Spotify Developer Blog](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api).

### Recommended Solution
To overcome this limitation, you can use the **pre-extracted dataset** provided by this project:
- The dataset is stored in the `spotify_cache.json` file and includes comprehensive artist, album, and track data along with audio features.

### Using the Dataset
1. Ensure you have the following dependencies installed:
   ```plaintext
   pandas
   numpy
   ```
2. Install the dependencies if needed:
   ```bash
   pip install pandas numpy
   ```
3. Use the `spotify_cache.json` file for your analysis and visualizations.

By leveraging this dataset, you can continue your audio feature analysis seamlessly, even with the recent API restrictions.

---

## Installation

### Prerequisites
- Python 3.7+
- Spotify Developer Account
- Spotify Client ID and Secret (Get them from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/))

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/JoanWaweru/SpotifyBandsVisualisationProject.git
   cd SpotifyBandsVisualisationProject
   ```

2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Spotify credentials:
   - Replace the `client_id` and `client_secret` in `spotify_extract.py` with your own credentials.

4. Run the Spotify Extract script to cache data:
   ```bash
   python spotify_extract.py
   ```

5. Launch the Dashboard:
   ```bash
   python spotify_dashboard.py
   ```

6. Open the application in your browser:
   - By default: `http://127.0.0.1:8050/`

---

## Usage

### Spotify Extract Script
- Modify the `artist_names` list in `spotify_extract.py` to include your favorite artists or bands.
- The script will fetch artist, album, and track details and save them to `spotify_cache.json`.

### Visualization Dashboard
- Interact with the dashboards to explore:
  - Popular artists and bands across genres.
  - Trends in music release over time.
  - Sentiment analysis of tracks.
  - Comparison of audio features across genres.

---

## Technologies Used
- **Programming Language**: Python
- **APIs**: Spotify API via Spotipy
- **Visualization**: Plotly, Dash
- **Data Processing**: Pandas
- **Cache Management**: JSON

---

## Future Enhancements
- Add more audio feature visualizations.
- Include more filtering options in the dashboard.
- Enhance the user interface with additional styling.

---

## Contributors
- [Joan Waweru](https://github.com/joanwaweru) - Project Author
