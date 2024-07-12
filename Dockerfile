# Usa una base image di Python
FROM python

# Imposta il working directory
WORKDIR /MaiDiary

# Copia il file requirements.txt e installa le dipendenze
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y x11vnc xvfb fluxbox supervisor


# Configura il display
ENV DISPLAY=:99

# Avvia un server X virtuale in background
RUN Xvfb :99 -screen 0 1024x768x16 &


# Copia il contenuto della directory corrente nella working directory
COPY . .

# Aggiungi il file di configurazione di supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Comando per eseguire l'applicazione
#CMD ["python", "src/maidiary.py"]

# Avvia supervisord
CMD ["/usr/bin/supervisord"]
