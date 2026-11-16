# Company Knowledge Assistant – RAG System

## Overview

The **Company Knowledge Assistant** is an AI-powered application that uses Retrieval-Augmented Generation (RAG) to answer questions based on company documents.

Instead of generating answers only from general knowledge, the system retrieves relevant information from the provided documents and uses it to generate context-based responses.

## Features

- Upload and process company documents.
- Ingest documents into a searchable knowledge base.
- Retrieve relevant information based on user queries.
- Generate answers using a Retrieval-Augmented Generation approach.
- Support company-specific knowledge retrieval.

## Project Structure

```text
Company-Knowledge-Assistant/
│
├── app.py
├── ingest.py
├── query.py
├── requirements.txt
├── .gitignore
│
└── documents/
    └── hr_policy.txt
```

## Technologies Used

- Python
- Retrieval-Augmented Generation (RAG)
- Vector Database (ChromaDB)
- AI / Language Models

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/vksnRaju-06/Company-Knowledge-Assistant-A-Retrieval-Augmented-Generation-RAG-System-.git
```

**2. Navigate to the project directory**

```bash
cd Company-Knowledge-Assistant-A-Retrieval-Augmented-Generation-RAG-System-
```

**3. Create a virtual environment**

```bash
python -m venv venv
```

**4. Activate the virtual environment**

Windows:

```bash
venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

## Configuration

Configure the required API keys and environment variables in a `.env` file if your application requires them.

Do not upload your `.env` file or expose API keys on GitHub.

## Running the Project

**Step 1: Ingest documents**

```bash
python ingest.py
```

**Step 2: Run the application**

```bash
python app.py
```

If you want to query the knowledge base separately, run:

```bash
python query.py
```

## How It Works

1. **Document Ingestion:** Company documents are loaded into the system.
2. **Text Processing:** Documents are processed into smaller chunks.
3. **Embedding Generation:** Text chunks are converted into vector embeddings.
4. **Vector Storage:** Embeddings are stored in the vector database.
5. **Information Retrieval:** Relevant document chunks are retrieved when a user asks a question.
6. **Answer Generation:** The retrieved information is used to generate a context-based answer.

## Use Cases

- HR policy assistance
- Employee queries
- Company documentation search
- Internal knowledge management

## Future Enhancements

- Support for PDF and DOCX documents.
- Improved document retrieval.
- Chat history and conversation memory.
- User authentication.
- Support for multiple document collections.

## Author

**Project:** Company Knowledge Assistant – RAG System

