import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import customtkinter as ctk



# Funzione per salvare il log delle giornate
def save_log(data):
    with open("diary_log.txt", "a") as file:
        file.write(data + "\n")

# Funzione per caricare il log delle giornate
def load_log():
    try:
        with open("diary_log.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def update_graph(canvas, figure, logs):
    dates = []
    satisfaction = []
    for log in logs:
        parts = log.strip().split("|")
        if len(parts) == 4:  # Data, Diario, Soddisfazione, Felicità
            dates.append(parts[0])
            satisfaction.append(int(parts[2]))

    figure.clear()
    ax = figure.add_subplot(111)
    ax.plot(dates, satisfaction, marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Satisfaction Level')
    canvas.draw()



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
    logo = tk.PhotoImage(file="MaiDiary_Logo.png")
    logo_label = tk.Label(main_frame, image=logo)
    logo_label.pack(side="top", pady=20)

    # Etichetta di benvenuto stampata a capo
    welcome_label = ctk.CTkLabel(main_frame, text="Keep control, of your days", font=("Helvetica", 16))
    welcome_label.pack(side="top")

    # Pulsante per accedere alla pagina di inserimento
    btn_continue = ctk.CTkButton(main_frame, width=250, height=50, text_color="#D3E3F9", text="Go to your MaiDiary", command=lambda: show_diary_page(root))
    btn_continue.configure(font=("Helvetica", 20))
    btn_continue.pack(side="top")
    

    root.mainloop()


def show_diary_page(root):
    
    # Elimino la finestra principale
    root.destroy()

    # Nuova finestra di livello superiore per il diario
    diary_window = ctk.CTk()
    diary_window.title("Diario")

    # Imposto le dimensioni della finestra del diario per corrispondere a quelle della finestra principale
    diary_window.geometry("800x600")
    #diary_window.attributes('-zoomed', True)
    diary_window.resizable(width=True, height=True)


    #Top frame e  bottom frame
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
    day_val_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    day_val_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    stress_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    stress_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    satisfaction_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    satisfaction_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    mood_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    mood_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    ph_act_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    ph_act_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    social_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    social_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    


    
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
    
    text_dv = tk.StringVar(value="0")
    text_st = tk.StringVar(value="0")
    text_s = tk.StringVar(value="0")
    text_m = tk.StringVar(value="0")
    text_pa = tk.StringVar(value="0")
    text_so = tk.StringVar(value="0")
    

    text_dv.set(f"Valutazione giornaliera: {text_dv.get()}")
    text_st.set(f"Stress: {text_st.get()}")
    text_s.set(f"Soddisfazione: {text_s.get()}")
    text_m.set(f"Mood: {text_m.get()}")
    text_pa.set(f"Attività Fisica: {text_pa.get()}")
    text_so.set(f"Relazioni Sociali: {text_so.get()}")


    # Funzione per mostrare il valore del cursore della soddisfazione come testo
    def mostra_dv_val(value):
        day_val_label.set(f"Valutazione giornaliera: {int(day_val_slider.get())}")

    def mostra_st_val(value):
        text_st.set(f"Stress: {int(stress_slider.get())}")

    def mostra_s_val(value):
        text_s.set(f"Soddisfazione: {int(satisfaction_slider.get())}")
    
    def mostra_m_val(value):
        text_m.set(f"Mood: {int(mood_slider.get())}")

    def mostra_pa_val(value):
        text_pa.set(f"Attività Fisica: {int(ph_act_slider.get())}")

    def mostra_so_val(value):
        text_so.set(f"Relazioni Sociali: {int(social_slider.get())}")


    #Slider e labels per la valutazione generale della giornata
    day_val_label = ctk.CTkLabel(day_val_frame, textvariable=text_dv, font=("Helvetica", 12))
    day_val_label.pack(side="left", pady=5)
    day_val_slider = ctk.CTkSlider(day_val_frame, from_=1, to=10, number_of_steps=10, command=mostra_dv_val)
    day_val_slider.pack(side="left", pady=5)
    day_val_slider.set(0)

    #Slider e labels per la soddisfazione
    satisfaction_label = ctk.CTkLabel(satisfaction_frame, textvariable=text_s, font=("Helvetica", 12))
    satisfaction_label.pack(side="left", pady=5, padx=5)
    satisfaction_slider = ctk.CTkSlider(satisfaction_frame, from_=1, to=10, number_of_steps=10, command=mostra_s_val)
    satisfaction_slider.pack(side="left", pady=5, padx=5)
    satisfaction_slider.set(0)

    #Slider e labels per il mood
    mood_label = ctk.CTkLabel(mood_frame, textvariable=text_m, font=("Helvetica", 12))
    mood_label.pack(side="left", pady=5, padx=5)
    mood_slider = ctk.CTkSlider(mood_frame, from_=1, to=10, number_of_steps=10, command=mostra_m_val)
    mood_slider.pack(side="left", pady=5, padx=5)
    mood_slider.set(0)

    #Slider e labels per lo stress
    stress_label = ctk.CTkLabel(stress_frame, textvariable=text_st, font=("Helvetica", 12))
    stress_label.pack(side="left", pady=5, padx=5)
    stress_slider = ctk.CTkSlider(stress_frame, from_=1, to=10, number_of_steps=10, command=mostra_st_val)
    stress_slider.pack(side="left", pady=5, padx=5)
    stress_slider.set(0)

    #Slider e labels per le attività fisiche
    ph_act_label = ctk.CTkLabel(ph_act_frame, textvariable=text_pa, font=("Helvetica", 12))
    ph_act_label.pack(side="left", pady=5, padx=5)
    ph_act_slider = ctk.CTkSlider(ph_act_frame, from_=1, to=10, number_of_steps=10, command=mostra_pa_val)
    ph_act_slider.pack(side="left", pady=5, padx=5)
    ph_act_slider.set(0)

    #Slider e labels per le relazioni sociali
    social_label = ctk.CTkLabel(social_frame, textvariable=text_so, font=("Helvetica", 12))
    social_label.pack(side="left", pady=5, padx=5)
    social_slider = ctk.CTkSlider(social_frame, from_=1, to=10, number_of_steps=10, command=mostra_so_val)
    social_slider.pack(side="left", pady=5, padx=5)
    social_slider.set(0)
    

    # Pulsante per inviare
    btn_submit = ctk.CTkButton(bottom_right_frame, width = 140, height = 28, text_color = "#D3E3F9", text="INVIA", 
                               command=lambda: submit_entry(day_val_slider, stress_slider, satisfaction_slider, mood_slider, ph_act_slider, social_slider, log_text, diary_entry, canvas, fig))
    btn_submit.pack(side="top", pady=5)
    btn_submit.configure(font=("Helvetica", 14))

    diary_window.mainloop()


def submit_entry(day_val_slider, stress_slider, satisfaction_slider, mood_slider , ph_act_slider, social_slider, log_text, diary_entry, canvas, fig):
    date_str = datetime.datetime.now().strftime("%d/%m/%Y")
    diary_text = diary_entry.get("1.0", tk.END).strip()
    day_val = int(day_val_slider.get())
    stress_level = int(stress_slider.get())
    satisfaction_level = int(satisfaction_slider.get())
    mood_level = int(mood_slider.get())
    physical_activity = int(ph_act_slider.get())
    social_relations = int(social_slider.get())
    

    if diary_text:
        log = f"{date_str} | {diary_text}"
        save_log(log)
        log_text.insert(tk.END, log + "\n")
        update_graph(canvas, fig, load_log())
        diary_entry.delete("1.0", tk.END)
        day_val_slider.set(0)
        stress_slider.set(0)
        satisfaction_slider.set(0)
        mood_slider.set(0)
        ph_act_slider.set(0)
        social_slider.set(0)

        messagebox.showinfo("","Pagina salvata con successo!")
        
    else:
        messagebox.showwarning("Errore", "Il testo del diario non può essere vuoto.")

if __name__ == "__main__":
    main()