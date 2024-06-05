import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import customtkinter as ctk




def main():
    root = ctk.CTk()
    root.title("Maidiary")

    #forza ad avere la finestra a schermo intero mantenendo la barra di navigazione
    #root.attributes('-zoomed', True)
    root.geometry("800x600")
    root.resizable(width=True, height=True)
    
    # Configurazione del frame principale
    main_frame = ctk.CTkFrame(root, corner_radius=20)
    #voglio che il frame prenda tutto lo spazio
    main_frame.pack(side="top", expand=True, fill="both", pady=10, padx=10)

    #Logo al programma
    logo = tk.PhotoImage(file="MaiDiary_logo.png")
    logo_label = tk.Label(main_frame, image=logo)
    logo_label.pack(side="top", pady=20)

    # Etichetta di benvenuto stampata a capo
    welcome_label = ctk.CTkLabel(main_frame, text="Keep control, of your days...", font=("Helvetica", 16))
    welcome_label.pack(side="top")

    # Pulsante per accedere alla pagina di inserimento
    btn_continue = ctk.CTkButton(main_frame, text="Go to MaiDiary", command=lambda: show_diary_page(root))
    btn_continue.pack(side="top")

    root.mainloop()


def show_diary_page(root):
    
    # Elimino la finestra principale
    root.destroy()

    # Creo una nuova finestra di livello superiore per il diario
    diary_window = ctk.CTk()
    diary_window.title("Diario")

    # Imposto le dimensioni della finestra del diario per corrispondere a quelle della finestra principale
    diary_window.geometry("800x600")
    #diary_window.attributes('-zoomed', True)
    diary_window.resizable(width=True, height=True)

    # Variabili per i valori di soddisfazione e felicità
    s_val = tk.IntVar()
    f_val = tk.IntVar()

    #crea un top frame e un bottom frame
    top_frame = ctk.CTkFrame(diary_window, corner_radius=20, bg_color="#D3E3F9")
    top_frame.pack(side="top",expand=True, fill="both")

    bottom_frame = ctk.CTkFrame(diary_window, corner_radius=20, bg_color="#D3E3F9")
    bottom_frame.pack(side="bottom",expand=True, fill="both")

    # Frame in alto a sinistra
    top_left_frame = ctk.CTkFrame(top_frame, corner_radius=15, fg_color="#D3E3F9")
    top_left_frame.pack(side="left",expand=True, fill="both", padx=5, pady=5)

    # Frame in basso a sinistra
    bottom_left_frame = ctk.CTkFrame(bottom_frame, corner_radius=15, fg_color="#D3E3F9")
    bottom_left_frame.pack(side="left",expand=True, fill="both", padx=5, pady=5)

    # Frame in alto a destra
    top_right_frame = ctk.CTkFrame(top_frame, corner_radius=15, fg_color="#D3E3F9")
    top_right_frame.pack(side="left",expand=True, fill="both", padx=5, pady=5)

    # Frame in basso a destra
    bottom_right_frame = ctk.CTkFrame(bottom_frame, corner_radius=15, fg_color="#D3E3F9")
    bottom_right_frame.pack(side="left",expand=True, fill="both", padx=5, pady=5)

    #Creo un frame per ogni valutazione
    satisfaction_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    satisfaction_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    happiness_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    happiness_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)


    
    # Log delle precedenti pagine di diario 
    logs = load_log()
    log_text = ctk.CTkTextbox(top_left_frame, border_color="#D3E3F9", corner_radius=15, scrollbar_button_color="#D3E3F9")
    log_text.pack(expand=True, fill="both", padx=5, pady=5)
    for log in logs:
        log_text.insert(tk.END, log)

   # Grafico che si adatta alla finestra bottom_left
    fig = plt.Figure(figsize=(6, 5), dpi=50)
    canvas = FigureCanvasTkAgg(fig, master=bottom_left_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill="both", padx=5, pady=5)
    update_graph(canvas, fig, logs)


    # Area di inserimento del diario
    diary_entry = ctk.CTkTextbox(top_right_frame, border_color="#D3E3F9", corner_radius=15, scrollbar_button_color="#D3E3F9")
    diary_entry.pack(expand=True, fill="both", padx=5, pady=5)

    text_h = tk.StringVar(value="0")
    text_s = tk.StringVar(value="0")

    text_h.set(f"Felicità: {text_h.get()}")
    text_s.set(f"Soddisfazione: {text_s.get()}")


    # Funzione per mostrare il valore del cursore della soddisfazione come testo
    def mostra_h_val(value):
        text_h.set(f"Felicità: {int(happiness_slider.get())}")

    def mostra_s_val(value):
        text_s.set(f"Soddisfazione: {int(satisfaction_slider.get())}")


    #Creo gli slider e le labels per la felicità e la soddisfazione
    satisfaction_label = ctk.CTkLabel(satisfaction_frame, textvariable=text_s, font=("Helvetica", 12))
    satisfaction_label.pack(side="left", pady=5, padx=5)
    satisfaction_slider = ctk.CTkSlider(satisfaction_frame, from_=1, to=10, number_of_steps=10, command=mostra_s_val)
    satisfaction_slider.pack(side="left", pady=5, padx=5)
    satisfaction_slider.set(0)

    happiness_label = ctk.CTkLabel(happiness_frame, textvariable=text_h, font=("Helvetica", 12))
    happiness_label.pack(side="left", pady=5, padx=5)
    happiness_slider = ctk.CTkSlider(happiness_frame, from_=1, to=10, number_of_steps=10, command=mostra_h_val)
    happiness_slider.pack(side="left", pady=5, padx=5)
    happiness_slider.set(0)


    # Pulsante per inviare
    btn_submit = ctk.CTkButton(bottom_right_frame, text="INVIA", command=lambda: submit_entry(satisfaction_slider,happiness_slider,log_text, diary_entry, canvas, fig))
    btn_submit.pack(side="top", pady=5)

    diary_window.mainloop()


def submit_entry(satisfaction_slider,happiness_slider,log_text, diary_entry, canvas, fig):
    date_str = datetime.datetime.now().strftime("%d/%m/%Y")
    diary_text = diary_entry.get("1.0", tk.END).strip()
    satisfaction_level = int(satisfaction_slider.get())
    happiness_level =int(happiness_slider.get())

    if diary_text:
        log = f"{date_str} | {diary_text} | {satisfaction_level} | {happiness_level}"
        save_log(log)
        log_text.insert(tk.END, log + "\n")
        update_graph(canvas, fig, load_log())
        diary_entry.delete("1.0", tk.END)
        satisfaction_slider.set(0)
        happiness_slider.set(0)
        messagebox.showinfo("Successo", "Diario salvato con successo!")
    else:
        messagebox.showwarning("Errore", "Il testo del diario non può essere vuoto.")

if __name__ == "__main__":
    main()