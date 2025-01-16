import customtkinter as ctk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO


class CountryDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Country Information Dashboard")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Frame Layout
        self.frame = ctk.CTkFrame(root, corner_radius=10)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(self.frame, text="Country Information Viewer", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)

        # Country Selection
        self.country_frame = ctk.CTkFrame(self.frame)
        self.country_frame.pack(pady=10, fill="x", padx=20)

        self.country_label = ctk.CTkLabel(self.country_frame, text="Select Country:", font=("Helvetica", 16))
        self.country_label.pack(side="left", padx=10)

        self.country_entry = ctk.CTkComboBox(self.country_frame, width=300, font=("Helvetica", 14))
        self.country_entry.pack(side="left", padx=10)
        self.country_entry.set("united arab emirates")  # Default value

        self.fetch_button = ctk.CTkButton(self.country_frame, text="Fetch Country Info", command=self.fetch_country_info)
        self.fetch_button.pack(side="left", padx=10)

        # Country Flag
        self.flag_label = ctk.CTkLabel(self.frame, text="", width=300, height=200, corner_radius=10)
        self.flag_label.pack(pady=20)

        # Info Section
        self.info_frame = ctk.CTkFrame(self.frame)
        self.info_frame.pack(pady=10, fill="x", padx=20)

        self.info_label = ctk.CTkLabel(self.info_frame, text="", font=("Helvetica", 14), justify="left")
        self.info_label.pack(padx=20, pady=10)

        # Currency Conversion
        self.currency_frame = ctk.CTkFrame(self.frame)
        self.currency_frame.pack(pady=20, fill="x", padx=20)

        self.currency_label = ctk.CTkLabel(self.currency_frame, text="Currency Conversion:", font=("Helvetica", 16))
        self.currency_label.pack(side="left", padx=10)

        self.currency_entry = ctk.CTkEntry(self.currency_frame, width=200, placeholder_text="Enter amount")
        self.currency_entry.pack(side="left", padx=10)

        self.convert_button = ctk.CTkButton(self.currency_frame, text="Convert to USD", command=self.convert_currency)
        self.convert_button.pack(side="left", padx=10)

        self.currency_result_label = ctk.CTkLabel(self.frame, text="", font=("Helvetica", 16, "bold"), text_color="green")
        self.currency_result_label.pack(pady=10)

    def fetch_country_info(self):
        country_name = self.country_entry.get().strip()
        if not country_name:
            messagebox.showerror("Error", "Please enter a country name!")
            return

        # Fetch country data
        try:
            response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
            response.raise_for_status()
            country_data = response.json()[0]

            # Update flag
            flag_url = country_data["flags"]["png"]
            flag_response = requests.get(flag_url)
            flag_image = Image.open(BytesIO(flag_response.content))
            flag_image = flag_image.resize((300, 200), Image.Resampling.LANCZOS)
            flag_photo = ImageTk.PhotoImage(flag_image)
            self.flag_label.configure(image=flag_photo, text="")
            self.flag_label.image = flag_photo

            # Update info
            country_info = f"""
            Name: {country_data['name']['common']}
            Capital: {country_data.get('capital', ['N/A'])[0]}
            Languages: {', '.join(country_data['languages'].values())}
            Population: {country_data['population']:,}
            Region: {country_data['region']}, Subregion: {country_data.get('subregion', 'N/A')}
            Currency: {list(country_data['currencies'].keys())[0]}
            """
            self.info_label.configure(text=country_info)

            # Store currency code
            self.currency_code = list(country_data['currencies'].keys())[0]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch country information: {e}")

    def convert_currency(self):
        amount = self.currency_entry.get().strip()
        if not amount.isdigit():
            self.currency_result_label.configure(text="Invalid amount! Please enter a number.", text_color="red")
            return

        amount = float(amount)
        if not hasattr(self, "currency_code"):
            self.currency_result_label.configure(text="Fetch country info first!", text_color="red")
            return

        try:
            # Fetch exchange rate
            api_key = "your_exchange_rate_api_key"
            response = requests.get(f"https://open.er-api.com/v6/latest/{self.currency_code}?apikey={api_key}")
            response.raise_for_status()
            exchange_data = response.json()

            # Calculate conversion
            usd_rate = exchange_data["rates"]["USD"]
            converted_amount = amount * usd_rate
            self.currency_result_label.configure(
                text=f"{amount} {self.currency_code} = {converted_amount:.2f} USD",
                text_color="green"
            )
        except Exception as e:
            self.currency_result_label.configure(text=f"Failed to convert currency: {e}", text_color="red")


if __name__ == "__main__":
    root = ctk.CTk()
    app = CountryDashboardApp(root)
    root.mainloop()
