"""Maidiary, un programma per la gestione di un diario personale"""

import datetime
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken

VERSION = "1.0"


ctk.set_appearance_mode("light")

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())


def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()


def visualize_log(log, log_content, left_frame):
    """Funzione che visualizza un log"""

    for widget in left_frame.winfo_children():
        widget.destroy()

    visualize_frame = ctk.CTkFrame(left_frame, corner_radius=20, fg_color="#D3E3F9")
    visualize_frame.pack(side="top", expand=True, fill="both", padx=2, pady=5)
    visualize_text = ctk.CTkTextbox(visualize_frame,
                                    border_color="#D3E3F9",
                                    height=500, width=600, font=("Helvetica", 14),
                                    corner_radius=20,
                                    scrollbar_button_color="#D3E3F9")
    visualize_text.pack(expand=True, fill="both", padx=2, pady=5)
    visualize_text.insert(tk.END, log_content + "\n")

    visualize_buttons_frame = ctk.CTkFrame(visualize_frame,
                                           corner_radius=20,
                                           fg_color="#D3E3F9")
    visualize_buttons_frame.pack(side="bottom", expand=True, fill="both", padx=2, pady=2)
    visualize_buttons_frame.grid_rowconfigure(0, weight=1)
    visualize_buttons_frame.grid_columnconfigure(1, weight=1)
    visualize_buttons_frame.grid_columnconfigure(0, weight=1)

    close_button = ctk.CTkButton(visualize_buttons_frame,
                                 text="Indietro",
                                 width=100,height=30,
                                 hover_color="red",
                                 command=lambda: close_visualize(visualize_frame, left_frame))
    close_button.grid(row=0, column=0, pady=2)
    save_button = ctk.CTkButton(visualize_buttons_frame,
                                text="Salva",
                                width=100, height=30, hover_color="green",
                                command=lambda: update_log(log,
                                                           visualize_text,
                                                           visualize_frame,
                                                           left_frame))
    save_button.grid(row=0, column=1, pady=2)


def close_visualize(visualize_frame, left_frame):
    """Funzione che chiude la visualizzazione di un log"""

    visualize_frame.destroy()
    refresh_logs(load_logs(LOGS_PATH, key), left_frame, LOGS_PATH, key)


def refresh_logs(logs, left_frame, LOGS_PATH, key):
    """Funzione che aggiorna la lista dei log visualizzati sul frame sinistro"""
    try:
        for widget in left_frame.winfo_children():
            widget.destroy()

        for log_name, decrypted_log_content in logs.items():
            log_frame = ctk.CTkFrame(left_frame,
                                     corner_radius=20,
                                     fg_color="#D3E3F9")
            log_frame.pack(side="top", expand=True, fill="both", padx=2, pady=5)

            buttons_frame = ctk.CTkFrame(left_frame,
                                         corner_radius=20,
                                         fg_color="#D3E3F9")
            buttons_frame.pack(side="top", expand=True, fill="both", padx=2, pady=2)
            buttons_frame.grid_rowconfigure(0, weight=1)
            buttons_frame.grid_columnconfigure(0, weight=1)
            buttons_frame.grid_columnconfigure(1, weight=1)

            log_text = ctk.CTkTextbox(log_frame,
                                      height=200, width=300, font=("Helvetica", 13),
                                      corner_radius=20, scrollbar_button_color="#D3E3F9")
            log_text.pack(expand=True, fill="both", padx=2, pady=5)
            log_text.insert(tk.END, decrypted_log_content + "\n")

            delete_button = ctk.CTkButton(buttons_frame,
                                          text="Cancella",
                                          width=100, height=30, hover_color="red",
                                          command=lambda: delete_log(log_name,
                                                                     left_frame,
                                                                     LOGS_PATH, key))
            delete_button.grid(row=0, column=0, pady=2)

            visualize_button = ctk.CTkButton(buttons_frame,
                                             text="Visualizza/Modifica",
                                             width=100, height=30, hover_color="green",
                                             command=lambda: visualize_log(log_name,
                                                                           decrypted_log_content,
                                                                           left_frame))
            visualize_button.grid(row=0, column=1, pady=2)


    except Exception as e:
        print(e)


def delete_log(log, left_frame, LOGS_PATH, key):
    """Funzione che elimina un log"""

    if messagebox.askyesno("", "Vuoi davvero eliminare la pagina?"):
        os.remove(f"{LOGS_PATH}/{log}")
        refresh_logs(load_logs(LOGS_PATH, key), left_frame, LOGS_PATH, key)


