# Keylogger System

## Overview

This project is a modular **Keylogger System** designed to **capture keystrokes**, **encrypt logs**, and **store them
securely** in multiple formats. It follows a **flexible and extensible architecture** with clear separation of concerns,
allowing easy modification and expansion.

## Features

- **Keystroke Logging** – Captures user input from the keyboard.
- **Application Focus Logging** – Tracks which application was active during keystroke input.
- **Encryption Support** – Encrypts logs using **XOR Encryption** (can be extended for stronger methods).
- **Multiple Log Writers**:
    - **ConsoleLogWriter** – Displays logs in the console.
    - **FileLogWriter** – Stores logs in a `.txt` file.
    - **JsonLogWriter** – Saves logs in a structured JSON format.
- **Configurable Log Interval** – Periodically processes and writes logs every **X seconds**.
- **Thread-Safe Design** – Atomic operations ensure safe execution.
- **Flexible and Extensible** – Supports additional log writers, encryption mechanisms, and output destinations.

## System Architecture

The project is structured as follows:

```
keylogger_project/
│── keylogger/
│   ├── interfaces/
│   │   ├── EncryptorInterface.py   # Defines encryption methods
│   │   ├── KeyloggerInterface.py   # Defines keylogger behavior
│   │   ├── LogWriterInterface.py   # Defines logging behavior
│   ├── encryptors/
│   │   ├── XorEncryption.py        # Implements XOR encryption
│   ├── keyloggers/
│   │   ├── SimpleKeylogger.py      # Captures keystrokes
│   ├── logwriters/
│   │   ├── ConsoleLogWriter.py     # Writes logs to console
│   │   ├── FileLogWriter.py        # Writes logs to a text file
│   │   ├── JsonLogWriter.py        # Writes logs to JSON
│   ├── manager/
│   │   ├── KeyLoggerManager.py     # Central component that collects and processes logs
│── main.py                         # Initializes and runs the keylogger system
│── README.md                        # Project documentation
```

## Flowchart

Below is the **logical flow** of how the system operates:

```mermaid
graph TD;
    A[Start] -->|Initialize Components| B[KeyLoggerManager]
    B --> |Start Keylogger| C[SimpleKeylogger Captures Keystrokes]
    C --> D[Application Focus Logging]
    D --> E[Store Logs in Buffer]
    E --> |Every X Seconds| F[Encrypt Logs]
    F --> G[Write Logs to Output (Console, File, JSON)]
    G -->|Repeat Until Stopped| B
    B -->|Stop Keylogger| H[End]
```

## Installation & Setup

### Prerequisites

Ensure you have **Python 3.8+** installed and install required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Keylogger

To start the system, execute:

```bash
python main.py
```

### Configuration Options

Modify the `KeyLoggerManager` settings in `main.py` to change:

- **Logging interval** (default: 10 seconds)
- **Output format** (Console, File, JSON)
- **Encryption method** (default: XOR)

## How It Works

1. `KeyLoggerManager` starts and initializes components.
2. `SimpleKeylogger` captures **keystrokes** and **active application**.
3. Logs are stored in an **internal buffer**.
4. Every **X seconds**, logs are **retrieved, timestamped, encrypted, and written** to output files.
5. The process repeats until the system is manually stopped.

## Future Enhancements

- **Support for Asynchronous Execution (`asyncio`)**
- **More Advanced Encryption (AES, RSA)**
- **Remote Log Transmission (Network Writer, Cloud Storage)**
- **Data retrieval and view via Web Interface**

---
**Disclaimer:** This tool is for educational and security research purposes only. Unauthorized usage may violate privacy
laws.