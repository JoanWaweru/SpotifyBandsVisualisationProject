from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Load Spotify cache data
CACHE_FILE = "spotify_cache.json"


def load_spotify_data():
    """
    Load Spotify data from cache and process it into a DataFrame.
    """
    with open(CACHE_FILE, "r") as f:
        spotify_data = json.load(f)

    data = []
    for artist, details in spotify_data.items():
        for album in details.get("albums", []):
            for track in album.get("tracks", []):
                data.append({
                    "Band Name": artist,
                    "Followers": details["followers"],
                    "Popularity": details["popularity"],
                    "Genres": ", ".join(details["genres"]),
                    "Album Name": album["album_name"],
                    "Release Date": album["release_date"],
                    "Track Name": track["track_name"],
                    "Danceability": track["audio_features"]["danceability"],
                    "Energy": track["audio_features"]["energy"],
                    "Valence": track["audio_features"]["valence"],
                    "Acousticness": track["audio_features"]["acousticness"],
                    "Loudness": track["audio_features"]["loudness"]
                })
    df = pd.DataFrame(data)

    # Convert release date to datetime
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    return df

def map_genres(genre_list):
    """
    Map genres to broader categories for clarity.
    """
    genre_mapping = {
        "rock": "Rock",
        "pop": "Pop",
        "hip hop": "Hip-Hop",
        "rap": "Hip-Hop",
        "jazz": "Jazz",
        "blues": "Blues",
        "k-pop": "K-Pop",
        "metal": "Metal",
        "punk": "Punk",
        "electronic": "Electronic/Dance",
        "reggae": "Reggae",
        "country": "Country",
        "latin": "Latin",
        "afro soul": "African"
    }
    for genre, broad_category in genre_mapping.items():
        if genre in genre_list.lower():
            return broad_category
    return "Other"

# Load and preprocess data
df = load_spotify_data()
df['Broad Genre'] = df['Genres'].apply(map_genres)

# Define the app
app = Dash(__name__)