def update_log(log, visualize_text, visualize_frame, left_frame):
    """Funzione che aggiorna un log"""

    encrypted_data = encrypt_data(visualize_text.get("1.0", ctk.END), key)

    with open(f"{LOGS_PATH}/{log}", "wb") as file:
        file.write(encrypted_data)

    visualize_frame.destroy()
    refresh_logs(load_logs(LOGS_PATH, key), left_frame, LOGS_PATH, key)

    messagebox.showinfo("","Pagina salvata con successo!")


def save_log(data, key, LOGS_PATH):
    """Funzione che salva un log sul file system"""
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    encrypted_data = encrypt_data(data, key)
    with open(f"{LOGS_PATH}/{timestamp}.txt", "wb") as file:
        file.write(encrypted_data)

    return f"{LOGS_PATH}/{timestamp}.txt"


def load_logs(LOGS_PATH, key):
    """Funzione che carica i log dal file system"""

    try:
        file_contents = {}

        for entry in os.scandir(LOGS_PATH):
            if entry.is_file():
                with open(entry.path, 'rb') as file:
                    encrypted_text = file.read()
                    file_contents[entry.name] = decrypt_data(encrypted_text, key)
        return file_contents
    except FileNotFoundError:
        return {}
    except InvalidToken:
        return {}


def calculate_quality(satisfaction_level,
                      mood_level,
                      stress_level,
                      physical_activity,
                      social_relations):
    """Funzione che calcola la qualità della giornata con pesi diversi per ogni fattore"""

    # Definisco i pesi per ciascun fattore
    weights = {
        'satisfaction_level': 0.3,
        'mood_level': 0.3,
        'stress_level': 0.1,
        'physical_activity': 0.15,
        'social_relations': 0.15
    }

    #Calcolo il valore pesato per ciascun fattore
    weighted_stress = stress_level * weights['stress_level']
    weighted_satisfaction = satisfaction_level * weights['satisfaction_level']
    weighted_mood = mood_level * weights['mood_level']
    weighted_physical_activity = physical_activity * weights['physical_activity']
    weighted_social_relations = social_relations * weights['social_relations']

    quality = (weighted_satisfaction + weighted_mood + weighted_physical_activity +
               weighted_social_relations + weighted_stress)

    return quality


def on_closing_root(root):
    """Funzione che gestisce la chiusura della finestra principale"""

    if messagebox.askokcancel("Quit", "Vuoi davvero chiudere MaiDiary?"):
        root.quit()


def create_main_frame(root):
    """Funzione che crea il frame principale"""

    main_frame = ctk.CTkFrame(root, corner_radius=20)
    #voglio che il frame prenda tutto lo spazio
    main_frame.pack(side="top", expand=True, fill="both", pady=10, padx=10)

    #Logo al programma
    logo_label = tk.Label(main_frame, image=root.logo_image)
    logo_label.pack(side="top", pady=10)

    # Etichetta di benvenuto stampata a capo
    welcome_label = ctk.CTkLabel(main_frame,
                                 text="Keep control, of your days",
                                 font=("Helvetica", 16))
    welcome_label.pack(side="top", pady=10)

    user_label = ctk.CTkLabel(main_frame,
                                text="Username:",
                                font=("Helvetica", 14))
    user_label.pack(side="top", pady=5)

    user_entry = ctk.CTkEntry(main_frame,
                                width=300,
                                font=("Helvetica", 14))
    user_entry.pack(side="top", pady=5)

    password_label = ctk.CTkLabel(main_frame,
                                text="Password:",
                                font=("Helvetica", 14))
    password_label.pack(side="top", pady=5)

    password_entry = ctk.CTkEntry(main_frame,
                                width=300,
                                font=("Helvetica", 14),
                                show="*")
    password_entry.pack(side="top", pady=5)


    version_label = ctk.CTkLabel(main_frame,
                                 text=f"Versione {VERSION}",
                                 font=("Helvetica", 12))
    version_label.pack(side="bottom", pady=5)

    # Pulsante per accedere alla pagina di inserimento
    btn_continue = ctk.CTkButton(main_frame,
                                 width=250, height=50, text_color="white",
                                 text="Go to your MaiDiary",
                                 command=lambda: show_diary_page(root,
                                                                 main_frame,
                                                                 user_entry,
                                                                 password_entry))
    btn_continue.configure(font=("Helvetica", 20))
    btn_continue.pack(side="top", pady=10)

    return main_frame


