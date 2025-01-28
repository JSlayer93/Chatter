# PyChat: A Simple Python Chat Application

PyChat is a basic chat application built using Python, PyQt5 for the graphical user interface, and MongoDB for the backend database. It allows users to create accounts, join chat rooms, and exchange messages.

## Features

- **User Authentication:** Secure user registration and login with password hashing (using bcrypt).
- **Chat Rooms:** Create and join chat rooms with optional passwords and user limits.
- **Messaging:** Send and receive text messages within chat rooms.
- **Basic GUI:** A simple and intuitive graphical user interface built with PyQt5.

## Installation

### Prerequisites

- **Python 3.7+:** Ensure you have Python 3.7 or higher installed on your system. You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
- **MongoDB:** You need a running MongoDB server. You can download and install MongoDB Community Edition from [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community). Instructions for setting up a MongoDB server can be found in the official MongoDB documentation.

### Installation Steps

1. **Clone the repository:**
   ```
   git clone https://github.com/your-username/PyChat.git  # Replace with your repository URL
   cd PyChat
   
2. **Create a virtual environment:**
    ```
    python3 -m venv .venv
    source .venv/bin/activate   # Activate the virtual environment (Linux/macOS)
    .venv\Scripts\activate     # Activate the virtual environment (Windows)

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    
4. **Set up environment variables**

-   Create a file named .env in the project's root directory.
-   Add your MongoDB connection string to the .env file (replace <your_connection_string> with your actual MongoDB connection URI):
    ```
    DATABASE="mongodb://<your_connection_string>"
    
5. **Run the application**

    ```bash
    python main.py