## ABHIMANYU_MV BACKEND

### Trade Mark Saarthi

An intelligent title verification and management system ensuring uniqueness, compliance, and streamlined workflows for title registration and comparison.

The backend is a robust and scalable system built with FastAPI, leveraging advanced libraries like FuzzyWuzzy, Metaphone, and NLTK for text and phonetic analysis. It integrates Milvus and Redis for efficient database and caching management, ensuring high performance for similarity checks and compliance rules. LangChain powers dynamic report generation, offering actionable insights from processed data.


##  Table of Contents

- [ABHIMANYU\_MV BACKEND](#abhimanyu_mv-backend)
  - [Trade Mark Saarthi](#trade-mark-saarthi)
- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Deploy on Railway](#deploy-on-railway)
  - [Installation](#installation)
- [Getting Started](#getting-started)
- [Learn More](#learn-more)


---

##  Overview

This project is designed to verify the accuracy and relevance of titles using a combination of efficient algorithms, vector databases, and similarity checks. By integrating techniques such as cosine similarity, fuzzy matching, and Levenshtein distance, the system ensures that titles align closely with their associated content. The use of Redis for quick data access further enhances the system's performance and scalability.

---

##  Features

- Vector Database Integration

Utilizes vector databases (such as Redis) to store and retrieve embeddings efficiently for quick similarity searches.
- Cosine Similarity Matching
Measures the similarity between title and content vectors to determine relevance by calculating cosine similarity scores.
- Fuzzy Matching
Implements fuzzy string matching techniques to handle partial matches and identify titles with slight variations or typos.
-  Levenshtein Distance
Calculates the edit distance between strings to detect minor discrepancies, such as spelling errors or character swaps.
-  Combination Algorithm
Combines multiple similarity measures to improve accuracy and reliability of title verification. It uses recursion and memoization for fast results over scalable data.
- Fast and Scalable
Utilizes Redis for rapid data storage and retrieval, making the system capable of handling large datasets efficiently.
- Text and Phonetic Analysis

FuzzyWuzzy: Performs approximate matching to identify similar titles based on text similarity.

Metaphone/Phonetics: Enables phonetic matching for sound-based comparisons.

NLTK: Handles NLP tasks like tokenization and stop words recognisation for deeper text analysis.

- Database Management:

Milvus: Maintains vector embeddings for fast similarity searches and title recommendations.

Redis: Serves as a caching layer for frequently accessed data, reducing latency.

- Dynamic Report Generation: 
Using LangChain, the system creates structured reports based on processed logic, including insights, summarized data, and actionable feedback.



---

##  Project Structure

```sh
└── trade-saarthi-backend/
    ├── API_flow.md
    ├── ReadMe.md
    ├── app.py
    ├── config
    │   ├── RedisConfig.py
    │   ├── __init__.py
    │   └── database.py
    ├── dataFiles
    │   ├── RestrictedPrefix.csv
    │   ├── RestrictedSuffix.csv
    │   ├── RestrictedWords.csv
    │   ├── final.csv
    │   ├── titlesWithCommonPreSuff.csv
    │   ├── titlesWithNonCommon.csv
    │   └── word_counts.csv
    ├── functions
    │   ├── AddCacheToRedis.py
    │   ├── CsvOperations.py
    │   ├── RestrictedListsFunctions.py
    │   └── __init__.py
    ├── models
    │   └── TradeMarkModel.py
    ├── requirements.txt
    ├── routes
    │   ├── RedisRoutes.py
    │   ├── RestrictedPrefixSuffixRoutes.py
    │   ├── RestrictedWordsRoutes.py
    │   ├── TitleCombinationRoute.py
    │   ├── TradeMarkRoute.py
    │   └── __init__.py
    └── utils
        └── path_utils.py
```


## Deploy on Railway

Check out our [Backend deployment](https://trade-saarthi-backend-production.up.railway.app/docs) to view hosted backend.


###  Installation

Install trade-saarthi-backend using one of the following methods:

**Build from source:**

1. Clone the trade-saarthi-backend repository:
```sh
❯ git https://repo.mic.gov.in/sih2024/integral-university/abhimanyu_mv_backend.git
```

2. Navigate to the project directory:
```sh
❯ cd abhimanyu_mv_backend
```

3. Install the project dependencies:


**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```

##  Getting Started

Run abhimanyu_mv_backend using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

## Learn More

To learn more about Fast-API, visit Docs.


---
