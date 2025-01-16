import tkinter as tk
import customtkinter as ctk
import requests
import random
from PIL import Image, ImageTk
from io import BytesIO

# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Country Quiz Game")
        self.root.geometry("600x500")

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

    def main_menu(self):
        self.clear_window()

        # Main Menu Components
        self.header_label = ctk.CTkLabel(self.root, text="Country Quiz Game", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.play_button = ctk.CTkButton(self.root, text="Play Game", command=self.choose_question_type)
        self.play_button.pack(pady=10)

        self.info_button = ctk.CTkButton(self.root, text="Information", command=self.show_info)
        self.info_button.pack(pady=10)

        self.country_info_button = ctk.CTkButton(self.root, text="Country Info Viewer", command=self.country_info_viewer)
        self.country_info_button.pack(pady=10)

    def show_info(self):
        self.clear_window()

        info_text = (
            "Welcome to the Country Quiz Game!\n\n"
            "Choose from three exciting question types:\n"
            "1. Guess the Flag\n"
            "2. Guess the Country by Capital\n"
            "3. Guess the Currency\n\n"
            "You can select a difficulty level that determines the time limit:\n"
            "- Easy: 2 minutes\n"
            "- Normal: 1 minute\n"
            "- Advanced: 30 seconds\n\n"
            "Try to answer 10 questions and achieve the highest score!"
        )

        self.info_label = ctk.CTkLabel(self.root, text=info_text, justify="left", wraplength=500)
        self.info_label.pack(pady=20)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.main_menu)
        self.back_button.pack(pady=10)

    def country_info_viewer(self):
        self.clear_window()

        self.header_label = ctk.CTkLabel(self.root, text="Country Info Viewer", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.search_entry = ctk.CTkEntry(self.root, placeholder_text="Enter country name", width=300)
        self.search_entry.pack(pady=10)

        self.search_button = ctk.CTkButton(self.root, text="Search", command=self.fetch_country_info)
        self.search_button.pack(pady=10)

        self.info_label = ctk.CTkLabel(self.root, text="", justify="left", wraplength=500)
        self.info_label.pack(pady=20)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.main_menu)
        self.back_button.pack(pady=10)

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

        self.header_label = ctk.CTkLabel(self.root, text="Choose Question Type", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.flag_button = ctk.CTkButton(self.root, text="Guess the Flag", command=lambda: self.choose_region("flag"))
        self.flag_button.pack(pady=10)

        self.capital_button = ctk.CTkButton(self.root, text="Guess the Country by Capital", command=lambda: self.choose_region("capital"))
        self.capital_button.pack(pady=10)

        self.currency_button = ctk.CTkButton(self.root, text="Guess the Currency", command=lambda: self.choose_region("currency"))
        self.currency_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.main_menu)
        self.back_button.pack(pady=10)

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
