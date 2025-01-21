# steganoweb

## Overview
**steganoweb** è un'applicazione web per la steganografia. Utilizza un backend scritto in Python per nascondere messaggi all'interno di immagini.

## Features
- **Steganografia**: Nasconde messaggi all'interno di immagini.
- **Facile da usare**: Interfaccia web semplice e intuitiva.
- **Leggero e veloce**: Scritto in Python per prestazioni ottimali.

## Application Information
- **Name**: steganoweb
- **Version**: 1.0.0
- **Author**: @ilgigante77
- **Website**: [https://github.com/tanadelgigante/steganoweb](https://github.com/tanadelgigante/steganoweb)

## Getting Started

### Prerequisites
- Python 3.8+
- Docker (opzionale per il deployment containerizzato)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/tanadelgigante/steganoweb.git
    cd steganoweb
    ```

2. **Setup the backend**:
    Assicurati di avere il file `main.py` preso dal progetto [Steganograpp](https://github.com/chtholine/Steganograpp) al quale però non siamo affiliati.

### Configuration

1. **Server Setup**:
   Configura il backend con il file `main.py` per avviare il server di steganografia.

### Running the Application

1. **Run Locally**:
    ```bash
    python main.py
    ```

2. **Using Docker**:
   Crea un Dockerfile per l'applicazione:
    ```dockerfile
    # Fase di build
    FROM python:3.8-slim

    WORKDIR /app

    # Copia i file necessari
    COPY . .

    # Installa le dipendenze
    RUN pip install -r requirements.txt

    # Comando di esecuzione dell'applicazione
    CMD ["python", "main.py"]
    ```

   Build and run the Docker container:
    ```bash
    docker build -t steganoweb .
    docker run steganoweb
    ```

### Usage

#### Web Interface
- **Steganografia**:
    Accedi all'interfaccia web e segui le istruzioni per nascondere un messaggio all'interno di un'immagine.

### Debugging

- Usa i log dell'applicazione per monitorare le operazioni di steganografia. Cerca messaggi `[INFO]` e `[DEBUG]` nell'output della console.

### Contributing
Le contribuzioni sono benvenute! Fai un fork del repository e invia pull request per miglioramenti o correzioni di bug.

### License
Questo progetto è concesso in licenza sotto la GPL 3.0 License. Vedi il file [LICENSE](LICENSE) per i dettagli.

### Disclaimer
Questo progetto è rilasciato "as-is" e l'autore non è responsabile per danni, errori o uso improprio.

## Contact
Per maggiori informazioni, visita [https://github.com/tanadelgigante/steganoweb](https://github.com/tanadelgigante/steganoweb).
