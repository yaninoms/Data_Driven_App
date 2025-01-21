import tkinter as tk
import customtkinter as ctk
import requests
import random
from PIL import Image, ImageTk
from io import BytesIO
import folium
import webview
import os

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Country Quiz Game")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # Game State
        self.current_question = None
        self.score = 0
        self.time_left = 0
        self.difficulty = None
        self.question_type = None
        self.questions_remaining = 0
        self.region = None

        # Pages
        self.main_menu()

    def set_background_image(self, image_path):
        # Load the background image
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((900, 700), Image.Resampling.LANCZOS)  # Resize to fit the window
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)

        # Add the image to a CTkLabel
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_image_tk, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch the image to fill the window

    def main_menu(self):
        self.clear_window()
        
        # Set your uploaded PNG as the background image
        self.set_background_image('wonderpals.png')  

        # Button Configuration
        button_width = 260
        button_height = 70

        play_game_image = Image.open("quiz-btn.png").resize((250, 80), Image.Resampling.LANCZOS)
        self.play_game_image_tk = ImageTk.PhotoImage(play_game_image)

        info_image = Image.open("info-btn.png").resize((250, 80), Image.Resampling.LANCZOS)
        self.info_image_tk = ImageTk.PhotoImage(info_image)

        viewer_image = Image.open("atlasbtn.png").resize((250, 80), Image.Resampling.LANCZOS)
        self.viewer_image_tk = ImageTk.PhotoImage(viewer_image)

        # Play Game Button
        self.play_button = ctk.CTkButton(
            self.root,
            text="",
            command=self.choose_question_type,
            image=self.play_game_image_tk,
            width=button_width,
            height=button_height,
            fg_color="#47250d",
            border_width=0,
            hover_color="#47250d"
        )
        self.play_button.place(x=40, y=506)  # Adjust coordinates to fit the design

        # Country Viewer Button
        self.viewer_button = ctk.CTkButton(
            self.root,
            text="",
            command=self.country_info_viewer,
            image=self.viewer_image_tk,
            width=button_width,
            height=button_height,
            fg_color="#47250d",
            border_width=0,
            hover_color="#47250d"
        )
        self.viewer_button.place(x=318, y=506)  # Adjust coordinates to fit the design

        #  Info Button
        self.info_button = ctk.CTkButton(
            self.root,
            text="",
            command=self.show_info,
            image=self.info_image_tk,
            width=button_width,
            height=button_height,
            fg_color="#47250d",
            border_width=0,
            hover_color="#47250d"
        )
        self.info_button.place(x=595, y=506)  # Adjust coordinates to fit the design

    def show_info(self):
        self.clear_window()
        self.set_background_image('info.png')

        button_width = 187
        button_height = 50

        back_image = Image.open("go-back.png").resize((187, 50), Image.Resampling.LANCZOS)
        self.back_image_tk = ImageTk.PhotoImage(back_image)

        self.back_button = ctk.CTkButton(
            self.root,
            width=button_width, 
            height=button_height, 
            text="", command=self.main_menu, 
            fg_color="#47250d",
            image=self.back_image_tk,
            hover_color="#47250d"
            )
        self.back_button.place(x=503, y=536)

    def country_info_viewer(self):
        self.clear_window()

        self.header_label = ctk.CTkLabel(self.root, text="Country Info Viewer", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.search_entry = ctk.CTkEntry(self.root, placeholder_text="Enter country name", width=300)
        self.search_entry.pack(pady=10)

        self.search_button = ctk.CTkButton(self.root, text="Search", command=self.fetch_country_info)
        self.search_button.pack(pady=10)

        self.search_button = ctk.CTkButton(self.root, text="Open Map", command=self.open_map)
        self.search_button.pack(pady=10)

        self.info_label = ctk.CTkLabel(self.root, text="",height=70, width=400, justify="left")
        self.info_label.pack(pady=30)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.main_menu)
        self.back_button.pack(pady=10)

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
        self.map_file = os.path.join(os.getcwd(), "map.html")
        m.save(self.map_file)  # Corrected this line

    def open_map(self):
        # Generate the map before attempting to open it
        self.generate_map()

        # Open the map if it was successfully created
        if hasattr(self, 'map_file') and os.path.exists(self.map_file):
            webview.create_window("Interactive Map", f"file://{os.path.abspath(self.map_file)}")
            webview.start()
        else:
            print("Error: Map file not found.")

    def fetch_country_info(self):
        country_name = self.search_entry.get().strip()
        if not country_name:
            self.info_label.configure(text="Please enter a country name.", text_color="red")
            return

        try:
            response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
            response.raise_for_status()
            country = response.json()[0]

            name = country.get('name', {}).get('common', 'Unknown')
            flag = country.get('flags', {}).get('png', 'Unknown')
            population = country.get('population', 'Unknown')
            region = country.get('region', 'Unknown')
            languages = ", ".join(country.get('languages', {}).values()) or 'Unknown'
            currencies = ", ".join(country.get('currencies', {}).keys()) or 'Unknown'

            info_text = (
                f"Name: {name}\n"
                f"Population: {population}\n"
                f"Region: {region}\n"
                f"Languages: {languages}\n"
                f"Currencies: {currencies}\n"
                f"Flag: \n"
            )

            self.info_label.configure(text=info_text)
            self.display_flag(flag)

        except Exception as e:
            self.info_label.configure(text=f"Error fetching country information: {e}", text_color="red")

    def display_flag(self, flag_url):
        try:
            response = requests.get(flag_url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            img = Image.open(image_data).resize((150, 100))
            flag_image = ImageTk.PhotoImage(img)

            # Clear previous flag if any
            if hasattr(self, 'flag_label'):
                self.flag_label.destroy()

            self.flag_label = tk.Label(self.root, image=flag_image)
            self.flag_label.image = flag_image
            self.flag_label.pack(pady=10)

        except Exception as e:
            self.info_label.configure(text=f"Error displaying flag: {e}", text_color="red")

    def choose_question_type(self):
        self.clear_window()
        self.set_background_image('1-game type.png')

        button_height = 310
        button_width = 214

        guessflag_image = Image.open("guessflag.png").resize((214, 310), Image.Resampling.LANCZOS)
        self.guessflag_image_tk = ImageTk.PhotoImage(guessflag_image)

        guesscap_image = Image.open("guesscap.png").resize((214,310), Image.Resampling.LANCZOS)
        self.guesscap_image_tk = ImageTk.PhotoImage(guesscap_image)

        guesscur_image = Image.open("guesscur.png").resize((214,310), Image.Resampling.LANCZOS)
        self.guesscur_image_tk = ImageTk.PhotoImage(guesscur_image)

        self.flag_button = ctk.CTkButton(
            self.root, text="", 
            command=lambda: self.choose_region("flag"),
            image= self.guessflag_image_tk,
            height= button_height,
            width=button_width,
            fg_color="#ffca53",
            hover_color="#f9a01b"
            )
        self.flag_button.place(x=50, y=178)

        self.capital_button = ctk.CTkButton(self.root, text="", 
            command=lambda: self.choose_region("capital"),
            height= button_height,
            width=button_width,
            image= self.guesscap_image_tk,
            fg_color="#ffca53",
            hover_color="#f9a01b")
        self.capital_button.place(x=336, y=178)

        self.currency_button = ctk.CTkButton(
            self.root, text="",
            command=lambda: self.choose_region("currency"),
            height= button_height,
            width=button_width,
            image= self.guesscur_image_tk,
            fg_color="#ffca53",
            hover_color="#f9a01b"
            )
        self.currency_button.place(x=620, y=178)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.main_menu)
        self.back_button.place(x=728, y=594)

    def choose_region(self, question_type):
        self.question_type = question_type
        self.clear_window()

        self.header_label = ctk.CTkLabel(self.root, text="Choose Region", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.international_button = ctk.CTkButton(self.root, text="International", command=lambda: self.start_game_with_region("international"))
        self.international_button.pack(pady=10)

        self.continent_button = ctk.CTkButton(self.root, text="By Continent", command=self.choose_continent)
        self.continent_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.choose_question_type)
        self.back_button.pack(pady=10)

    def choose_continent(self):
        self.clear_window()

        self.header_label = ctk.CTkLabel(self.root, text="Choose Continent", font=("Arial", 20))
        self.header_label.pack(pady=20)

        continents = ["Africa", "Americas", "Asia", "Europe", "Oceania"]
        for continent in continents:
            ctk.CTkButton(
                self.root, text=continent,
                command=lambda c=continent: self.start_game_with_region(c.lower())
            ).pack(pady=5)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.choose_region)
        self.back_button.pack(pady=10)

    def start_game_with_region(self, region):
        self.region = region
        self.choose_difficulty(self.question_type)

    def choose_difficulty(self, question_type):
        self.question_type = question_type
        self.clear_window()

        self.header_label = ctk.CTkLabel(self.root, text="Choose Difficulty", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.easy_button = ctk.CTkButton(self.root, text="Easy (2 minutes)", command=lambda: self.start_game("easy"))
        self.easy_button.pack(pady=10)

        self.normal_button = ctk.CTkButton(self.root, text="Normal (1 minute)", command=lambda: self.start_game("normal"))
        self.normal_button.pack(pady=10)

        self.advanced_button = ctk.CTkButton(self.root, text="Advanced (30 seconds)", command=lambda: self.start_game("advanced"))
        self.advanced_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.choose_region)
        self.back_button.pack(pady=10)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.questions_remaining = 10
        self.time_left = {"easy": 120, "normal": 60, "advanced": 30}[difficulty]
        self.clear_window()
        self.setup_game_ui()
        self.fetch_new_question()
        self.update_timer()

    def setup_game_ui(self):
        self.timer_label = ctk.CTkLabel(self.root, text=f"Time Left: {self.time_left}s", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.score_label = ctk.CTkLabel(self.root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack(pady=10)

        self.question_label = ctk.CTkLabel(self.root, text="", font=("Arial", 16), wraplength=500, justify="center")
        self.question_label.pack(pady=20)

        self.answer_entry = ctk.CTkEntry(self.root, placeholder_text="Your Answer", width=300)
        self.answer_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self.root, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.feedback_label = ctk.CTkLabel(self.root, text="", font=("Arial", 14))
        self.feedback_label.pack(pady=10)

    def fetch_new_question(self):
        if self.questions_remaining <= 0:
            self.end_game()
            return

        try:
            response = requests.get("https://restcountries.com/v3.1/all")
            response.raise_for_status()
            countries = response.json()

            # Randomly select a country
            country = random.choice(countries)
            self.current_question = {
                "name": country.get("name", {}).get("common", "Unknown"),
                "flag": country.get("flags", {}).get("png", ""),
                "capital": ", ".join(country.get("capital", [])) or "Unknown",
                "currency": ", ".join(country.get("currencies", {}).keys()) or "Unknown",
            }

            # Display question based on the question type
            if self.question_type == "flag":
                self.question_label.configure(text="Which country has this flag?")
                self.display_flag(self.current_question["flag"])
            elif self.question_type == "capital":
                self.question_label.configure(text=f"What is the country with the capital: {self.current_question['capital']}?")
            elif self.question_type == "currency":
                self.question_label.configure(text=f"Which country's currency is: {self.current_question['currency']}?")

        except Exception as e:
            self.feedback_label.configure(text=f"Error fetching question: {e}", text_color="red")

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        if user_answer == self.current_question["name"].lower():
            self.score += 1
            self.feedback_label.configure(text="Correct!", text_color="green")
        else:
            self.feedback_label.configure(text=f"Incorrect! The correct answer was {self.current_question['name']}.", text_color="red")

        self.questions_remaining -= 1
        self.score_label.configure(text=f"Score: {self.score}")
        self.answer_entry.delete(0, tk.END)

        self.fetch_new_question()

    def update_timer(self):
        if self.time_left <= 0:
            self.end_game()
            return

        self.time_left -= 1
        self.timer_label.configure(text=f"Time Left: {self.time_left}s")
        self.root.after(1000, self.update_timer)

    def end_game(self):
        self.clear_window()
        self.header_label = ctk.CTkLabel(self.root, text=f"Game Over! Your Score: {self.score}", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.play_again_button = ctk.CTkButton(self.root, text="Play Again", command=self.main_menu)
        self.play_again_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = QuizApp(root)
    root.mainloop()
