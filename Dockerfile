# Usa una base image di Python
FROM python

# Imposta il working directory
WORKDIR /MaiDiary

# Copia il file requirements.txt e installa le dipendenze
RUN pip install --upgrade pip
RUN python -m pip install cryptography
RUN python -m pip install customtkinter
RUN python -m pip install pytest
RUN python -m pip install pylint
RUN python -m pip install hypothesis

# Copia il contenuto della directory corrente nella working directory
COPY . .

# Comando per eseguire l'applicazione
CMD ["python", "maidiary.py"]
