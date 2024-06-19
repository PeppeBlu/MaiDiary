import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import customtkinter as ctk
import os

logs_path = "diary_logs"
ratings_file = "ratings_log.txt"

#Funzione che aggiorna i log
def refresh_logs(logs, ratings, left_frame):
    # Elimino tutti i widget presenti nel frame
    for widget in left_frame.winfo_children():
        widget.destroy()
    for log in logs:    
        log_frame = ctk.CTkFrame(left_frame, corner_radius=15, fg_color="#D3E3F9")
        log_frame.pack(side="top", expand=True, fill="both", padx=2, pady=5)

        log_text = ctk.CTkTextbox(log_frame, border_color="#D3E3F9", height=200,
                                  corner_radius=15, scrollbar_button_color="#D3E3F9")
        log_text.pack(expand=True,side="left", fill="both", padx=2, pady=5)

        with open(f"{logs_path}/{log}", "r") as file:
            log_content = file.read()
            log_text.insert(tk.END, log_content + "\n")

        erase_button = ctk.CTkButton(log_frame, text="Cancella", width=10, height=2, fg_color="blue", hover_color="red",
                                            command=lambda: delete_log(log_frame))
        erase_button.pack(side="right", padx=5, pady=5)

        
                


    def delete_log(log_frame):
        if messagebox.askyesno("","Vuoi davvero eliminare la pagina?"):
                
            for widget in log_frame.winfo_children():
                widget.destroy()
            log_frame.destroy() 
            logs = load_logs()
            refresh_logs(logs, ratings, left_frame)
            messagebox.showinfo("","Pagina eliminata con successo!")

def load_ratings():
    try:
        with open(ratings_file, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

# Funzione che salva il log delle giornate
def save_log(data):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y, %H-%M-%S")
    with open(f"{logs_path}/{timestamp}.txt", "w") as file:
        file.write(data)

# Funzione che carica il log delle giornate
def load_logs():
    try:
        file_contents = {}
        for entry in os.scandir(logs_path):
            if entry.is_file():
                with open(entry.path, 'r') as file:
                    file_contents[entry.name] = file.read()
        return file_contents
    except FileNotFoundError:
        return []
    
#Funzione che calcola la qualità della giornata
def calculate_quality(stress_level, satisfaction_level, 
                        mood_level, physical_activity, social_relations):
    
    return (satisfaction_level + mood_level + physical_activity + 
            social_relations - stress_level) / 6

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

    diary_frame = ctk.CTkFrame(root, corner_radius=20, bg_color="#D3E3F9")
    diary_frame.pack(side="top", expand=True, fill="both", pady=10, padx=10)
 
    #Top frame e  bottom frame
    left_frame = ctk.CTkScrollableFrame(diary_frame, corner_radius=20, fg_color="#D3E3F9")
    left_frame.pack(side="left",expand=True, fill="both", padx=5, pady=5)
    right_frame = ctk.CTkFrame(diary_frame, corner_radius=20, fg_color="#D3E3F9")
    right_frame.pack(side="right",expand=True, fill="both", padx=5, pady=5)


    # Frame in alto a sinistra
    top_left_frame = ctk.CTkScrollableFrame(left_frame, corner_radius=15, fg_color="#D3E3F9")
    top_left_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    # Frame in basso a sinistra
    bottom_left_frame = ctk.CTkFrame(left_frame, corner_radius=15, fg_color="#D3E3F9")
    bottom_left_frame.pack(side="bottom",expand=True, fill="both", padx=5, pady=5)

    # Frame in alto a destra
    top_right_frame = ctk.CTkFrame(right_frame, corner_radius=15, fg_color="#D3E3F9")
    top_right_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    # Frame in basso a destra
    bottom_right_frame = ctk.CTkFrame(right_frame, corner_radius=15, fg_color="#D3E3F9")
    bottom_right_frame.pack(side="bottom",expand=True, fill="both", padx=5, pady=5)

    #Creo un frame per ogni valutazione
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
    logs = load_logs()

    #Carico le valutazioni
    ratings = load_ratings()
    logs = load_logs()
    refresh_logs(logs, ratings, left_frame)
    
    #Area di inserimento del diario
    diary_entry = ctk.CTkTextbox(top_right_frame, border_color="#D3E3F9", 
                                 corner_radius=15, scrollbar_button_color="#D3E3F9")
    diary_entry.pack(expand=True, fill="both", padx=5, pady=5)
    
    text_st = ctk.StringVar(value="0")
    text_s = ctk.StringVar(value="0")
    text_m = ctk.StringVar(value="0")
    text_pa = ctk.StringVar(value="0")
    text_so = ctk.StringVar(value="0")
    
    text_st.set(f"Stress: {text_st.get()}")
    text_s.set(f"Soddisfazione: {text_s.get()}")
    text_m.set(f"Mood: {text_m.get()}")
    text_pa.set(f"Attività Fisica: {text_pa.get()}")
    text_so.set(f"Relazioni Sociali: {text_so.get()}")


    #Funzioni per mostrare i valori dei cursori
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
        date_str = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        diary_text = diary_entry.get("1.0", ctk.END).strip()
        stress_level = int(stress_slider.get())
        satisfaction_level = int(satisfaction_slider.get())
        mood_level = int(mood_slider.get())
        physical_activity = int(ph_act_slider.get())
        social_relations = int(social_slider.get())
        # Reset dei valori dei cursori dopo l'invio
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
        quality_of_day = calculate_quality(stress_level, satisfaction_level, 
                                        mood_level, physical_activity, social_relations)
        if diary_text:
            log = (f"Pagina del {date_str}\nValutazione giornata: {quality_of_day}\n"
            f"Valutazioni singole:\n Stress: {stress_level}\n Satisfaction: {satisfaction_level}\n"
            f" Mood: {mood_level}\n Physical_activity: {physical_activity}\n"
            f" Social_relations: {social_relations}\n\n{diary_text}")

            save_log(log)
            logs = load_logs()
            refresh_logs(logs, quality_of_day, left_frame)
            
            
            #update_graph(canvas, fig, load_ratings())
            diary_entry.delete("1.0", ctk.END)
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
  


    