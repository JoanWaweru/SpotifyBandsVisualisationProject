import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os

# Set up Spotipy credentials
client_credentials_manager = SpotifyClientCredentials(client_id="afc0ff7212974456aa59e6f70db640d2",
                                                      client_secret="40a338c6eb524b4196d01ac62f3de6b0")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# List of artists to search
artist_names = [
    # Rock Bands
    "The Beatles", "Led Zeppelin", "Pink Floyd", "The Rolling Stones", "Queen",
    "AC/DC", "Metallica", "Guns N' Roses", "The Who", "Nirvana", "Aerosmith",
    "Foo Fighters", "The Eagles", "Green Day", "The Doors", "Radiohead", "U2",
    "Pearl Jam", "Red Hot Chili Peppers", "The Clash", "The Kinks", "The Beach Boys",

    # Pop Bands
    "BTS", "Blackpink", "One Direction", "Why Don't We", "The Vamps", "The Wanted", "Jonas Brothers", "Little Mix",
    "Spice Girls", "The 1975", "Backstreet Boys", "Westlife", "*NSYNC", "Fifth Harmony", "The Pussycat Dolls", "Destiny's Child",
    "ABBA", "Jackson 5", "Take That", "Girls Aloud", "Prettymuch", "Sugababes",

    # Metal Bands
    "Iron Maiden", "Slayer", "Megadeth", "Judas Priest", "Black Sabbath",
    "Pantera", "System of a Down", "Anthrax", "Lamb of God", "Sepultura",
    "Slipknot", "Avenged Sevenfold", "Metallica", "Tool", "Dream Theater",

    # Jazz Bands
    "Snarky Puppy", "The Manhattan Transfer", "Weather Report", "The Modern Jazz Quartet",
    "Count Basie Orchestra", "The Dave Brubeck Quartet", "The Bad Plus", "Pat Metheny Group",
    "Yellowjackets", "The Jazz Messengers", "Oregon",

    # Alternative and Indie Bands
    "Radiohead", "Arctic Monkeys", "Red Hot Chili Peppers", "Imagine Dragons",
    "Florence and the Machine", "The Killers", "The Strokes", "The Black Keys",
    "Tame Impala", "Vampire Weekend", "The National", "Arcade Fire", "Bon Iver",
    "Modest Mouse", "Phoenix", "Of Monsters and Men", "Mumford & Sons",

    # Blues Bands
    "The Allman Brothers Band", "Stevie Ray Vaughan and Double Trouble", "ZZ Top",
    "Blues Traveler", "The Black Crowes", "Tedeschi Trucks Band", "Kenny Wayne Shepherd Band",
    "North Mississippi Allstars", "The Fabulous Thunderbirds",

    # K-pop Bands
    "BTS", "Blackpink", "EXO", "TWICE", "Red Velvet", "SEVENTEEN", "NCT", "Stray Kids",
    "ATEEZ", "GOT7", "SHINee", "Girls' Generation", "Monsta X", "Super Junior", "2NE1",
    "MAMAMOO", "ITZY", "Big Bang",

    # Punk Bands
    "Green Day", "The Clash", "Ramones", "Blink-182", "The Sex Pistols",
    "Bad Religion", "NOFX", "The Offspring", "Dead Kennedys", "Rancid",
    "Misfits", "Descendents", "Black Flag", "Social Distortion", "Pennywise",

    # Hip-Hop and Rap Groups
    "The Sugarhill Gang", "Run-D.M.C.", "N.W.A", "Beastie Boys", "OutKast",
    "A Tribe Called Quest", "Wu-Tang Clan", "Public Enemy", "Bone Thugs-N-Harmony",
    "Migos", "The Roots", "Cypress Hill", "De La Soul", "Fugees", "G-Unit",
    "Three 6 Mafia", "Mobb Deep", "Salt-N-Pepa",

    # Electronic/Dance Bands
    "Daft Punk", "The Chemical Brothers", "The Prodigy", "Swedish House Mafia",
    "Disclosure", "Justice", "Major Lazer", "The Chainsmokers", "Underworld", "Above & Beyond",
    "The Crystal Method", "Deadmau5", "Boards of Canada", "Röyksopp",
    "Kraftwerk", "Depeche Mode", "Faithless",

    # Reggae Bands
    "Bob Marley and The Wailers", "Steel Pulse", "Toots and the Maytals",
    "Black Uhuru", "UB40", "Inner Circle", "The Mighty Diamonds",
    "Third World", "Culture", "The Skatalites", "SOJA", "Rebelution",
    "Iration", "Groundation", "Slightly Stoopid",

    # Latin and Reggaeton Groups
    "Gente de Zona", "Calle 13", "Aventura", "Bomba Estéreo",
    "Los Tigres del Norte", "La Sonora Dinamita", "Orishas", "Los Fabulosos Cadillacs",
    "Los Ángeles Azules", "Maná", "Buena Vista Social Club", "CNCO",
    "Grupo Niche", "Café Tacvba", "Bachata Heightz",

    # Country Bands
    "Zac Brown Band", "Lady A", "Florida Georgia Line", "Little Big Town",
    "Old Dominion", "The Band Perry", "Rascal Flatts", "Brooks & Dunn",
    "The Chicks", "Lonestar", "Alabama", "Sugarland", "Diamond Rio",
    "Maddie & Tae", "Parmalee"
    
    # African Bands
    "P-Square", "Tinariwen", "Sauti Sol", "Wanavokali", "H_Art the Band", "Elani",
    "Mighty Popo", "Ladysmith Black Mambazo", "Freshlyground", "Mafikizolo", "Stimela", "Gnawa Diffusion",
    "El Tanbura", "Wenge Musica", "Staff Benda Bilili", "Magic System"
    
    #Classical Bands
    "2Cellos", "The Piano Guys", "Apocalyptica", "Bond", "Emerson, Lake & Palmer",
    "Electric Light Orchestra (ELO)", "Nightwish", "Berlin Philharmonic Orchestra",
    "The Kronos Quartet", "Vienna Philharmonic", "London Symphony Orchestra",
    "The Swingle Singers", "Canadian Brass", "The King's Singers", "Academy of St Martin in the Fields"

]

