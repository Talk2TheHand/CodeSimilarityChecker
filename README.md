# CodeSimilarityChecker

A simple script for testing and reviewing AI-generated or manually written code for similarities. While primarily created for experimentation, it works for general use as well.

This is not a fancy tool—it's far from optimized—but it’s good enough for spotting duplicate or similar code structures that might need improvement. Feel free to try it out, and if you have ideas, contributions, or fixes, go ahead and update it further!

## Known Issues / Missing Features

While the script is useful, there are a few limitations and areas where it could be improved:

1. **False Positive Duplications in Reports**  
   The HTML report can sometimes show duplications for a single function, mistaking it for different code. These cases usually show a 100% similarity or close to it, so with manual review, they’re easy to notice and dismiss.

2. **Multiplier Quirk**  
   The script applies a multiplier to adjust the similarity percentage, but it occasionally pushes the percentage over 100%. This could be refined, but for quick use, it works well enough.

3. **No In-depth Optimizations**  
   The script isn’t optimized for speed or accuracy with very large projects. The best way to use it is with targeted files or folders, though you could scan an entire codebase if needed.

## It's Useful For:

- Getting a quick snapshot of similar code structures in your project.
- Identifying parts of the code that might need refactoring or improvement.
- Finding duplicate or overly similar functions to consolidate or optimize.
- Highlighting potential areas to hand off to AI tools or tackle yourself.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Talk2TheHand/CodeSimilarityChecker.git
   cd CodeSimilarityChecker
Install the required Python packages:
bash
Copy code
pip install -r requirements.txt
Usage
Ensure your Python version is 3.x or above.
Place the script in a folder containing the Python files you want to analyze.
Run the script:
bash
Copy code
python detect_duplicates.py
Review the results:
Check the terminal for a summary of duplicates.
Open the generated HTML report for a detailed view, including line numbers and similarity percentages.
Contributions
If you’ve got an idea to improve the script, feel free to fork the repo and submit a pull request.