# Add the new graph to the layout
app.layout = html.Div([
    html.H1("Spotify Bands Data Visualization", style={'textAlign': 'center'}),

    # Dropdown for filtering by genre
    html.Div([
        html.Label("Select Genre:"),
        dcc.Dropdown(
            id='genre-filter',
            options=[{'label': genre, 'value': genre} for genre in df['Broad Genre'].unique()],
            value=None,
            multi=True
        )
    ], style={'width': '48%', 'margin': 'auto'}),

    # Dropdown for filtering by year
    # html.Div([
    #     html.Label("Select Year:"),
    #     dcc.Dropdown(
    #         id='year-filter',
    #         options=[{'label': int(year), 'value': int(year)} for year in
    #                  sorted(df['Release Date'].dt.year.dropna().unique())],
    #         value=None,
    #         placeholder="Select a year (optional)"
    #     )
    # ], style={'width': '48%', 'margin': 'auto'}),

    # Slider for filtering by popularity
    html.Div([
        html.Label("Select Popularity Range:"),
        dcc.RangeSlider(
            id='popularity-slider',
            min=int(df['Popularity'].min()),
            max=int(df['Popularity'].max()),
            step=1,
            value=[int(df['Popularity'].min()), int(df['Popularity'].max())],
            marks={i: str(i) for i in range(int(df['Popularity'].min()), int(df['Popularity'].max()) + 1, 10)}
        )
    ], style={'width': '80%', 'margin': '20px auto'}),

    # Graphs
    html.Div([
        dcc.Graph(id='popularity-followers-scatter'),
        dcc.Graph(id='top-bands-bar'),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div([
        dcc.Graph(id='genre-diversity-bar'),
        dcc.Graph(id='genre-bar'),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div([
        dcc.Graph(id='sentiment-analysis'),
        dcc.Graph(id='time-trends-line-chart'),
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'}),

    # 3D Scatter Plot with dynamic axis selection
    # html.Div([
    #     html.Label("Select X-axis Feature:"),
    #     dcc.Dropdown(
    #         id='x-axis-feature',
    #         options=[
    #             {'label': 'Energy', 'value': 'Energy'},
    #             {'label': 'Danceability', 'value': 'Danceability'},
    #             {'label': 'Valence', 'value': 'Valence'},
    #             {'label': 'Acousticness', 'value': 'Acousticness'}
    #             # {'label': 'Loudness', 'value': 'Loudness'}
    #         ],
    #         value='Energy'
    #     )
    # ], style={'width': '30%', 'display': 'inline-block'}),
    #
    # html.Div([
    #     html.Label("Select Y-axis Feature:"),
    #     dcc.Dropdown(
    #         id='y-axis-feature',
    #         options=[
    #             {'label': 'Energy', 'value': 'Energy'},
    #             {'label': 'Danceability', 'value': 'Danceability'},
    #             {'label': 'Valence', 'value': 'Valence'},
    #             {'label': 'Acousticness', 'value': 'Acousticness'}
    #             # {'label': 'Loudness', 'value': 'Loudness'}
    #         ],
    #         value='Danceability'
    #     )
    # ], style={'width': '30%', 'display': 'inline-block'}),

    # html.Div([
    #     html.Label("Select Z-axis Feature:"),
    #     dcc.Dropdown(
    #         id='z-axis-feature',
    #         options=[
    #             {'label': 'Energy', 'value': 'Energy'},
    #             {'label': 'Danceability', 'value': 'Danceability'},
    #             {'label': 'Valence', 'value': 'Valence'},
    #             {'label': 'Acousticness', 'value': 'Acousticness'}
    #             # {'label': 'Loudness', 'value': 'Loudness'}
    #         ],
    #         value='Valence'
    #     )
    # ], style={'width': '30%', 'display': 'inline-block'}),

    # html.Div([
    #     # dcc.Graph(id='time-trends-line-chart'),
    #     dcc.Graph(id='time-trends-line-chart'),
    # ], style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div([
        dcc.Graph(id='audio-feature-comparison-parallel'),
    ], style={'margin': '20px auto', 'width': '90%'}),

    html.Div([
        dcc.Graph(id='audio-feature-comparison-all'),
    ], style={'margin': '20px auto', 'width': '90%'})
])



# Callbacks for visualizations
# Existing Callbacks
@app.callback(
    Output('popularity-followers-scatter', 'figure'),
    Input('genre-filter', 'value')
)
def update_scatter(selected_genres):
    filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df
    fig = px.scatter(
        filtered_df,
        x="Followers",
        y="Popularity",
        color="Broad Genre",  # Use Broad Genre for color mapping
        hover_name="Band Name",
        title="Popularity vs Followers",
        size="Popularity",
        color_discrete_map={
            "Pop": "red",
            "Rock": "blue",
            "Hip-Hop": "purple",
            "Jazz": "orange",
            "Blues": "lightblue",
            "Metal": "gray",
            "Punk": "green",
            "Electronic/Dance": "yellow",
            "Reggae": "brown",
            "Country": "gold",
            "Latin": "teal",
            "African": "darkgreen",
            "Other": "lightgray"
        }
    )

    # Set static axis ranges
    fig.update_layout(
        xaxis=dict(range=[0, df['Followers'].max()], title="Followers"),
        yaxis=dict(range=[0, 100], title="Popularity"),  # Adjusted y-axis range
        dragmode='zoom',  # Enable zooming
        height=600
    )
    return fig

@app.callback(
    Output('audio-feature-comparison-all', 'figure'),
    Input('genre-filter', 'value')
)
def update_audio_feature_comparison(selected_genres):
    # Filter data based on selected genres
    filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df

    # Create a scatter matrix with additional hover data
    fig = px.scatter_matrix(
        filtered_df,
        dimensions=["Energy", "Loudness", "Valence", "Danceability", "Acousticness"],
        color="Broad Genre",
        title="Audio Feature Comparison by Genre",
        hover_data=["Band Name"],  # Include Band Name in hover data
        labels={"Broad Genre": "Genres"},
        color_discrete_map={
            "Pop": "red",
            "Rock": "blue",
            "Hip-Hop": "purple",
            "Jazz": "orange",
            "Blues": "lightblue",
            "K-Pop": "pink",
            "Metal": "gray",
            "Punk": "green",
            "Electronic/Dance": "yellow",
            "Reggae": "brown",
            "Country": "gold",
            "Latin": "teal",
            "African": "darkgreen",
            "Other": "lightgray"
        }
    )

    # Update layout for better readability
    fig.update_layout(
        height=800,
        title_font_size=20,
        title_x=0.5,
        legend_title="Genres",
        margin=dict(t=50, l=50, r=50, b=50)
    )

    return fig


# @app.callback(
#     Output('dance-energy-bar', 'figure'),
#     Input('genre-filter', 'value')
# )
# def update_scatter_dance_energy(selected_genres):
#     filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df
#     grouped = filtered_df.groupby(["Band Name", "Broad Genre"])[["Danceability", "Energy"]].mean().reset_index()
#
#     fig = px.scatter(
#         grouped,
#         x="Danceability",
#         y="Energy",
#         color="Broad Genre",
#         hover_name="Band Name",
#         size="Danceability",
#         title="Danceability vs Energy by Band and Genre",
#         color_discrete_map={
#             "Pop": "red",
#             "Rock": "blue",
#             "Hip-Hop": "purple",
#             "Jazz": "orange",
#             "Blues": "lightblue",
#             "K-Pop": "pink",
#             "Metal": "gray",
#             "Punk": "green",
#             "Electronic/Dance": "yellow",
#             "Reggae": "brown",
#             "Country": "gold",
#             "Latin": "teal",
#             "African": "darkgreen",
#             "Other": "lightgray"
#         }
#     )
#
#     # Set static axis ranges
#     fig.update_layout(
#         xaxis=dict(range=[0, 1], title="Danceability"),
#         yaxis=dict(range=[0, 1], title="Energy"),
#         dragmode='zoom',
#         height=600
#     )
#     return fig


@app.callback(
    Output('genre-diversity-bar', 'figure'),
    Input('genre-filter', 'value')
)
def update_genre_diversity(selected_genres):
    """
    Analyze genre diversity for bands and visualize the count of single-genre vs. multi-genre bands.
    """
    # Filter data by selected genres
    filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df

    # Calculate the number of genres for each band
    filtered_df['Num Genres'] = filtered_df['Genres'].apply(lambda x: len(x.split(", ")))

    # Classify bands as single-genre or multi-genre
    filtered_df['Genre Diversity'] = filtered_df['Num Genres'].apply(
        lambda x: 'Single-Genre' if x == 1 else 'Multi-Genre'
    )

    # Count the number of bands in each category
    genre_diversity_counts = (
        filtered_df.groupby('Genre Diversity')['Band Name']
        .nunique()
        .reset_index()
        .rename(columns={'Band Name': 'Band Count'})
    )

    # Create a bar chart
    fig = px.bar(
        genre_diversity_counts,
        x='Genre Diversity',
        y='Band Count',
        color='Genre Diversity',
        title='Count of Single-Genre vs. Multi-Genre Bands',
        labels={'Band Count': 'Number of Bands'},
        color_discrete_map={
            'Single-Genre': 'blue',
            'Multi-Genre': 'orange'
        }
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title="Genre Diversity",
        yaxis_title="Number of Bands",
        legend_title="Diversity Type",
        height=600
    )

    return fig


# Top Bands by Followers and Popularity (Bar Chart)
@app.callback(
    Output('top-bands-bar', 'figure'),
    [Input('genre-filter', 'value'),
     Input('popularity-slider', 'value')]
)
def update_top_bands(selected_genres, popularity_range):
    # Filter data based on selected genres and popularity range
    filtered_df = df[(df['Popularity'] >= popularity_range[0]) & (df['Popularity'] <= popularity_range[1])]

    # Check if genres are selected, and filter further
    if selected_genres:
        filtered_df = filtered_df[filtered_df['Broad Genre'].isin(selected_genres)]

    # Ensure the filtered DataFrame is not empty
    if filtered_df.empty:
        return go.Figure().update_layout(
            title="No Data Available",
            xaxis=dict(title="Followers"),
            yaxis=dict(title="Band Name"),
        )

    # Group by band name and calculate mean values
    grouped = filtered_df.groupby("Band Name")[["Followers", "Popularity"]].mean().reset_index()

    # Sort by followers in descending order
    top_bands = grouped.sort_values(by="Followers", ascending=False).head(10)

    # Create bar chart
    fig = px.bar(
        top_bands,
        x="Followers",
        y="Band Name",
        orientation='h',
        color="Popularity",
        title="Top Bands by Followers and Popularity",
        text="Followers",
        color_continuous_scale="Viridis"
    )

    # Update layout
    fig.update_layout(
        height=600,
        xaxis_title="Followers",
        yaxis_title="Band Name",
        yaxis=dict(categoryorder='total ascending')  # Ensure the order is descending by followers
    )

    return fig


# Callback for the Parallel Coordinates Plot with Interactive Genres
@app.callback(
    Output('audio-feature-comparison-parallel', 'figure'),
    [Input('genre-filter', 'value'), Input('popularity-slider', 'value')]
)
def update_audio_features_parallel_coordinates(selected_genres, popularity_range):
    """
    Update the parallel coordinates plot based on selected genres.
    """
    # Filter data based on selected genres and popularity range
    filtered_df = df[(df['Popularity'] >= popularity_range[0]) & (df['Popularity'] <= popularity_range[1])]
    if selected_genres:
        filtered_df = filtered_df[filtered_df['Broad Genre'].isin(selected_genres)]

    # Calculate the mean audio features for each genre
    avg_features = filtered_df.groupby('Broad Genre')[
        ["Energy", "Loudness", "Valence", "Danceability", "Acousticness"]].mean().reset_index()

    # Add genre colors
    genre_color_map = {
        "Pop": "red",
        "Rock": "blue",
        "Hip-Hop": "purple",
        "Jazz": "orange",
        "Blues": "lightblue",
        "K-Pop": "pink",
        "Metal": "gray",
        "Punk": "green",
        "Electronic/Dance": "yellow",
        "Reggae": "brown",
        "Country": "gold",
        "Latin": "teal",
        "African": "darkgreen",
        "Other": "lightgray"
    }
    avg_features['Color'] = avg_features['Broad Genre'].map(genre_color_map)

    # Create the parallel coordinates plot
    fig = go.Figure(data=go.Parcoords(
        line=dict(
            color=avg_features.index,
            colorscale=[(i / len(avg_features), color) for i, color in enumerate(avg_features['Color'])],
            showscale=False
        ),
        dimensions=[
            dict(label="Energy", values=avg_features["Energy"], range=[0, 1]),
            dict(label="Loudness", values=avg_features["Loudness"], range=[-60, 0]),
            dict(label="Valence", values=avg_features["Valence"], range=[0, 1]),
            dict(label="Danceability", values=avg_features["Danceability"], range=[0, 1]),
            dict(label="Acousticness", values=avg_features["Acousticness"], range=[0, 1])
        ]
    ))

    # Add a legend to display genre colors
    fig.update_layout(
        title="Audio Feature Comparison by Genre",
        height=600,
        title_font_size=20,
        title_x=0.5,
        font=dict(size=12),
        showlegend=True,
        legend=dict(
            itemsizing='constant',
            x=1.1,
            y=1
        )
    )

    # Add annotations as a legend workaround (hover doesn't work directly with Parcoords)
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color=list(genre_color_map.values())),
        legendgroup="Genres",
        showlegend=True,
        hoverinfo="text",
        text=list(genre_color_map.keys())
    ))

    return fig


@app.callback(
    Output('genre-bar', 'figure'),
    Input('genre-filter', 'value')
)
def update_genre_bar(selected_genres):
    # Filter data based on the selected genres
    filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df

    # Count the number of songs per genre
    genre_counts = filtered_df.groupby('Broad Genre')['Track Name'].count().reset_index()
    genre_counts.columns = ['Genre', 'Song Count']  # Rename columns for clarity

    # Sort the genres alphabetically for a clean presentation
    genre_counts = genre_counts.sort_values(by='Genre')

    # Define the color map for genres
    genre_color_map = {
        "Pop": "red",
        "Rock": "blue",
        "Hip-Hop": "purple",
        "Jazz": "orange",
        "Blues": "lightblue",
        "K-Pop": "pink",
        "Metal": "gray",
        "Punk": "green",
        "Electronic/Dance": "yellow",
        "Reggae": "brown",
        "Country": "gold",
        "Latin": "teal",
        "African": "darkgreen",
        "Other": "lightgray"
    }

    # Create a bar chart
    fig = px.bar(
        genre_counts,
        x="Song Count",
        y="Genre",
        orientation="h",
        title="Number of Songs by Genre",
        text="Song Count",
        color="Genre",  # Use Genre for color
        color_discrete_map=genre_color_map  # Apply the color mapping
    )

    # Customize the bar chart layout
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(
        xaxis_title="Number of Songs",
        yaxis_title="Genre",
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        height=600,
        margin=dict(t=50, l=100, r=50, b=50)  # Adjust margins for better spacing
    )

    return fig




# @app.callback(
#     Output('energy-valence-scatter', 'figure'),
#     Input('genre-filter', 'value')
# )
# def update_energy_valence(selected_genres):
#     # Filter data based on selected genres
#     filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df
#
#     # Create scatter plot with genres as color
#     fig = px.scatter(
#         filtered_df,
#         x="Energy",
#         y="Valence",
#         color="Broad Genre",  # Use Broad Genre for color mapping
#         size="Danceability",
#         hover_name="Track Name",
#         title="Energy vs Valence by Track Name & Genre",
#         color_discrete_map={
#             "Pop": "red",
#             "Rock": "blue",
#             "Hip-Hop": "purple",
#             "Jazz": "orange",
#             "Blues": "lightblue",
#             "K-Pop": "pink",
#             "Metal": "gray",
#             "Punk": "green",
#             "Electronic/Dance": "yellow",
#             "Reggae": "brown",
#             "Country": "gold",
#             "Latin": "teal",
#             "African": "darkgreen",
#             "Other": "lightgray"
#         }
#     )
#
#     # Update layout for improved readability
#     fig.update_traces(marker=dict(size=4, opacity=0.7))  # Reduce marker size and opacity
#     fig.update_layout(
#         dragmode='zoom',  # Enable zooming
#         xaxis={'title': 'Energy'},
#         yaxis={'title': 'Valence'},
#         legend_title="Genres",
#         height=800
#     )
#
#     return fig


# Callback for Time-Based Trends
@app.callback(
    Output('time-trends-line-chart', 'figure'),
    Input('genre-filter', 'value')
)
def update_time_trends(selected_genres):
    filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df
    filtered_df['Year'] = filtered_df['Release Date'].dt.year
    genre_time_data = filtered_df.groupby(['Year', 'Broad Genre'])['Track Name'].count().reset_index()
    genre_time_data.columns = ['Year', 'Genre', 'Track Count']

    fig = px.line(
        genre_time_data,
        x="Year",
        y="Track Count",
        color="Genre",
        title="Tracks Released Over Time by Genre",
        labels={"Track Count": "Number of Tracks Released", "Year": "Year"},
        color_discrete_map={
            "Pop": "red",
            "Rock": "blue",
            "Hip-Hop": "purple",
            "Jazz": "orange",
            "Blues": "lightblue",
            "K-Pop": "pink",
            "Metal": "gray",
            "Punk": "green",
            "Electronic/Dance": "yellow",
            "Reggae": "brown",
            "Country": "gold",
            "Latin": "teal",
            "African": "darkgreen",
            "Other": "lightgray"
        }
    )

    # Set static axis ranges
    fig.update_layout(
        xaxis=dict(range=[filtered_df['Year'].min(), filtered_df['Year'].max()], title="Year"),
        yaxis=dict(range=[0, genre_time_data['Track Count'].max()], title="Number of Tracks Released"),
        dragmode='zoom',
        height=600
    )

    return fig


# @app.callback(
#     Output('top-bands-songs-bar', 'figure'),
#     [Input('genre-filter', 'value'),
#      Input('year-filter', 'value')]
# )
# def update_top_bands_songs(selected_genres, selected_year):
#     """
#     Update the bar chart to show the top 10 bands by songs released in a selected year, colored by genre.
#     """
#     # Step 1: Copy the dataset to avoid modifying the original
#     filtered_df = df.copy()
#
#     # Step 2: Filter by genres if specified
#     if selected_genres:
#         filtered_df = filtered_df[filtered_df['Broad Genre'].isin(selected_genres)]
#
#     # Step 3: Extract the release year and filter by selected year
#     filtered_df['Year'] = filtered_df['Release Date'].dt.year
#     if selected_year:
#         filtered_df = filtered_df[filtered_df['Year'] == selected_year]
#
#     # Step 4: Group by band, genre, and count the number of songs
#     band_song_counts = (
#         filtered_df.groupby(['Band Name', 'Broad Genre'], as_index=False)
#         .agg({'Track Name': 'count'})
#         .rename(columns={'Track Name': 'Song Count', 'Broad Genre': 'Genre'})
#     )
#
#     # Step 5: Sort the bands by song count in descending order and pick the top 10
#     top_bands = band_song_counts.sort_values(by='Song Count', ascending=False).head(10)
#
#     # Step 6: If no data is available, return an empty figure
#     if top_bands.empty:
#         return go.Figure().update_layout(
#             title=f"No Data Available for {selected_year if selected_year else 'All Years'}",
#             xaxis=dict(title="Number of Songs"),
#             yaxis=dict(title="Band Name"),
#         )
#
#     # Step 7: Define a color map for genres
#     genre_color_map = {
#         "Pop": "red",
#         "Rock": "blue",
#         "Hip-Hop": "purple",
#         "Jazz": "orange",
#         "Blues": "lightblue",
#         "K-Pop": "pink",
#         "Metal": "gray",
#         "Punk": "green",
#         "Electronic/Dance": "yellow",
#         "Reggae": "brown",
#         "Country": "gold",
#         "Latin": "teal",
#         "African": "darkgreen",
#         "Other": "lightgray"
#     }
#
#     # Step 8: Create a vertical bar chart
#     fig = px.bar(
#         top_bands,
#         x="Song Count",
#         y="Band Name",
#         title=f"Top 10 Bands by Songs Released in {selected_year if selected_year else 'All Years'}",
#         labels={"Song Count": "Number of Songs", "Band Name": "Band"},
#         color="Genre",
#         color_discrete_map=genre_color_map  # Apply genre-based color mapping
#     )
#
#     # Step 9: Customize the chart layout for better readability
#     fig.update_layout(
#         xaxis=dict(title="Number of Songs", tickangle=-45),  # Rotate x-axis labels
#         yaxis=dict(title="Band Name"),
#         legend_title="Genre",
#         height=600
#     )
#
#     return fig


# @app.callback(
#     Output('dynamic-3d-scatter', 'figure'),
#     [Input('x-axis-feature', 'value'),
#      Input('y-axis-feature', 'value'),
#      # Input('z-axis-feature', 'value'),
#      Input('genre-filter', 'value')]
# )
# def update_dynamic_3d_scatter(x_feature, y_feature, selected_genres):
#     """
#     Create a dynamic 3D scatter plot for user-selected audio features.
#     """
#     # Filter data based on selected genres
#     filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df
#
#     # Check for valid feature selections
#     if not (x_feature and y_feature):
#         return go.Figure().update_layout(
#             title="Please select valid features for the axes",
#             height=600
#         )
#
#     # Create the 3D scatter plot
#     fig = px.scatter_3d(
#         filtered_df,
#         x=x_feature,
#         y=y_feature,
#         color='Broad Genre',
#         hover_name='Band Name',
#         title=f"3D Scatter Plot: {x_feature}, {y_feature}",
#         labels={x_feature: x_feature, y_feature: y_feature},
#         color_discrete_map={
#             "Pop": "red",
#             "Rock": "blue",
#             "Hip-Hop": "purple",
#             "Jazz": "orange",
#             "Blues": "lightblue",
#             "Metal": "gray",
#             "Punk": "green",
#             "Electronic/Dance": "yellow",
#             "Reggae": "brown",
#             "Country": "gold",
#             "Latin": "teal",
#             "African": "darkgreen",
#             "Other": "lightgray"
#         }
#     )
#
#     # Customize the layout
#     fig.update_layout(
#         scene=dict(
#             xaxis=dict(title=x_feature, range=[0, 1]),
#             yaxis=dict(title=y_feature, range=[0, 1])
#             # zaxis=dict(title=z_feature, range=[0, 1])
#         ),
#         margin=dict(l=0, r=0, b=0, t=50)
#     )
#
#     return fig

@app.callback(
    Output('sentiment-analysis', 'figure'),
    Input('genre-filter', 'value')
)
def sentiment_analysis_of_valence(selected_genres):
    """
    Perform sentiment analysis based on the valence attribute of tracks.
    """
    # Filter data by selected genres
    filtered_df = df[df['Broad Genre'].isin(selected_genres)] if selected_genres else df

    # Categorize valence into sentiment labels
    def categorize_valence(val):
        if val >= 0.7:
            return "Positive"
        elif val >= 0.3:
            return "Neutral"
        else:
            return "Negative"

    filtered_df['Sentiment'] = filtered_df['Valence'].apply(categorize_valence)

    # Aggregate sentiment counts per genre
    sentiment_counts = filtered_df.groupby(['Broad Genre', 'Sentiment'])['Track Name'].count().reset_index()
    sentiment_counts.columns = ['Genre', 'Sentiment', 'Track Count']

    # Create a grouped bar chart
    fig = px.bar(
        sentiment_counts,
        x="Genre",
        y="Track Count",
        color="Sentiment",
        title="Sentiment Analysis of Track Valence by Genre",
        barmode="group",
        labels={"Track Count": "Number of Tracks", "Genre": "Genre"},
        color_discrete_map={
            "Positive": "green",
            "Neutral": "orange",
            "Negative": "red"
        }
    )

    # Update layout for readability
    fig.update_layout(
        height=600,
        title_font_size=20,
        title_x=0.5,
        xaxis=dict(title="Genre", tickangle=-45),
        yaxis=dict(title="Number of Tracks"),
        legend_title="Sentiment"
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
