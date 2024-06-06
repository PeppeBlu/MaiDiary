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

def calculate_quality(day_val, stress_level, satisfaction_level, mood_level, physical_activity, social_relations):
    return (day_val + satisfaction_level + mood_level + physical_activity + social_relations - stress_level) / 6

def save_ratings(timestamp, day_val, stress_level, satisfaction_level, mood_level, physical_activity, social_relations, quality_of_day):
    with open("ratings_log.txt", "a") as file:
        file.write(f"{timestamp} -> Valutazione: {day_val}, Stress: {stress_level}, Soddisfazione: {satisfaction_level}, Umore: {mood_level}, Attività fisica: {physical_activity}, Relazioni sociali: {social_relations}, Qualità: {int(quality_of_day)}\n")
        
def load_ratings():
    try:
        with open("ratings_log.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def update_graph(canvas, figure, logs):
    timestamps = []
    quality_of_days = []
    for log in logs:
        parts = log.strip().split("->")
        if len(parts) == 2:
            timestamp = parts[0].strip()
            ratings = parts[1].strip().split(",")
            quality_of_day = float(ratings[-1].split(":")[1].strip())
            timestamps.append(timestamp)
            quality_of_days.append(quality_of_day)

    figure.clear()
    ax = figure.add_subplot(111)
    ax.plot(timestamps, quality_of_days, marker='o', label='Qualità della giornata')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Qualità della giornata')
    ax.legend()
    plt.xticks(rotation=45, ha='right')
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
    
    #Salva le informazioni della grandezza della finestra root che possono essere cambiate
    #per poi essere ripristinate nella nuova finestra
    width_r = root.winfo_width()
    height_r = root.winfo_height()

    # Elimino la finestra principale
    #root.quit()
    root.destroy()

    # Nuova finestra di livello superiore per il diario
    diary_window = ctk.CTk()
    diary_window.title("Diario")

    # Imposto le dimensioni della finestra del diario per corrispondere a quelle della finestra principale
    diary_window.geometry(f"{width_r}x{height_r}")
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

    #Configurazione dei frame per le valutazioni
    day_val_frame.grid_columnconfigure(0, weight=1)
    day_val_frame.grid_columnconfigure(1, weight=0)
    day_val_frame.grid_columnconfigure(2, weight=1)

    stress_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    stress_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    stress_frame.grid_columnconfigure(0, weight=1)
    stress_frame.grid_columnconfigure(1, weight=0)
    stress_frame.grid_columnconfigure(2, weight=1)

    satisfaction_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    satisfaction_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    satisfaction_frame.grid_columnconfigure(0, weight=1)
    satisfaction_frame.grid_columnconfigure(1, weight=0)
    satisfaction_frame.grid_columnconfigure(2, weight=1)

    mood_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    mood_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    mood_frame.grid_columnconfigure(0, weight=1)
    mood_frame.grid_columnconfigure(1, weight=0)
    mood_frame.grid_columnconfigure(2, weight=1)

    ph_act_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    ph_act_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    ph_act_frame.grid_columnconfigure(0, weight=1)
    ph_act_frame.grid_columnconfigure(1, weight=0)
    ph_act_frame.grid_columnconfigure(2, weight=1)

    social_frame = ctk.CTkFrame(bottom_right_frame, corner_radius=15, fg_color="#D3E3F9")
    social_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    social_frame.grid_columnconfigure(0, weight=1)
    social_frame.grid_columnconfigure(1, weight=0)
    social_frame.grid_columnconfigure(2, weight=1)


    
    # Log delle precedenti pagine di diario 
    logs = load_log()
    log_text = ctk.CTkTextbox(top_left_frame, border_color="#D3E3F9", corner_radius=15, scrollbar_button_color="#D3E3F9")
    log_text.pack(expand=True, fill="both", padx=5, pady=5)
    for log in logs:
        log_text.insert(tk.END, log)

   # Grafico che si adatta alla finestra bottom_left
    fig = plt.Figure(figsize=(15, 7), dpi=50)
    canvas = FigureCanvasTkAgg(fig, master=bottom_left_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill="both", padx=5, pady=5)
    update_graph(canvas, fig, load_ratings())


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
        text_dv.set(f"Valutazione giornaliera: {int(day_val_slider.get())}")

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
    day_val_label = ctk.CTkLabel(day_val_frame, textvariable=text_dv, font=("Helvetica", 15))
    day_val_label.grid(row=0, column=1, pady=10)
    day_val_slider = ctk.CTkSlider(day_val_frame, from_=0, to=10, number_of_steps=10, command=mostra_dv_val)
    day_val_slider.grid(row=0, column=2, pady=10)
    day_val_slider.set(0)

    #Slider e labels per la soddisfazione
    satisfaction_label = ctk.CTkLabel(satisfaction_frame, textvariable=text_s, font=("Helvetica", 15))
    satisfaction_label.grid(row=0, column=1, pady=10)
    satisfaction_slider = ctk.CTkSlider(satisfaction_frame, from_=0, to=10, number_of_steps=10, command=mostra_s_val)
    satisfaction_slider.grid(row=0, column=2, pady=10)
    satisfaction_slider.set(0)

    #Slider e labels per il mood
    mood_label = ctk.CTkLabel(mood_frame, textvariable=text_m, font=("Helvetica", 15))
    mood_label.grid(row=0, column=1, pady=10)
    mood_slider = ctk.CTkSlider(mood_frame, from_=0, to=10, number_of_steps=10, command=mostra_m_val)
    mood_slider.grid(row=0, column=2, pady=10)
    mood_slider.set(0)

    #Slider e labels per lo stress
    stress_label = ctk.CTkLabel(stress_frame, textvariable=text_st, font=("Helvetica", 15))
    stress_label.grid(row=0, column=1, pady=10)
    stress_slider = ctk.CTkSlider(stress_frame, from_=0, to=10, number_of_steps=10, command=mostra_st_val)
    stress_slider.grid(row=0, column=2, pady=10)
    stress_slider.set(0)

    #Slider e labels per le attività fisiche
    ph_act_label = ctk.CTkLabel(ph_act_frame, textvariable=text_pa, font=("Helvetica", 15))
    ph_act_label.grid(row=0, column=1, pady=10)
    ph_act_slider = ctk.CTkSlider(ph_act_frame, from_=0, to=10, number_of_steps=10, command=mostra_pa_val)
    ph_act_slider.grid(row=0, column=2, pady=10)
    ph_act_slider.set(0)

    #Slider e labels per le relazioni sociali
    social_label = ctk.CTkLabel(social_frame, textvariable=text_so, font=("Helvetica", 15))
    social_label.grid(row=0, column=1, pady=10)
    social_slider = ctk.CTkSlider(social_frame, from_=0, to=10, number_of_steps=10, command=mostra_so_val)
    social_slider.grid(row=0, column=2, pady=10)
    social_slider.set(0)


    # Pulsante per inviare
    btn_submit = ctk.CTkButton(bottom_right_frame, width = 140, height = 28, text_color = "#D3E3F9", text="INVIA", 
                               command=lambda: submit_entry(day_val_slider, stress_slider, satisfaction_slider, mood_slider , 
                                                            ph_act_slider, social_slider, log_text, diary_entry, canvas, fig, 
                                                            mostra_dv_val, mostra_st_val, mostra_s_val, mostra_m_val, mostra_pa_val, 
                                                            mostra_so_val))
    btn_submit.pack(side="top", pady=5)
    btn_submit.configure(font=("Helvetica", 14))

    diary_window.mainloop()


def submit_entry(day_val_slider, stress_slider, satisfaction_slider, mood_slider, 
                                                            ph_act_slider, social_slider, log_text, diary_entry, canvas, fig, 
                                                            mostra_dv_val, mostra_st_val, mostra_s_val, mostra_m_val, mostra_pa_val, 
                                                            mostra_so_val):
    date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    diary_text = diary_entry.get("1.0", tk.END).strip()
    day_val = int(day_val_slider.get())
    stress_level = int(stress_slider.get())
    satisfaction_level = int(satisfaction_slider.get())
    mood_level = int(mood_slider.get())
    physical_activity = int(ph_act_slider.get())
    social_relations = int(social_slider.get())

    # Reset dei valori dei cursori dopo l'invio
    day_val_slider.set(0)
    mostra_dv_val(0)
    stress_slider.set(0)
    mostra_st_val(0)
    satisfaction_slider.set(0)
    mostra_s_val(0)
    mood_slider.set(0)
    mostra_m_val(0)
    ph_act_slider.set(0)
    mostra_pa_val(0)
    social_slider.set(0)
    mostra_so_val(0)


    # Calcolo della qualità della giornata
    quality_of_day = calculate_quality(day_val, stress_level, satisfaction_level, mood_level, physical_activity, social_relations)

    if diary_text:
        log = f"{date_str} | {diary_text}"
        save_log(log)
        save_ratings(date_str, day_val, stress_level, satisfaction_level, mood_level, physical_activity, social_relations, quality_of_day)
        log_text.insert(tk.END, log + "\n")
        update_graph(canvas, fig, load_ratings())
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

    