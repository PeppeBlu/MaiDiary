# Usa una base image di Python
FROM python

# Imposta il working directory
WORKDIR /MaiDiary

# Copia il file requirements.txt e installa le dipendenze
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia il contenuto della directory corrente nella working directory
COPY . .

# Comando per eseguire l'applicazione
CMD ["python", "src/maidiary.py"]
