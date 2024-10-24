# ASU Online assistant

## Problem Statement
ASU Online provides a comprehensive set of FAQs, but users often struggle to find the most relevant answers quickly. Searching through static FAQ pages can be inefficient, leading to frustration and delays in accessing important information.

### Proposed Solution
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

### Running it
basically run the main jupyter file:
```bash
jupyter notebook 01_rag_flow.ipynb
```

## Evaluation
To have a look at the code that is evaluating the system, you can check the latter portion in [01_rag_flow.ipynb](01_rag_flow.ipynb).

We are basically using the following for our RAG:
- knowledge base: in-house search engine 'minsearch' fitted to ASU online FAQs.
- LLM: openAI model such as gpt-4o-mini.

### Retrieval
For the basic approach, that is, not using any boosting when using minsearch, we get the following metrics:
- Hit rate: 0.74
- Mean Reciprocal Rank: 0.47

Using hyperopt, we optimize the boost values so that question gets boosted by 0.2 and section by 0.07, thus giving us the following metrics:
- Hit rate: 0.94
- Mean Reciprocal Rank: 0.77

#### Interesting notes about optimal boost values being <1.
We can notice that hyperopt has found a boost on the question to be ~0.2, which is a tad counterintuitive as one would figure the actual question would be of significant importance to get a good response in our search engine.

Turns out, there are multiple reasons for the question boost value to be <1:
- balance between fields: a high boost value on question may overshadow any contributions from the section component, so you may need lower the boost value for questions to even things out with the section field.
- field quality: the question actually may be a bit too generic or ambiguous and the section field may provide additional context.
- field overfitting: a high boost value on the question may make the search engine to prioritize exact matches, so to help the engine find relevant results that are not quite exact, you may need to reduce the boost.
- search engine sensitivity: maybe the minsearch engine is too sensitive to boost values and it may miss subtle but relevant matches if the value is too high.


### RAG flow
We used the cosine similarity metric to evaluate the performance of our RAG flow given different openAI models.

We evaluated 256 ground truths using both gpt-4o-mini and gpt-4o.

The results were as follows:

![cosine-similarity](cosine-similarity-image.png)

We see that the performance is relatively equivalent, with gpt-4o performing slightly better.

In the interest of economy we will proceed with gpt-4o mini, since that one is ~10x cheaper than gpt-4o.

## Monitoring