import tkinter as tk
import customtkinter as ctk
import requests
import random

# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Country Quiz Game")
        self.root.geometry("600x400")
        
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

    def update_timer(self):
        if self.time_left > 0 and self.questions_remaining > 0:
            self.time_left -= 1
            self.timer_label.configure(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        elif self.questions_remaining == 0:
            self.end_game()
        else:
            self.feedback_label.configure(text="Time's up!", text_color="red")
            self.end_game()

    def fetch_new_question(self):
        try:
            url = "https://restcountries.com/v3.1/all"
            if self.region and self.region != "international":
                url = f"https://restcountries.com/v3.1/region/{self.region}"

            response = requests.get(url)
            response.raise_for_status()
            countries = response.json()
            country = random.choice(countries)

            if self.question_type == "capital":
                self.current_question = {
                    "question": f"What is the capital of {country['name']['common']}?",
                    "answer": country.get("capital", ["Unknown"])[0]
                }
            elif self.question_type == "flag":
                self.current_question = {
                    "question": f"Which country does this flag belong to?",
                    "answer": country['name']['common'],
                    "flag": country['flags']['png']
                }
            elif self.question_type == "currency":
                currencies = list(country.get("currencies", {}).keys())
                self.current_question = {
                    "question": f"What is the currency of {country['name']['common']}?",
                    "answer": currencies[0] if currencies else "Unknown"
                }
            
            self.display_question()
        except Exception as e:
            self.question_label.configure(text=f"Error fetching question: {e}")

    def display_question(self):
        self.question_label.configure(text=self.current_question.get("question", ""))
        self.answer_entry.delete(0, tk.END)

        if hasattr(self, "flag_label") and self.flag_label.winfo_exists():
            self.flag_label.destroy()

        if "flag" in self.current_question:
            from PIL import Image, ImageTk
            from io import BytesIO
            try:
                response = requests.get(self.current_question["flag"])
                response.raise_for_status()
                image_data = BytesIO(response.content)
                img = Image.open(image_data).resize((150, 100))
                flag_image = ImageTk.PhotoImage(img)
                self.flag_label = tk.Label(self.root, image=flag_image)
                self.flag_label.image = flag_image
                self.flag_label.pack()
            except Exception as e:
                self.question_label.configure(text=f"Error displaying flag: {e}")

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.current_question.get("answer", "").strip().lower()

        if user_answer == correct_answer:
            self.feedback_label.configure(text="Correct!", text_color="green")
            self.score += 1
        else:
            self.feedback_label.configure(text=f"Wrong! The correct answer was {self.current_question.get('answer', 'Unknown')}.", text_color="red")

        self.questions_remaining -= 1
        self.score_label.configure(text=f"Score: {self.score}")

        if self.questions_remaining > 0:
            self.fetch_new_question()
        else:
            self.end_game()

    def end_game(self):
        self.clear_window()

        self.header_label = ctk.CTkLabel(self.root, text="Game Over", font=("Arial", 20))
        self.header_label.pack(pady=20)

        self.score_label = ctk.CTkLabel(self.root, text=f"Your Score: {self.score}", font=("Arial", 16))
        self.score_label.pack(pady=10)

        self.play_again_button = ctk.CTkButton(self.root, text="Play Again", command=self.main_menu)
        self.play_again_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Main Application
if __name__ == "__main__":
    root = ctk.CTk()
    app = QuizApp(root)
    root.mainloop()

