import folium
import requests
import customtkinter as ctk
from tkinterweb import HtmlFrame  # For embedding the HTML map

# Step 1: Generate the interactive map
def generate_map():
    # Create a base map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")

    # Fetch GeoJSON data for countries
    geojson_url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    response = requests.get(geojson_url)
    countries_geojson = response.json()

    # Function to fetch details from the REST Countries API
    def fetch_country_details(country_name):
        try:
            url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
            response = requests.get(url)
            response.raise_for_status()
            country_data = response.json()[0]

            # Extract details
            capital = country_data.get("capital", ["Unknown"])[0]
            population = country_data.get("population", "Unknown")
            region = country_data.get("region", "Unknown")
            subregion = country_data.get("subregion", "Unknown")

            return f"Country: {country_name}\nCapital: {capital}\nPopulation: {population:,}\nRegion: {region}, Subregion: {subregion}"
        except Exception as e:
            return f"Details not available for {country_name}. Error: {e}"

    # Add GeoJSON layer with click functionality
    def on_click_callback(feature):
        country_name = feature["properties"]["ADMIN"]
        return fetch_country_details(country_name)

    folium.GeoJson(
        countries_geojson,
        style_function=lambda x: {"fillColor": "blue", "color": "black", "weight": 1},
        highlight_function=lambda x: {"weight": 3, "color": "green"},
        tooltip=folium.GeoJsonTooltip(fields=["ADMIN"], aliases=["Country:"]),
        popup=folium.GeoJsonPopup(
            fields=["ADMIN"],
            labels=True,
            localize=True,
            parse_html=False,
            popup_function=lambda feature: on_click_callback(feature),
        ),
    ).add_to(m)

    # Save the map to an HTML file
    m.save("interactive_map.html")
    print("Map has been generated and saved as interactive_map.html")

# Step 2: Embed the map in a CustomTkinter GUI
class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Map Viewer")
        self.root.geometry("900x700")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Main Frame for the GUI layout
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title Label
        self.title_label = ctk.CTkLabel(self.main_frame, text="Interactive Map Viewer", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # HTML Frame to display the map
        self.map_frame = HtmlFrame(self.main_frame, horizontal_scrollbar="auto")
        self.map_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load the generated map into the HTML frame
        self.map_frame.load_file("interactive_map.html")

# Generate the map first
generate_map()

# Create the GUI application
if __name__ == "__main__":
    root = ctk.CTk()
    app = MapApp(root)
    root.mainloop()
