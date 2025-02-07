# Virtual Book Library

## Overview
The **Virtual Book Library (VBL)** is a **desktop application** developed using **CustomTkinter**, **SQLite**, and **Pillow** to provide an interactive and user-friendly interface for managing books. Users can register, log in, add new books, track reading progress, and analyze their book collection with ease.

## Features
- **User Authentication**: Register and log in with secure credentials.
- **Book Management**: Add, update, and delete books.
- **Reading Timer**: Track reading time for each book.
- **Book Analysis**: Generate insights on reading habits.
- **Search & Filter**: Quickly find books using search functionality.
- **Data Persistence**: Stores book data securely in an SQLite database.

## Installation
### Prerequisites
- Python (>=3.8)
- Required Libraries:
  ```bash
  pip install customtkinter tkinter tkcalendar pandas pandastable pillow pygame opencv-python 
  ```

### Running the Application
```bash
python VBL_App.py
```

## Usage Guide
### 1. User Registration & Login
- Users must register with their **name, email, username, and password**.
- Upon login, users are redirected to the **Dashboard**.

### 2. Managing Books
- **Read New Book**: Enter book details including title, author, genre, and number of pages.
- **Read Existing Book**: Resume reading a previously added book.
- **Track Reading Time**: Use the built-in timer to measure reading duration.
- **Update Book Details**: Modify book attributes using a dynamic checkbox form.

### 3. Book Analysis
- Displays statistics on reading habits.
- Tracks books completed, time spent, and ratings.

## Code Structure
- **Book_App.py**: Main application file.
- **Connect_DB.py**: Handles database interactions.
- **img/**: Stores UI-related images.

## Future Enhancements
- Implement an **export to CSV** feature.
- Add **dark mode & themes**.
- Enhance **book analysis visualization**.

## To create executable of the app 
(**Visit Here**)[Pyinstaller.md]

## License
This project is open-source and free to use under the MIT License.

---
For any issues or improvements, feel free to contribute or contact the developer!

