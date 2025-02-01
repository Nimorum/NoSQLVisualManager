# NoSQL Visual Manager

The NoSQL Visual Manager is a Python-based GUI tool designed to simplify the management of NoSQL databases, primarily MongoDB. The application allows users to interact with databases and collections visually, enabling actions such as adding, editing, deleting, and querying data with ease. It is ideal for developers and administrators who need a lightweight and user-friendly interface for managing NoSQL databases.

---

## Features

### Connect to MongoDB
- Use a connection string to connect to a MongoDB instance.
- Save and reuse connection strings for convenience.

### Visual Data Interaction
- View and manage databases, collections, and documents in a tabular format.
- Perform CRUD (Create, Read, Update, Delete) operations.

### Query Support
- Filter, sort, and paginate data directly from the GUI.
- Use MongoDB aggregation pipelines for advanced queries.

### Dynamic UI Panels
- Add rows, confirm actions, and customize filters dynamically.

### Mock Data Mode
- Enable mock data for testing without connecting to a live database.

---

## Installation Instructions

### Clone or Download the Repository
Ensure all project files are in a single directory.

### Setup a Virtual Environment (Optional but Recommended)

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate.bat
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

### Install required Python packages
```bash
pip install -r requirements.txt
```

---

## Execution Instructions

### Run the Application
1. Navigate to the project directory:
   ```bash
   cd NoSQLVisualManager
   ```

2. Run the main file:
   ```bash
   python main.py
   ```

### Connect to MongoDB
1. On the connection panel:
   - Enter a valid MongoDB connection string (e.g., `mongodb://localhost:27017`).
   - Or select a saved connection from the dropdown.

### Browse and Manage Data
- Explore available databases and collections.
- Perform queries, sort, and paginate through data using the intuitive interface.

### Perform Operations
- Add new documents using the **Add Document** button.
- Delete records directly from the UI.
- Edit values by double-clicking on the value to update.
- Sort by clicking on the column header.

### Use Mock Data (Optional)
Click the **Use Mock Data** button on the connection panel to simulate a database environment.

---

## File Structure

- **`main.py`**: Entry point of the application.
- **`requirements.txt`**: Contains the list of dependencies.
- **`config.json`**: Stores application settings and connection strings.

### Directories
- **`business/`**: Handles business logic and interaction between UI and database.
  - `business_manager.py`
  - `config.py`
- **`db/`**: Handles database interaction logic.
  - `abstract_client.py`
  - `mongodb_client.py`
  - `repository.py`
- **`ui/`**: Contains all UI-related modules.
  - `main_window.py`
  - `add_row_panel.py`
  - `confirmation_window.py`
  - `connection_window.py`

---

## Notes

- Ensure MongoDB is running and accessible via the connection string.
- Use the `mock_client.py` for testing if MongoDB is not available.

---

## Future Improvements

- Add support for other NoSQL databases (e.g., CouchDB, Cassandra).
- Integrate additional query features like `$group` or `$lookup`.
- Enhance UI for bulk operations and schema analysis.