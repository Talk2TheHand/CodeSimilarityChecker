# CodeSimilarityChecker

CodeSimilarityChecker is a simple Python script that detects similar or duplicate functions in Python files. It uses the `rapidfuzz` library for similarity measurement and provides results in both the terminal and an HTML report.

## Features
- Detects duplicate or highly similar functions in Python files.
- Provides similarity scores for detected duplicates.
- Generates a detailed HTML report with line numbers for easy debugging.
- Console-based interactive display using `rich`.

## Requirements
- Python 3.8+
- `rapidfuzz`
- `rich`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Talk2TheHand/CodeSimilarityChecker.git
   cd CodeSimilarityChecker