# # Limit the number of albums and tracks to fetch for each artist
MAX_ALBUMS = 5
MAX_TRACKS_PER_ALBUM = 5

# Cache file
CACHE_FILE = "spotify_cache.json"

# Load cache if available and valid
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r") as f:
            spotify_data = json.load(f)
    except json.JSONDecodeError:
        print("Cache file is corrupted. Starting with an empty cache.")
        spotify_data = {}
else:
    spotify_data = {}

# Fetch data for each artist
for name in artist_names:
    if name in spotify_data:
        print(f"Using cached data for artist: {name}")
        continue

    results = sp.search(q="artist:" + name, type="artist", limit=1)
    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]
        artist_id = artist["id"]

        # Store essential artist information
        spotify_data[name] = {
            "name": artist["name"],
            "id": artist_id,
            "followers": artist["followers"]["total"],
            "popularity": artist["popularity"],
            "genres": artist["genres"],
            "albums": []
        }

        # Fetch a limited number of albums
        albums = sp.artist_albums(artist_id, album_type="album", limit=MAX_ALBUMS)
        for album in albums['items']:
            album_id = album['id']
            album_name = album['name']

            # Store essential album information
            album_data = {
                "album_name": album_name,
                "release_date": album["release_date"],
                "total_tracks": album["total_tracks"],
                "tracks": []
            }

            # Fetch a limited number of tracks in the album
            album_tracks = sp.album_tracks(album_id, limit=MAX_TRACKS_PER_ALBUM)
            track_ids = [track["id"] for track in album_tracks["items"]]

            # Batch fetch audio features for all tracks in the album
            audio_features = sp.audio_features(track_ids)

            for track, features in zip(album_tracks["items"], audio_features):
                if features:  # Check that audio features exist
                    track_data = {
                        "track_name": track["name"],
                        "track_id": track["id"],
                        "popularity": track.get("popularity", None),  # Popularity may not always be available
                        "audio_features": {
                            "acousticness": features["acousticness"],
                            "danceability": features["danceability"],
                            "energy": features["energy"],
                            "instrumentalness": features["instrumentalness"],
                            "liveness": features["liveness"],
                            "loudness": features["loudness"],
                            "speechiness": features["speechiness"],
                            "tempo": features["tempo"],
                            "valence": features["valence"]
                        }
                    }
                    album_data["tracks"].append(track_data)

            spotify_data[name]["albums"].append(album_data)

        print(f"Data fetched for artist: {name}")

        # Update the cache after each artist to avoid losing data if interrupted
        with open(CACHE_FILE, "w") as f:
            json.dump(spotify_data, f, indent=4)

print("All data has been saved to spotify_cache.json")