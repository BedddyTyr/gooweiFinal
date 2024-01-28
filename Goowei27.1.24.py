import tkinter as tk
import random
import time

morse_codes = {
    ".-": 'a', "-...": 'b', "-.-.": 'c', "-..": 'd', ".": 'e',
    "..-.": 'f', "--.": 'g', "....": 'h', "..": 'i', ".---": 'j',
    "-.-": 'k', ".-..": 'l', "--": 'm', "-.": 'n', "---": 'o',
    ".--.": 'p', "--.-": 'q', ".-.": 'r', "...": 's', "-": 't',
    "..-": 'u', "...-": 'v', ".--": 'w', "-..-": 'x', "-.--": 'y',
    "--..": 'z'
}


class CountdownWindow:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.master.configure(bg="Black")
        self.remaining_time = 30
        self.countdown_label = tk.Label(master, text=f"Time Left: {self.remaining_time} seconds",
                                        font=("OCR A Extended", 12), fg="Green", bg="Black")
        self.countdown_label.grid(pady=10)
        self.update_countdown()

    def update_countdown(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.countdown_label.config(text=f"Time Left: {self.remaining_time} seconds")
            self.master.after(1000, self.update_countdown)
        else:
            self.callback()


class MorseGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Menu")
        self.master.geometry("350x350+500+150")
        self.master.configure(bg="Black")
        self.current_game_window = None
        self.timed_countdown_window = None
        self.hint_window = None
        self.score = 0

        self.label = tk.Label(master, text="Welcome to the\nMorseZone!", font=("OCR A Extended", 16, "bold"),
                              fg="green", bg="Black")
        self.label.pack(pady=43)

        self.button_frame = tk.Frame(master)
        self.button_frame.configure(bg="Black")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        self.normal_button = tk.Button(self.button_frame, text="Normal Mode", command=self.start_normal_game,
                                       font=("OCR A Extended", 14), bg="Black", fg="Green",)
        self.normal_button.grid(row=1, column=0, pady=10)

        self.timed_button = tk.Button(self.button_frame, text="Timed Mode", command=self.start_timed_game,
                                      font=("OCR A Extended", 14), bg="Black", fg="Green")
        self.timed_button.grid(row=1, column=3, pady=10)

        self.hint_button = tk.Button(self.button_frame, text="Hint", command=self.display_hint, font=("OCR A Extended", 14),
                                     bg="Black", fg="Green")
        self.hint_button.grid(row=3, column=2, pady=10)

        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.master.destroy,
                                     font=("OCR A Extended", 14), bg="Black", fg="Green")
        self.quit_button.grid(row=4, column=2, pady=10)
        self.button_frame.pack()

    def start_normal_game(self):
        if self.current_game_window:
            self.current_game_window.destroy()

        self.current_game_window = tk.Toplevel(self.master)
        self.current_game_window.geometry("+425+210")
        self.current_game_window.configure(bg="black")
        self.current_game_window.title("N O R M A L   M O D E")
        self.score = 0
        self.nrmlFrm = tk.Frame(self.current_game_window)
        self.nrmlFrm.configure(bg="Black")

        self.morse_codes_copy = list(morse_codes.items())
        random.shuffle(self.morse_codes_copy)
        self.current_question_index = 0

        self.normal_display_next_question()

        self.nrmlFrm.pack()

    def normal_display_next_question(self):
        if self.current_question_index < 10:
            random_morse, correct_answer = self.morse_codes_copy[self.current_question_index]
            self.normal_display_question(random_morse)

            user_input = tk.Entry(self.nrmlFrm, font=("OCR A Extended", 14), fg="Green", bg="Black")
            user_input.grid(row=2, column=0, pady=10)

            submit_button = tk.Button(self.nrmlFrm, text="Submit",
                                      command=lambda r=random_morse, c=correct_answer: self.normal_check_answer(user_input, r,
                                                                                                         c),
                                      font=("OCR A Extended", 14), fg="Green", bg="Black")
            submit_button.grid(row=3, column=0, pady=10)

        else:
            empty_label = tk.Label(self.nrmlFrm,
                                   text="                                                                                \n  ",
                                   font=("OCR A Extended", 14), fg="Black", bg="Black")
            empty_label.grid(row=1, column=0, pady=20)
            self.normal_display_score()
            main_menu_button = tk.Button(self.nrmlFrm, text="Back to Main Menu",
                                         command=self.current_game_window.destroy, font=("OCR A Extended", 14),
                                         fg="Green", bg="Black")
            main_menu_button.grid(row=3, column=0, pady=10)
            empty_label = tk.Label(self.nrmlFrm,
                                   text="                                                         \n  ",
                                   font=("OCR A Extended", 14),fg="Black", bg="Black")
            empty_label.grid(row=4, column=0, pady=20)

    def normal_display_question(self, random_morse):
        morse_label = tk.Label(self.nrmlFrm,
                               text=f"Guess the letter for the following Morse code:\n{random_morse}",
                               font=("OCR A Extended", 14), fg="Green", bg="Black")
        morse_label.grid(row=1, column=0, pady=20)

    def normal_check_answer(self, user_input, random_morse, correct_answer):
        user_answer = user_input.get().lower()

        if user_answer == correct_answer:
            self.display_feedback("               Correct! Nice guess!               ", True)
            self.score += 1
        else:
            self.display_feedback(f"Wrong. The correct answer is '{correct_answer}'.", False)

        user_input.delete(0, tk.END)
        self.current_question_index += 1
        self.normal_display_next_question()

    def display_feedback(self, feedback, is_correct):
        feedback_label = tk.Label(self.nrmlFrm, text=feedback, font=("OCR A Extended", 14),
                                  fg="green" if is_correct else "red", bg="Black")
        feedback_label.grid(row=4, column=0, pady=20)

    def normal_display_score(self):
        score_label = tk.Label(self.nrmlFrm, text=f"Your final score is: {self.score}/10",
                               font=("OCR A Extended", 16),fg="Green", bg="Black")
        score_label.grid(row=2, column=0, pady=20)


    def start_timed_game(self):
        if self.current_game_window:
            self.current_game_window.destroy()

        self.current_game_window = tk.Toplevel(self.master)
        self.current_game_window.configure(bg="black")
        self.current_game_window.title("T I M E D   M O D E")
        self.current_game_window.geometry("+425+190")
        self.score = 0
        self.questions_attempted = 0
        self.start_time = time.time()

        self.timedFrm = tk.Frame(self.current_game_window)

        self.countdown = CountdownWindow(self.timedFrm, self.end_game)

        self.timedFrm.pack()
        self.display_next_question()

    def display_next_question(self):
        if time.time() - self.start_time <= 30:  # Check if 30 seconds have not passed
            random_morse, correct_answer = random.choice(list(morse_codes.items()))
            self.display_question(random_morse)

            user_input = tk.Entry(self.timedFrm, font=("OCR A Extended", 14), fg="Green", bg="Black")
            user_input.grid(row=2, column=0, pady=10)

            submit_button = tk.Button(self.timedFrm, text="Submit",
                                      command=lambda r=random_morse, c=correct_answer: self.check_answer(user_input, r,
                                                                                                         c),
                                      font=("OCR A Extended", 14), fg="Green", bg="Black")
            submit_button.grid(row=3, column=0, pady=10)

        else:
            self.end_game()

    def check_answer(self, user_input, random_morse, correct_answer):
        user_answer = user_input.get().lower()
        user_input.delete(0, tk.END)

        feedback = tk.Label(self.timedFrm, font=("OCR A Extended", 14), fg="Green", bg="Black")

        if user_answer == correct_answer:
            self.score += 1
            feedback.config(text="               Correct! Nice guess!               ", fg="green", bg="Black")
        else:
            feedback.config(text=f"Wrong. The correct answer is '{correct_answer}'.", fg="red", bg="Black")

        feedback.grid(row=5, column=0, pady=10)

        self.questions_attempted += 1
        self.display_next_question()

    def display_question(self, random_morse):
        morse_label = tk.Label(self.timedFrm,
                               text=f"Guess the letter for the following Morse code:\n{random_morse}",
                               font=("OCR A Extended", 14), fg="Green", bg="Black")
        morse_label.grid(row=1, column=0, pady=20)

    def end_game(self):
        empty_label = tk.Label(self.timedFrm,
                               text="                                                             "
                                    "                                                         \n  ",
                               font=("Helvetica", 14), fg="Black", bg="black")
        empty_label.grid(row=1, column=0, pady=20)
        self.display_score()
        empty_label = tk.Label(self.timedFrm,
                               text="                                                              "
                                    "                                                    \n  ",
                               font=("Helvetica", 14), fg="Black", bg="Black")
        empty_label.grid(row=5, column=0, pady=20)
        self.remove_submit_button()

    def remove_submit_button(self):
        for widget in self.timedFrm.winfo_children():
            if widget.winfo_class() == "Button" and widget["text"] == "Submit":
                widget.destroy()

        back_to_menu_button = tk.Button(self.timedFrm, text="Back to Menu", command=self.current_game_window.destroy,
                                        font=("OCR A Extended", 14), fg="Green", bg="Black")
        back_to_menu_button.grid(row=4, column=0, pady=10)

    def display_score(self):
        score_label = tk.Label(self.timedFrm,
                               text=f"    Your final score is: {self.score}/{self.questions_attempted}    ",
                               font=("OCR A Extended", 16), fg="Green", bg="Black")
        score_label.grid(row=2, column=0, pady=20)


    def display_hint(self):
        if self.hint_window:
            self.hint_window.destroy()

        self.hint_window = tk.Toplevel(self.master)
        self.hint_window.title("H I N T S")
        self.hint_window.configure(bg="black")
        self.hint_window.geometry("+50+20")
        hint_label = tk.Label(self.hint_window, text=self.generate_hint_text(), font=("OCR A Extended", 14)
                              , fg="Green", bg="Black")
        hint_label.grid(row=0, column=0, pady=15, padx=10)

        back_button = tk.Button(self.hint_window, text="<<", command=self.hint_window.destroy,
                                font=("OCR A Extended", 11), fg="Green", bg="Black")
        back_button.grid(row=1, column=0, pady=10)

    def generate_hint_text(self):
        hint_text = "--Morse Code Hints--\n"
        for code, letter in morse_codes.items():
            hint_text += f"{letter.upper()} = {code}\n"
        return hint_text

if __name__ == "__main__":
    root = tk.Tk()
    app = MorseGameGUI(root)
    root.mainloop()