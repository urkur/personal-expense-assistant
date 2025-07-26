# Personal Expense Assistant

This repository contains the source code for a personal expense assistant application. The application allows users to track their expenses by uploading receipts, automatically extracting relevant information, and providing insights into their spending habits.

## Features

- **Receipt Upload:** Users can upload images of their receipts.
- **Automatic Data Extraction:** The system uses a large language model to extract key information from receipts, such as store name, transaction time, total amount, and purchased items.
- **Expense Tracking:** All extracted data is stored in a structured format, allowing users to track their expenses over time.
- **Search and Filtering:** Users can search for specific receipts based on metadata (e.g., date range, amount) or by using natural language queries.
- **Interactive Chat Interface:** A user-friendly chat interface allows users to interact with the assistant, ask questions about their expenses, and get insights into their spending.

## Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** Gradio
- **Language Model:** Gemini 2.5 Flash
- **Database:** Firestore
- **Artifact Storage:** Google Cloud Storage

## Getting Started

### Prerequisites

- Python 3.9+
- Google Cloud SDK

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/personal-expense-assistant.git
   cd personal-expense-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud authentication:**
   ```bash
   gcloud auth application-default login
   ```

4. **Configure settings:**
   - Create a `settings.yaml` file from the `settings.yaml.example` template.
   - Fill in your Google Cloud project details.

### Running the Application

1. **Start the backend server:**
   ```bash
   python backend.py
   ```

2. **Start the frontend interface:**
   ```bash
   python frontend.py
   ```

   The application will be available at `http://localhost:8080`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.