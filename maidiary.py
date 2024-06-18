import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import customtkinter as ctk
import os

directory_path = "diary_logs"

#Funzione che aggiorna i log
def refresh_logs(logs, top_left_frame):
    # Elimino tutti i widget presenti nel frame
    for widget in top_left_frame.winfo_children():
        widget.destroy()
    for log in logs:    
        log_text = ctk.CTkTextbox(top_left_frame, border_color="#D3E3F9", height=70,
                                  corner_radius=15, scrollbar_button_color="#D3E3F9")
        log_text.pack(expand=True, fill="both", padx=5, pady=5)

        with open(f"{directory_path}/{log}", "r") as file:
            log_content = file.read()

        log_text.insert(tk.END, log_content + "\n")
        
# Funzione che salva il log delle giornate
def save_log(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"{directory_path}/{timestamp}.txt", "w") as file:
        file.write(data)

# Funzione che carica il log delle giornate
def load_log():
    try:
        file_contents = {}
        for entry in os.scandir(directory_path):
            if entry.is_file():
                with open(entry.path, 'r') as file:
                    file_contents[entry.name] = file.read()
        return file_contents
    except FileNotFoundError:
        return []
    
#Funzione che calcola la qualità della giornata
def calculate_quality(day_val, stress_level, satisfaction_level, mood_level, 
                      physical_activity, social_relations):
    
    return (day_val + satisfaction_level + mood_level + physical_activity + 
            social_relations - stress_level) / 6

#Funzione che salva le valutazioni
def save_ratings(timestamp, day_val, stress_level, satisfaction_level, mood_level, 
                 physical_activity, social_relations, quality_of_day):
    
    with open("ratings_log.txt", "a") as file:
        file.write(f"{timestamp} -> Valutazione: {day_val}, Stress: {stress_level}, "
                   f"Soddisfazione: {satisfaction_level}, Umore: {mood_level}, "
                   f"Attività fisica: {physical_activity}, Relazioni sociali: {social_relations}, "
                   f"Qualità: {int(quality_of_day)}\n"
                   )

#Funzione che carica le valutazioni        
def load_ratings():
    try:
        with open("ratings_log.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

#Funzione che aggiorna il grafico
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

# Funzione per la chiusura della finestra principale
def on_closing_root(root):
    if messagebox.askokcancel("Quit", "Vuoi davvero chiudere MaiDiary?"):
        root.quit()

#Funzione che crea il mainLframe
def create_main_frame(root):
    main_frame = ctk.CTkFrame(root, corner_radius=20)
    #voglio che il frame prenda tutto lo spazio
    main_frame.pack(side="top", expand=True, fill="both", pady=10, padx=10)

    #Logo al programma
    logo_label = tk.Label(main_frame, image=root.logo_image)
    logo_label.pack(side="top", pady=20)

    # Etichetta di benvenuto stampata a capo
    welcome_label = ctk.CTkLabel(main_frame, text="Keep control, of your days", font=("Helvetica", 16))
    welcome_label.pack(side="top", pady=10)

    # Pulsante per accedere alla pagina di inserimento
    btn_continue = ctk.CTkButton(main_frame, width=250, height=50, text_color="#D3E3F9", 
                                 text="Go to your MaiDiary", command=lambda: show_diary_page(root, main_frame))
    btn_continue.configure(font=("Helvetica", 20))
    btn_continue.pack(side="top")

    return main_frame

def back_to_main(root, diary_frame):
    diary_frame.destroy()
    main_frame = create_main_frame(root)
    main_frame.pack(side="top", expand=True, fill="both", pady=10, padx=10)


def main():
    root = ctk.CTk()
    root.title("Maidiary by Peppe Blunda")

    # Associa la funzione di chiusura personalizzata all'evento di chiusura della finestra principale
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing_root(root))

    #forza ad avere la finestra a schermo intero mantenendo la barra di navigazione
    #root.attributes('-zoomed', True)
    root.geometry("800x600")
    root.resizable(width=True, height=True)
    
    # Carica l'immagine del logo una volta e mantieni un riferimento
    root.logo_image = tk.PhotoImage(file="MaiDiary_Logo.png")

    # Configurazione del frame principale
    main_frame = create_main_frame(root)
    main_frame.pack(side="top", expand=True, fill="both", pady=10, padx=10)

    root.mainloop()


