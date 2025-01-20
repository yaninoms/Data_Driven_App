import customtkinter as ctk
import requests
import folium
import os
import webview

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
        self.generate_map()

    def generate_map(self):
        # Create a folium map
        m = folium.Map(location=[20, 0], zoom_start=2)

        # Fetch GeoJSON data
        try:
            response = requests.get("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson")
            response.raise_for_status()
            countries_geojson = response.json()
        except requests.RequestException as e:
            print(f"Error fetching GeoJSON data: {e}")
            return

        # Add GeoJSON to the map
        folium.GeoJson(
            countries_geojson,
            style_function=lambda x: {"fillColor": "blue", "color": "black", "weight": 1},
            highlight_function=lambda x: {"weight": 3, "color": "green"},
            tooltip=folium.GeoJsonTooltip(fields=["ADMIN"], aliases=["Country:"]),
        ).add_to(m)

        # Save the map as an HTML file
        map_file = os.path.join(os.getcwd(), "map.html")
        m.save(map_file)

        # Open the map in a pywebview window
        webview.create_window("Interactive Map", f"file://{os.path.abspath(map_file)}")
        webview.start()

    def convert_currency(self):
        """Convert local currency to USD."""
        try:
            amount = float(self.currency_entry.get())
            self.result_label.configure(text=f"Converted Amount: {amount * 0.27:.2f} USD")  # Example conversion
        except ValueError:
            self.result_label.configure(text="Invalid amount entered.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = InteractiveMapApp(root)
    root.mainloop()
