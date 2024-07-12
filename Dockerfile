# Usa una base image di Python
FROM python

# Imposta il working directory
WORKDIR /MaiDiary

# Copia la directory nella workdir  
COPY . .

# installa le dipendenze
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libx11-6 \
    libxext-dev libxrender-dev fonts-dejavu\
    libxinerama-dev libxi-dev libxrandr-dev \
    libxcursor-dev libxtst-dev tk-dev

# Comando per eseguire l'applicazione
CMD ["python", "src/maidiary.py"]