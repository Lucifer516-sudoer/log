# 😸 Cat Log - A Minimalist Journal
[![GitHub Repo](https://img.shields.io/badge/GitHub-log-blue?logo=github)](https://github.com/Lucifer516-sudoer/log)

**Cat Log** is a simple and intuitive journaling application built with the Flet framework. It allows users to record and view logs of their daily activities or thoughts, providing a smooth interface for adding, viewing, and managing journal entries.

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Features
- 📅 **Log Entry**: Easily add a journal entry with a timestamp and message.
- 🌗 **Theme Switching**: Toggle between light and dark modes for better readability.
- 📝 **View Logs**: Display logs in a clean and organized manner with the latest entries first.
- 🖼 **Minimal UI**: A floating action button and a simple dialog box for adding new logs.
- 🔄 **Auto Scroll**: Automatically scroll to the latest log entry for convenience.

## How It Works
1. Click the **floating action button** to open the "Add Entry" dialog.
2. Type in your log message and click "Add" to save it.
3. The log is displayed on the page with the timestamp.
4. Switch between light and dark themes using the **theme toggle button**.

## Installation

### Prerequisites
- Python 3.x
- Flet library (`pip install flet`)
- Ensure that `log` (your API and database handling module) is accessible.

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/Lucifer516-sudoer/log.git
   ```
2. Navigate to the project directory:
   ```bash
   cd log
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Run the application:
   ```bash
   poetry run python main.py
   ```

## Usage
- Upon launching the app, you can begin adding log entries by clicking the **floating action button** at the bottom of the screen.
- Logs will display with their timestamp and message in an organized list format.
- To switch between light and dark modes, click the theme toggle button.

## Project Structure
- `main.py`: The main application file that defines the Flet UI and interactions.
- `log.api`: Handles API communication for log data.
- `log.database.models`: Contains database models, such as `LogInfo` and `Message`.
- For further questions, just look into the codebase

## Future Enhancements
- 🗑 **Log Deletion**: Option to delete or edit logs.
- 🔍 **Search Functionality**: Add a search bar to filter through logs by keywords or date.

## License
This project is licensed under the MIT License - see the **LICENSE** file for details.
