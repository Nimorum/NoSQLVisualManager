# NoSQL Visual Manager

The NoSQL Visual Manager is a Python-based GUI tool designed to simplify the management of **both NoSQL and SQL databases**, including **MongoDB** and **MySQL**. The application provides a user-friendly interface to interact with databases, allowing users to run queries, manage collections/tables, and perform CRUD operations visually.

Additionally, the system is extensible, meaning it can support **any database** as long as an implementation of the `AbstractClient` interface is added.

---

## Features

### **Connect to Multiple Databases**
- **MongoDB**: Use a connection string to connect to a MongoDB instance.
- **MySQL**: Connect to MySQL databases using standard credentials.
- **Extensibility**: Implement the `AbstractClient` interface to add support for other databases.

### **Raw Query Execution**
- A **new dedicated query execution screen** allows running **SQL** and **NoSQL** queries.
- **Syntax Highlighting**: Keywords and operators are visually distinguished.
- **Query Selection Execution**: Run either a selected part of a query or the entire input.

### **Visual Data Interaction**
- View and manage **databases, collections, and tables** in a tabular format.
- Perform **CRUD** (Create, Read, Update, Delete) operations visually.
- Filter, sort, and paginate results easily.

### **Dynamic UI Panels**
- **Raw Query Window** for direct query execution.
- **Add Row & Edit Panels** for structured data entry.
- **Confirmation Dialogs** to prevent unintended modifications.

### **Mock Data Mode**
- Enable mock data for testing without requiring a live database connection.

---

## Installation Instructions

### **Clone or Download the Repository**
Ensure all project files are in a single directory.

### **Setup a Virtual Environment (Optional but Recommended)**

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

### **Install required Python packages**
```bash
pip install -r requirements.txt
```

---

## Execution Instructions

### **Run the Application**
1. Navigate to the project directory:
   ```bash
   cd NoSQLVisualManager
   ```
2. Run the main file:
   ```bash
   python main.py
   ```

### **Connect to a Database**
1. In the connection panel:
   - **For MongoDB**, enter a connection string (e.g., `mongodb://localhost:27017`).
   - **For MySQL**, enter credentials (e.g., `mysql://user:password@localhost:3306/database`).
   - Additional databases can be added by implementing `AbstractClient`.

2. Click **"Connect"** to establish the connection.

---

## **Using the Raw Query Window**
The **Raw Query Window** allows users to execute queries directly on their database.

### **How to Open the Raw Query Screen**
- Click the **"Raw Query"** button from the main interface.

### **Running a Query**
1. Enter the query in the text box.
2. Select part of the query to execute **only that section**, or leave it unselected to run the entire input.
3. Click **"Execute"** to run the query.

### **Examples**
- **SQL Query Example**:
  ```sql
  SELECT * FROM users WHERE age > 25;
  ```
- **MongoDB Query Example**:
  ```json
  db.users.find({ "age": { "$gt": 25 } })
  ```

---

## File Structure

- **`main.py`**: Entry point of the application.
- **`requirements.txt`**: Contains the list of dependencies.
- **`config.json`**: Stores application settings and connection strings.

### **Directories**
- **`business/`**: Handles business logic and interaction between UI and database.
  - `business_manager.py`
  - `config.py`
- **`db/`**: Handles database interaction logic.
  - `abstract_client.py` (Defines the contract for all database clients)
  - `mongodb_client.py` (MongoDB implementation)
  - `mysql_client.py` (MySQL implementation)
  - `repository.py`
- **`ui/`**: Contains all UI-related modules.
  - `main_window.py`
  - `raw_query_window.py` (New!)
  - `add_row_panel.py`
  - `confirmation_window.py`
  - `connection_window.py`

---

## **Extending Support to Other Databases**
NoSQL Visual Manager is built to be **database-agnostic**. To add support for a new database:
1. Implement a new class that follows the **`AbstractClient`** interface.
2. Add the new client to the connection logic in **`main.py`**.
3. Define how queries should be executed for the new database.

For example, to add PostgreSQL:
- Create `postgres_client.py` implementing `AbstractClient`.
- Modify `main.py`:
  ```python
  if connection_string.startswith("postgresql"):
      client = PostgreSQLClient(connection_string)
  ```

---

## **Notes**
- Ensure **MongoDB** or **MySQL** is running and accessible via the connection string.
- Use **`MockClient`** for testing if a live database is not available.

---

## **Future Improvements**
- Support for more databases like **PostgreSQL**, **Cassandra**, and **SQLite**.
- Improved **query visualization** and **execution logs**.
- Additional **bulk operations** and **schema analysis tools**.

---

This update reflects the **new SQL support, query execution screen, and extensibility for future databases.** 🚀