# ASU Online assistant

## Problem Statement
ASU Online provides a comprehensive set of FAQs, but users often struggle to find the most relevant answers quickly. Searching through static FAQ pages can be inefficient, leading to frustration and delays in accessing important information.

## Proposed Solution
This project implements a **Retrieval-Augmented Generation (RAG)** system to enhance the user experience by allowing users to query ASU Online’s FAQs and receive accurate, concise responses. The system uses a search engine to index the FAQs, retrieves the top 10 relevant results, and then generates a response using a lightweight LLM (gpt-4o-mini and similar).

## How to Run the Project

### Prerequisites
- Python 3.x
- A virtual environment (`.venv`) with necessary libraries installed
- OpenAI API key stored in a `.envrc` file

### Setup Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/anicolas91/LLM_ASU_assistant.git
    cd LLM_ASU_assistant
    ```
2. Create the virtual environment
    ```bash
    python -m venv .venv
    ```
3. Activate the virtual environment
    ```bash
    source .venv/bin/activate  # On macOS/Linux
    .\.venv\Scripts\activate  # On Windows
    ```
4. Install the required dependencies: Ensure all necessary libraries are installed:
    ```bash
    pip install -r requirements.txt
    ```
5. Set your OpenAI API key: The OpenAI API key is saved in a .envrc file. Make sure it contains:
    ```bash
    OPENAI_API_KEY=your-openai-api-key-here
    ```