def show_diary_page(root, main_frame):
    
    main_frame.destroy()

    diary_frame = ctk.CTkFrame(root, corner_radius=20)
    diary_frame.pack(side="top", expand=True, fill="both", pady=10, padx=10)
 
    #Top frame e  bottom frame
    top_frame = ctk.CTkFrame(diary_frame, corner_radius=20, bg_color="#D3E3F9")
    top_frame.pack(side="top",expand=True, fill="both")
    bottom_frame = ctk.CTkFrame(diary_frame, corner_radius=20, bg_color="#D3E3F9")
    bottom_frame.pack(side="bottom",expand=True, fill="both")

    # Frame in alto a sinistra
    top_left_frame = ctk.CTkScrollableFrame(top_frame, corner_radius=15, fg_color="#D3E3F9")
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


    #Log delle precedenti pagine di diario 
    #logs è un array di stringhe che rappresentano le pagine del diario
    logs = load_log()
    refresh_logs(logs, top_left_frame)

   #Grafico della qualità della giornata
    fig = plt.Figure(figsize=(8, 6), dpi=50)
    canvas = FigureCanvasTkAgg(fig, master=bottom_left_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill="both", padx=5, pady=5)
    update_graph(canvas, fig, load_ratings())


    #Area di inserimento del diario
    diary_entry = ctk.CTkTextbox(top_right_frame, border_color="#D3E3F9", 
                                 corner_radius=15, scrollbar_button_color="#D3E3F9")
    diary_entry.pack(expand=True, fill="both", padx=5, pady=5)
    
    text_dv = ctk.StringVar(value="0")
    text_st = ctk.StringVar(value="0")
    text_s = ctk.StringVar(value="0")
    text_m = ctk.StringVar(value="0")
    text_pa = ctk.StringVar(value="0")
    text_so = ctk.StringVar(value="0")
    

    text_dv.set(f"Valutazione giornaliera: {text_dv.get()}")
    text_st.set(f"Stress: {text_st.get()}")
    text_s.set(f"Soddisfazione: {text_s.get()}")
    text_m.set(f"Mood: {text_m.get()}")
    text_pa.set(f"Attività Fisica: {text_pa.get()}")
    text_so.set(f"Relazioni Sociali: {text_so.get()}")


    #Funzioni per mostrare i valori dei cursori
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
    day_val_label = ctk.CTkLabel(day_val_frame, textvariable=text_dv, font=("Helvetica", 12))
    day_val_label.grid(row=0, column=1, pady=5)
    day_val_slider = ctk.CTkSlider(day_val_frame, from_=0, to=10, number_of_steps=10, command=mostra_dv_val)
    day_val_slider.grid(row=0, column=2, pady=5)
    day_val_slider.set(0)

    #Slider e labels per la soddisfazione
    satisfaction_label = ctk.CTkLabel(satisfaction_frame, textvariable=text_s, font=("Helvetica", 12))
    satisfaction_label.grid(row=0, column=1, pady=5)
    satisfaction_slider = ctk.CTkSlider(satisfaction_frame, from_=0, to=10, number_of_steps=10, command=mostra_s_val)
    satisfaction_slider.grid(row=0, column=2, pady=5)
    satisfaction_slider.set(0)

    #Slider e labels per il mood
    mood_label = ctk.CTkLabel(mood_frame, textvariable=text_m, font=("Helvetica", 12))
    mood_label.grid(row=0, column=1, pady=5)
    mood_slider = ctk.CTkSlider(mood_frame, from_=0, to=10, number_of_steps=10, command=mostra_m_val)
    mood_slider.grid(row=0, column=2, pady=5)
    mood_slider.set(0)

    #Slider e labels per lo stress
    stress_label = ctk.CTkLabel(stress_frame, textvariable=text_st, font=("Helvetica", 12))
    stress_label.grid(row=0, column=1, pady=5)
    stress_slider = ctk.CTkSlider(stress_frame, from_=0, to=10, number_of_steps=10, command=mostra_st_val)
    stress_slider.grid(row=0, column=2, pady=5)
    stress_slider.set(0)

    #Slider e labels per le attività fisiche
    ph_act_label = ctk.CTkLabel(ph_act_frame, textvariable=text_pa, font=("Helvetica", 12))
    ph_act_label.grid(row=0, column=1, pady=5)
    ph_act_slider = ctk.CTkSlider(ph_act_frame, from_=0, to=10, number_of_steps=10, command=mostra_pa_val)
    ph_act_slider.grid(row=0, column=2, pady=5)
    ph_act_slider.set(0)

    #Slider e labels per le relazioni sociali
    social_label = ctk.CTkLabel(social_frame, textvariable=text_so, font=("Helvetica", 12))
    social_label.grid(row=0, column=1, pady=5)
    social_slider = ctk.CTkSlider(social_frame, from_=0, to=10, number_of_steps=10, command=mostra_so_val)
    social_slider.grid(row=0, column=2, pady=5)
    social_slider.set(0)


    #Pulsante per fare il submit
    btn_submit = ctk.CTkButton(bottom_right_frame, width = 140, height = 28, text_color = "#D3E3F9", text="INVIA", 
                               command=lambda: submit_entry())
    btn_submit.pack(side="top", pady=5)
    btn_submit.configure(font=("Helvetica", 14))



    def submit_entry():
        date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        diary_text = diary_entry.get("1.0", ctk.END).strip()
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
        quality_of_day = calculate_quality(day_val, stress_level, satisfaction_level, 
                                        mood_level, physical_activity, social_relations)

        if diary_text:
            log = f"{date_str} \n {diary_text}"
            save_log(log)
            logs = load_log()
            refresh_logs(logs, top_left_frame)
            save_ratings(date_str, day_val, stress_level, satisfaction_level, mood_level, 
                        physical_activity, social_relations, quality_of_day)
            
            update_graph(canvas, fig, load_ratings())
            diary_entry.delete("1.0", ctk.END)
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
  


    