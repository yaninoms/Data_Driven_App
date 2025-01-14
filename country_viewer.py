import customtkinter as ctk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# Your Exchange Rates API key
EXCHANGE_API_KEY = "your_api_key_here"

class CountryInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Country Information Viewer")
        self.root.geometry("800x650")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Main Frame for Clean Layout
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title Label
        self.title_label = ctk.CTkLabel(self.main_frame, text="Country Information Viewer", font=("Arial", 24, "bold"), text_color="blue")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # Country Dropdown
        self.country_label = ctk.CTkLabel(self.main_frame, text="Select Country:", font=("Arial", 14))
        self.country_label.grid(row=1, column=0, sticky="w", padx=10)

        self.country_dropdown = ctk.CTkComboBox(self.main_frame, width=300, values=[], command=self.on_country_select)
        self.country_dropdown.grid(row=1, column=1, columnspan=2, pady=10)

        # Fetch Country Data Button
        self.fetch_button = ctk.CTkButton(self.main_frame, text="Fetch Country Info", command=self.fetch_country_info, width=150)
        self.fetch_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Flag Display Section
        self.flag_label = ctk.CTkLabel(self.main_frame, text="Flag will appear here", font=("Arial", 12), text_color="gray")
        self.flag_label.grid(row=3, column=0, columnspan=3, pady=15)

        # Country Info Labels
        self.info_label = ctk.CTkLabel(self.main_frame, text="Country Info will be displayed here.", font=("Arial", 14))
        self.info_label.grid(row=4, column=0, columnspan=3, pady=10)

        # Additional Information
        self.languages_label = ctk.CTkLabel(self.main_frame, text="Languages Spoken:", font=("Arial", 12))
        self.languages_label.grid(row=5, column=0, sticky="w", padx=10)

        self.languages_info = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 12), text_color="gray")
        self.languages_info.grid(row=5, column=1, columnspan=2, pady=5)

        self.population_label = ctk.CTkLabel(self.main_frame, text="Population:", font=("Arial", 12))
        self.population_label.grid(row=6, column=0, sticky="w", padx=10)

        self.population_info = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 12), text_color="gray")
        self.population_info.grid(row=6, column=1, columnspan=2, pady=5)

        self.region_label = ctk.CTkLabel(self.main_frame, text="Region & Subregion:", font=("Arial", 12))
        self.region_label.grid(row=7, column=0, sticky="w", padx=10)

        self.region_info = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 12), text_color="gray")
        self.region_info.grid(row=7, column=1, columnspan=2, pady=5)

        # Currency Conversion Section
        self.currency_label = ctk.CTkLabel(self.main_frame, text="Currency Conversion:", font=("Arial", 12))
        self.currency_label.grid(row=8, column=0, sticky="w", padx=10)

        self.currency_entry = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="Amount in local currency", font=("Arial", 12))
        self.currency_entry.grid(row=8, column=1, pady=10)

        self.convert_button = ctk.CTkButton(self.main_frame, text="Convert to USD", command=self.convert_currency, width=150)
        self.convert_button.grid(row=8, column=2, pady=10)

        # Populate country dropdown
        self.fetch_countries()

    def fetch_countries(self):
        """Fetch country data and populate the dropdown."""
        try:
            response = requests.get("https://restcountries.com/v3.1/all")
            response.raise_for_status()
            countries = response.json()

            country_names = [country.get("name", {}).get("common", "Unknown") for country in countries]
            self.country_dropdown.configure(values=country_names)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch countries: {e}")

    def on_country_select(self, selected_country):
        """Reset information when a new country is selected."""
        self.info_label.configure(text="")
        self.flag_label.configure(image=None, text="Flag will appear here.")
        self.languages_info.configure(text="")
        self.population_info.configure(text="")
        self.region_info.configure(text="")

    def fetch_country_info(self):
        """Fetch and display country information."""
        selected_country = self.country_dropdown.get()

        try:
            # Fetch country data
            url = f"https://restcountries.com/v3.1/name/{selected_country}?fullText=true"
            response = requests.get(url)
            response.raise_for_status()
            country_data = response.json()[0]

            country_name = country_data["name"]["common"]
            capital = country_data.get("capital", ["Unknown"])[0]
            region = country_data.get("region", "Unknown")
            subregion = country_data.get("subregion", "Unknown")
            population = country_data.get("population", "Unknown")
            languages = ", ".join(country_data.get("languages", {}).values())

            # Display the country information
            self.info_label.configure(text=f"Name: {country_name}\nCapital: {capital}")
            self.languages_info.configure(text=f"Languages: {languages}")
            self.population_info.configure(text=f"Population: {population:,}")
            self.region_info.configure(text=f"Region: {region}, Subregion: {subregion}")

            # Display the flag
            flag_url = country_data["flags"]["png"]
            self.display_flag(flag_url)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch country data: {e}")

    # Display the flag
    def display_flag(self, flag_url):
        """Display the flag of the country."""
        try:
            response = requests.get(flag_url)
            response.raise_for_status()
            flag_image = Image.open(BytesIO(response.content))
            flag_image = flag_image.resize((300, 200), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
            flag_photo = ImageTk.PhotoImage(flag_image)

            self.flag_label.configure(image=flag_photo, text="")
            self.flag_label.image = flag_photo  # Keep reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load flag image: {e}")


    def convert_currency(self):
        """Convert the selected country's currency to USD."""
        selected_country = self.country_dropdown.get()

        try:
            # Fetch country data
            url = f"https://restcountries.com/v3.1/name/{selected_country}?fullText=true"
            response = requests.get(url)
            response.raise_for_status()
            country_data = response.json()[0]

            country_currency = list(country_data.get("currencies", {}).keys())[0]
            amount = float(self.currency_entry.get())

            # Fetch exchange rates from the API
            exchange_url = f"https://open.er-api.com/v6/latest/{country_currency}"
            exchange_response = requests.get(exchange_url, headers={"apikey": EXCHANGE_API_KEY})
            exchange_response.raise_for_status()
            exchange_data = exchange_response.json()

            # Convert to USD
            if "rates" in exchange_data and "USD" in exchange_data["rates"]:
                exchange_rate = exchange_data["rates"]["USD"]
                converted_amount = amount * exchange_rate
                messagebox.showinfo("Currency Conversion", f"{amount} {country_currency} = {converted_amount:.2f} USD")
            else:
                messagebox.showerror("Error", "Exchange rate not found.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert currency: {e}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = CountryInfoApp(root)
    root.mainloop()
