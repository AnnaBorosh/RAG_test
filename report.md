# Multimodal RAG System – Project Report

### 1. **Overview**
This project implements a Multimodal Retrieval-Augmented Generation (RAG) system that answers user questions by retrieving relevant news articles from [The Batch](https://www.deeplearning.ai/the-batch/) and presenting both textual and visual data to the user. The goal was to build a pipeline integrating data ingestion, vector search, LLM generation and a user interface that ties it all together.

---

### 2. **Approach**
1. Data Ingestion
   Articles from The Batch are scraped using a custom Python script with BeautifulSoup, extracting:
   - Title  
   - Full text content  
   - Article image  
   - Source URL

2. **Embedding and Indexing**  
   Extracted text is stored in Pinecone, a vector database. Integrated embedding with already hosted `llama-text-embed-v2` model. Each article is stored with metadata (`title`, `image_url`, `link`) in an index.

3. **Query + Retrieval**  
   The system uses Pinecone's hosted model embedding to convert user queries into vectors and retrieve the top 3 most relevant articles.

4. **Answer Generation**  
   Retrieved text is passed to Gemini 1.5 Flash, which generates the final answer to the user’s question.

5. **Multimodal Display**  
   The answer is displayed in a Streamlit UI with: answer and  a related article image + article title + link  

6. **Deployment**
    The system has been deployed on Streamlit Cloud, making it easily accessible and testable by others without any setup.

---

### 3. **Tools Used**
| Component | Tool / Model |
|----------|--------------|
| UI        | Streamlit    |
| Vector DB | Pinecone     |
| LLM       | Gemini 1.5 Flash |
| Scraper   | BeautifulSoup |
| Format    | JSON         | 

---

### 4. **Reasoning**
- Gemini 1.5 Flash was selected because it's speedy and performs well (also the Gemini API free tier played a role)
- Pinecone was chosen because of hosted embedding models, which simplifies the workflow — no extra work with manual embedding.

---

### 5. **Evaluation**
The system performs well across a variety of query types. For example:
> Query: “What is Codex?” 
>
> Answer: "Codex is an agentic software-development system launched by OpenAI. Available as a preview via ChatGPT (for Pro, Enterprise, and Team users, with Plus and Edu coming soon), it acts like a team of virtual coworkers in the cloud. It uses agents to perform tasks such as writing code, running tests, and fixing bugs in parallel, operating directly on a user's code repository (locally or on GitHub)."


> Query: "What incident led to Grok making misleading claims about South Africa, and how did xAI respond?"
>
> Answer: "An unauthorized xAI employee circumvented the company's code-review process and modified Grok's system prompt. This prompt instructed Grok to accept and reflect the narrative of "white genocide" in South Africa, even in unrelated conversations. In response, xAI launched an investigation (though they didn't disclose details), implemented new code review checks, added monitoring to catch problems faster, prevented unauthorized prompt changes, and published the system prompt on GitHub for transparency and user feedback."

- The system accurately retrieves relevant content  
- Contextual answers are consistent with source material   

**Limitations:**
- New articles must be re-scraped manually

---

### 6. **Future Improvements**

- Extend scraper to support all archived issues of The Batch automatically  
- Add database update automation and periodic scraping  