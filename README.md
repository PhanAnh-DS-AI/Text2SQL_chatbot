# Text2SQL Chatbot

This project aims to build a robust pipeline for a **Text2SQL chatbot** that empowers users to query databases using natural language. The chatbot processes user input, converts it into SQL queries, and retrieves the relevant data from the database. This approach simplifies data access, making it accessible to non-technical users without requiring any knowledge of SQL.

## Features:
- **Natural Language Processing (NLP)**: Converts user queries into valid SQL queries.
- **Database Querying**: Retrieves relevant data from databases seamlessly.
- **User-Friendly**: No SQL knowledge required to interact with the system.

---

## Dataset

The project uses the **Travel2 dataset** for querying:

1. Download the `travel2.sqlite` dataset from the following link:  
   [Travel2 Dataset](https://storage.googleapis.com/benchmarks-artifacts/travel-db/travel2.sqlite)
   
2. Place the downloaded file into the `Data/` directory of your project.

---

## Requirements

To get started with the project, make sure to install the necessary Python libraries. You can install the required dependencies by following these steps:

1. Create a virtual environment (if not already done):
   ```bash
   python -m venv venv
   
2. Activate the virtual environment:
.\venv\Scripts\activate

3. Install the required libraries using pip:
pip install -r requirements.txt

The requirements.txt file includes all the necessary libraries for the project, including NLP tools, database connectors, and model dependencies.

---
## Model API Integration

- SET up **API Key** in config.py: To use the model, integrate your API key from a service such as **ChatGroq** or **Gemini** for natural language processing tasks.

---

## ChromaDB Setup

To initialize and set up ChromaDB for the project:

1. Load the `swiss.faq` file.
2. Navigate to the `helpers/chroma_helpers` directory.
3. Run the `setup_chroma` script to create the Chroma database.

Once completed, the Chroma database will be ready for use in the chatbot's querying process.

---

Running the Application
Once you have completed the setup, you can run the chatbot by executing the main.py script.

Ensure that all dependencies are installed and the virtual environment is activated.
Run the following command to start the chatbot

python main.py

This will launch the chatbot, and you will be able to interact with the database by submitting natural language queries.

---

Feel free to reach out with any questions or suggestions for further improvements!
