import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font
from modules.movie_genre_predictor import MovieGenrePredictor
from modules.translate_module import translate_texts
from modules.audio_module import text_to_speech
import threading

class MovieGenreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filmception")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f2f5")
        
        # Custom fonts
        self.title_font = Font(family="Helvetica", size=18, weight="bold")
        self.button_font = Font(family="Arial", size=12)
        self.genre_font = Font(family="Arial", size=11, slant="italic")
        
        # Load predictor
        self.predictor = MovieGenrePredictor()
        
        # Language options
        self.languages = {
            "English": "en",
            "Urdu": "ur",
            "Arabic": "ar",
            "Korean": "ko"
        }
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # App logo and title
        logo_label = tk.Label(header_frame, text="🎬", font=("Arial", 28), bg="#2c3e50", fg="white")
        logo_label.pack(side="left", padx=20)
        
        title_label = tk.Label(header_frame, text="FILMCEPTION", font=self.title_font, 
                              bg="#2c3e50", fg="white")
        title_label.pack(side="left")
        
        # Main Content Frame
        main_frame = tk.Frame(self.root, bg="#f0f2f5", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Summary Input
        input_frame = tk.LabelFrame(main_frame, text=" Enter Movie Summary ", font=self.button_font,
                                  bg="#f0f2f5", fg="#2c3e50", padx=10, pady=10)
        input_frame.pack(fill="x", pady=(0, 20))
        
        self.summary_entry = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=80, height=8,
                                                     font=("Arial", 11), bg="white", fg="#333",
                                                     insertbackground="#3498db")
        self.summary_entry.pack()
        
        # Predict Button
        predict_btn = tk.Button(main_frame, text="Predict Genres", command=self.predict_genres,
                              font=self.button_font, bg="#3498db", fg="white",
                              activebackground="#2980b9", activeforeground="white",
                              relief="flat", padx=20, pady=8)
        predict_btn.pack(pady=(10, 20))
        
        # Results Frame
        results_frame = tk.LabelFrame(main_frame, text=" Prediction Results ", font=self.button_font,
                                    bg="#f0f2f5", fg="#2c3e50", padx=10, pady=10)
        results_frame.pack(fill="x", pady=(0, 20))
        
        self.genre_label = tk.Label(results_frame, text="Genres will appear here...", 
                                  font=self.genre_font, bg="white", fg="#2c3e50",
                                  wraplength=800, justify="left")
        self.genre_label.pack(fill="x", padx=5, pady=5)
        
        # Translation Section
        trans_frame = tk.LabelFrame(main_frame, text=" Translation Options ", font=self.button_font,
                                  bg="#f0f2f5", fg="#2c3e50", padx=10, pady=10)
        trans_frame.pack(fill="x")
        
        # Language Selection
        lang_label = tk.Label(trans_frame, text="Select Language:", font=("Arial", 11), 
                             bg="#f0f2f5", fg="#333")
        lang_label.pack(anchor="w", pady=(0, 5))
        
        self.lang_var = tk.StringVar()
        lang_options = list(self.languages.keys())
        
        lang_menu = ttk.Combobox(trans_frame, textvariable=self.lang_var, 
                                values=lang_options, state="readonly",
                                font=("Arial", 11))
        lang_menu.current(0)
        lang_menu.pack(fill="x", pady=(0, 15))
        
        # Translate Button
        trans_btn = tk.Button(trans_frame, text="Translate & Speak", command=self.translate_and_speak,
                            font=self.button_font, bg="#27ae60", fg="white",
                            activebackground="#219653", activeforeground="white",
                            relief="flat", padx=20, pady=8)
        trans_btn.pack(pady=(5, 0))
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken",
                            anchor="w", font=("Arial", 10), bg="#ecf0f1", fg="#2c3e50")
        status_bar.pack(side="bottom", fill="x")
    
    def predict_genres(self):
        summary = self.summary_entry.get("1.0", "end-1c").strip()
        if not summary:
            messagebox.showwarning("Input Error", "Please enter a movie summary first!")
            return
        
        self.status_var.set("Predicting genres...")
        self.root.update()
        
        try:
            # Run prediction in a separate thread to keep GUI responsive
            threading.Thread(target=self._run_prediction, args=(summary,), daemon=True).start()
        except Exception as e:
            self.status_var.set("Error in prediction")
            messagebox.showerror("Prediction Error", f"An error occurred: {str(e)}")
    
    def _run_prediction(self, summary):
        try:
            genres = self.predictor.predict(summary)
            self.root.after(0, self._update_genre_display, genres)
            self.status_var.set("Prediction complete")
        except Exception as e:
            self.root.after(0, self._show_error, "Prediction Error", str(e))
    
    def _update_genre_display(self, genres):
        if not genres:
            self.genre_label.config(text="No genres predicted", fg="#e74c3c")
        else:
            genres_text = " | ".join(genres)
            self.genre_label.config(text=genres_text, fg="#27ae60")
    
    def translate_and_speak(self):
        summary = self.summary_entry.get("1.0", "end-1c").strip()
        if not summary:
            messagebox.showwarning("Input Error", "Please enter a movie summary first!")
            return
        
        lang_name = self.lang_var.get()
        if not lang_name:
            messagebox.showwarning("Language Error", "Please select a language!")
            return
        
        if lang_name == "English":
            threading.Thread(target=self._run_translation, args=(summary, "en"), daemon=True).start()
            return
        
        lang_code = self.languages[lang_name]
        self.status_var.set(f"Translating to {lang_name}...")
        self.root.update()
        
        # Run translation in a separate thread
        threading.Thread(target=self._run_translation, args=(summary, lang_code), daemon=True).start()
    
    def _run_translation(self, text, lang_code):
        if lang_code == "en":
            translated = text
            self.status_var.set(f"No translation needed. Playing {lang_code} summary...")
            self.root.after(0, self._speak_translation, translated, lang_code)
        else:
            try:
                translated = translate_texts([text], lang_code)[0]
                self.root.after(0, self._speak_translation, translated, lang_code)
                self.status_var.set(f"Playing {lang_code} translation...")
            except Exception as e:
                self.root.after(0, self._show_error, "Translation Error", str(e))
    
    def _speak_translation(self, text, lang_code):
        try:
            text_to_speech(text, lang_code)
            self.status_var.set("Ready")
        except Exception as e:
            self.root.after(0, self._show_error, "Audio Error", str(e))
    
    def _show_error(self, title, message):
        messagebox.showerror(title, message)
        self.status_var.set("Error occurred")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieGenreApp(root)
    root.mainloop()