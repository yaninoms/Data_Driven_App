import customtkinter as ctk
from tkinterweb import HtmlFrame  # To embed folium map in Tkinter
import requests
import folium
import os

class InteractiveMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Country Viewer")
        self.root.geometry("1000x700")
        ctk.set_appearance_mode("Dark")

        # Main Layout
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Sidebar for Country Information
        self.sidebar = ctk.CTkFrame(self.main_frame, width=300)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.info_label = ctk.CTkLabel(self.sidebar, text="Select a country on the map", font=("Arial", 16, "bold"))
        self.info_label.pack(pady=10)

        self.flag_label = ctk.CTkLabel(self.sidebar, text="Flag will appear here", text_color="gray")
        self.flag_label.pack(pady=10)

        self.details_label = ctk.CTkLabel(self.sidebar, text="", justify="left")
        self.details_label.pack(pady=10)

        # Currency Conversion Section
        self.currency_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Amount in local currency")
        self.currency_entry.pack(pady=5)

        self.convert_button = ctk.CTkButton(self.sidebar, text="Convert to USD", command=self.convert_currency)
        self.convert_button.pack(pady=5)

        self.result_label = ctk.CTkLabel(self.sidebar, text="")
        self.result_label.pack(pady=5)

        # Map Area
        self.map_frame = HtmlFrame(self.main_frame)
        self.map_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Generate the map
        self.generate_map()


    def generate_map(self):
        """Generate a folium map and embed it into the Tkinter app."""
        # Create a folium map
        m = folium.Map(location=[20, 0], zoom_start=2)

        # Load country GeoJSON data
        response = requests.get("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson")
        if response.status_code != 200:
            print("Error fetching GeoJSON data:", response.status_code)
            return

        countries_geojson = response.json()

        # Add GeoJSON layer to the map
        def on_click_callback(feature):
            country_name = feature["properties"]["ADMIN"]
            return f"<b>{country_name}</b><br>Click <a href='#' onclick='window.countrySelected(\"{country_name}\")'>here</a> for details."

        folium.GeoJson(
            countries_geojson,
            style_function=lambda x: {"fillColor": "blue", "color": "black", "weight": 1},
            highlight_function=lambda x: {"weight": 3, "color": "green"},
            tooltip=folium.GeoJsonTooltip(fields=["ADMIN"], aliases=["Country:"]),
            popup=folium.GeoJsonPopup(
                fields=["ADMIN"],
                aliases=["Country:"],
                labels=True,
            ),
        ).add_to(m)

        # Save the map as an HTML file
        map_path = os.path.abspath("map.html")
        m.save(map_path)
        print(f"Map saved at {map_path}")

        # Ensure the correct file path is being loaded
        if os.path.exists(map_path):
            self.map_frame.load_file(map_path)
        else:
            print("Error: map.html not found!")


    def fetch_country_info(self, country_name):
        """Fetch country details from the REST Countries API."""
        try:
            url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
            response = requests.get(url)
            response.raise_for_status()
            country_data = response.json()[0]

            # Extract country details
            flag_url = country_data["flags"]["png"]
            capital = country_data.get("capital", ["Unknown"])[0]
            region = country_data.get("region", "Unknown")
            population = country_data.get("population", "Unknown")

            # Update the sidebar
            self.info_label.configure(text=f"Country: {country_name}")
            self.details_label.configure(text=f"Capital: {capital}\nRegion: {region}\nPopulation: {population:,}")
            self.display_flag(flag_url)

        except Exception as e:
            self.info_label.configure(text=f"Error: {e}")

    def display_flag(self, flag_url):
        """Display the flag image."""
        try:
            response = requests.get(flag_url)
            response.raise_for_status()
            image_data = response.content

            with open("flag.png", "wb") as f:
                f.write(image_data)

            flag_image = ctk.CTkImage("flag.png", size=(200, 120))
            self.flag_label.configure(image=flag_image, text="")
            self.flag_label.image = flag_image  # Prevent garbage collection
        except Exception as e:
            self.flag_label.configure(text="Error loading flag", image=None)

    def convert_currency(self):
        """Convert local currency to USD."""
        try:
            amount = float(self.currency_entry.get())
            # Use your exchange API logic here (dummy rate: 0.27)
            self.result_label.configure(text=f"Converted Amount: {amount * 0.27:.2f} USD")
        except ValueError:
            self.result_label.configure(text="Invalid amount entered.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = InteractiveMapApp(root)
    root.mainloop()