def main(root, Test):
    """Funzione principale del programma"""

    root.title("Maidiary by Peppe Blunda")

    #Associo la funzione di chiusura personalizzata all'evento di chiusura della finestra principale
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing_root(root))

    root.geometry("800x600")
    root.resizable(width=True, height=True)

    root.logo_image = tk.PhotoImage(file="MaiDiary_Logo.png")

    # Configurazione del frame principale
    main_frame = create_main_frame(root)
    main_frame.pack(side="top", expand=True, fill="both", pady=10, padx=10)

    if Test:
        root.quit()
    else:
        root.mainloop()


def show_diary_page(root, main_frame, user_entry, password_entry):
    """Funzione che mostra la pagina di inserimento del diario"""

    global LOGS_PATH
    global key
    username = user_entry.get()
    password = password_entry.get()
    LOGS_PATH  = f"users/{username}_diary"
    salt = username.encode()
    key = generate_key(password, salt)

    #controllo se i campi sono vuoti
    if username == "" or password == "":
        messagebox.showwarning("Errore", "È necessario compilare tutti i campi!")
        return

    if not os.path.exists(f"users/{username}_diary"):
        #chiedere se si vuole creare un nuovo utente
        if messagebox.askyesno("Nuovo utente", "Utente non trovato.\nVuoi crearne uno nuovo?"):
            os.makedirs(f"users/{username}_diary")
        else:
            return

    logs = load_logs(LOGS_PATH, key)

    if logs == {}:
        messagebox.showwarning("Errore", "Password o username errati!")
        return

    if(main_frame.winfo_exists()):
        main_frame.destroy()

    left_frame = ctk.CTkScrollableFrame(root,
                                        corner_radius=20,
                                        fg_color="#D3E3F9",
                                        width=300)
    left_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    right_frame = ctk.CTkFrame(root,
                               corner_radius=20,
                               fg_color="#D3E3F9",
                               width=390)
    right_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)

    # Faccio il refresh dei log
    refresh_logs(logs,left_frame, LOGS_PATH, key)

    # Frame in alto a destra
    top_right_frame = ctk.CTkFrame(right_frame,
                                   corner_radius=20,
                                   fg_color="#D3E3F9")
    top_right_frame.pack(side="top",expand=True, fill="both", padx=5, pady=5)

    # Frame in basso a destra
    bottom_right_frame = ctk.CTkFrame(right_frame,
                                      corner_radius=20,
                                      fg_color="#D3E3F9")
    bottom_right_frame.pack(side="bottom", expand=True, fill="both",
                            padx=5, pady=5, anchor=tk.CENTER)
    bottom_right_frame.grid_rowconfigure(0, weight=1)
    bottom_right_frame.grid_rowconfigure(1, weight=1)
    bottom_right_frame.grid_rowconfigure(2, weight=1)
    bottom_right_frame.grid_rowconfigure(3, weight=1)
    bottom_right_frame.grid_rowconfigure(4, weight=1)
    bottom_right_frame.grid_rowconfigure(5, weight=1)
    bottom_right_frame.grid_columnconfigure(0, weight=1)
    bottom_right_frame.grid_columnconfigure(1, weight=1)

    #Area di inserimento del diario
    diary_entry = ctk.CTkTextbox(top_right_frame,
                                 border_color="#D3E3F9",
                                 font=("Helvetica", 15),
                                 corner_radius=20,
                                 scrollbar_button_color="#D3E3F9")
    diary_entry.pack(expand=True,fill="both", padx=5, pady=5)

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
    def mostra_s_val(value):
        text_s.set(f"Soddisfazione: {int(satisfaction_slider.get())}")

    def mostra_st_val(value):
        text_st.set(f"Stress: {int(stress_slider.get())}")

    def mostra_m_val(value):
        text_m.set(f"Mood: {int(mood_slider.get())}")

    def mostra_pa_val(value):
        text_pa.set(f"Attività Fisica: {int(ph_act_slider.get())}")

    def mostra_so_val(value):
        text_so.set(f"Relazioni Sociali: {int(social_slider.get())}")


    #Slider e labels per la soddisfazione
    satisfaction_label = ctk.CTkLabel(bottom_right_frame,
                                      textvariable=text_s,
                                      font=("Helvetica", 15))
    satisfaction_label.grid(row=0, column=0, pady=5)
    satisfaction_slider = ctk.CTkSlider(bottom_right_frame,
                                        from_=0, to=10, number_of_steps=10,
                                        command=mostra_s_val)
    satisfaction_slider.grid(row=0, column=1, pady=5)
    satisfaction_slider.set(0)

    #Slider e labels per il mood
    mood_label = ctk.CTkLabel(bottom_right_frame,
                              textvariable=text_m,
                              font=("Helvetica", 15))
    mood_label.grid(row=1, column=0, pady=5)
    mood_slider = ctk.CTkSlider(bottom_right_frame,
                                from_=0, to=10, number_of_steps=10,
                                command=mostra_m_val)
    mood_slider.grid(row=1, column=1, pady=5)
    mood_slider.set(0)

    #Slider e labels per lo stress
    stress_label = ctk.CTkLabel(bottom_right_frame,
                                textvariable=text_st,
                                font=("Helvetica", 15))
    stress_label.grid(row=2, column=0, pady=5)
    stress_slider = ctk.CTkSlider(bottom_right_frame,
                                  from_=0, to=10, number_of_steps=10,
                                  command=mostra_st_val)
    stress_slider.grid(row=2, column=1, pady=5)
    stress_slider.set(0)

    #Slider e labels per le attività fisiche
    ph_act_label = ctk.CTkLabel(bottom_right_frame,
                                textvariable=text_pa,
                                font=("Helvetica", 15))
    ph_act_label.grid(row=3, column=0, pady=5)
    ph_act_slider = ctk.CTkSlider(bottom_right_frame,
                                  from_=0, to=10, number_of_steps=10,
                                  command=mostra_pa_val)
    ph_act_slider.grid(row=3, column=1, pady=5)
    ph_act_slider.set(0)

    #Slider e labels per le relazioni sociali
    social_label = ctk.CTkLabel(bottom_right_frame,
                                textvariable=text_so,
                                font=("Helvetica", 15))
    social_label.grid(row=4, column=0, pady=5)
    social_slider = ctk.CTkSlider(bottom_right_frame,
                                  from_=0, to=10, number_of_steps=10,
                                  command=mostra_so_val)
    social_slider.grid(row=4, column=1, pady=5)
    social_slider.set(0)


    #Pulsante per fare il submit
    btn_submit = ctk.CTkButton(bottom_right_frame,
                               width = 140, height = 28,
                               text_color = "#D3E3F9", text="INVIA",
                               command=lambda: submit_entry(key,LOGS_PATH))
    btn_submit.grid(row=5, column=0, columnspan=2, pady=5)
    btn_submit.configure(font=("Helvetica", 14))


    def submit_entry(key,LOGS_PATH):
        date_str = datetime.datetime.now().strftime("%d/%m/%Y, ore %H:%M:%S")
        diary_text = diary_entry.get("1.0", ctk.END).strip()
        stress_level = int(stress_slider.get())
        satisfaction_level = int(satisfaction_slider.get())
        mood_level = int(mood_slider.get())
        physical_activity = int(ph_act_slider.get())
        social_relations = int(social_slider.get())

        # Reset dei valori dei cursori dopo l'invio
        satisfaction_slider.set(0)
        mostra_s_val(0)
        stress_slider.set(0)
        mostra_st_val(0)
        mood_slider.set(0)
        mostra_m_val(0)
        ph_act_slider.set(0)
        mostra_pa_val(0)
        social_slider.set(0)
        mostra_so_val(0)

        # Calcolo della qualità della giornata
        quality_of_day = calculate_quality(satisfaction_level,
                                            mood_level,
                                            stress_level,
                                            physical_activity,
                                            social_relations)
        if diary_text:
            log = (f"Pagina del {date_str}\nValutazione giornata: {quality_of_day}\n"
            f"Valutazioni singole:\n - Soddisfazione: {satisfaction_level}\n"
            f" - Mood: {mood_level}\n - Stress: {stress_level}\n"
            f" - Attività Fisica: {physical_activity}\n - Relazioni Sociali: {social_relations}\n"
            f"\n{diary_text}")

            path = save_log(log, key, LOGS_PATH)
            refresh_logs(load_logs(LOGS_PATH, key), left_frame, LOGS_PATH, key)
            diary_entry.delete("1.0", ctk.END)

            #Reset degli slider
            stress_slider.set(0)
            satisfaction_slider.set(0)
            mood_slider.set(0)
            ph_act_slider.set(0)
            social_slider.set(0)
            messagebox.showinfo("","Pagina salvata con successo!")


        else:
            messagebox.showwarning("Errore", "Il testo del diario non può essere vuoto.")
        print("fine della funzione show_diary_page")


if __name__ == "__main__":
    root = ctk.CTk()
    main(root, Test=False)
