import re
from rapidfuzz import fuzz
import os
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()


def preprocess_code(content):
    """
    Preprocess code to normalize formatting and remove irrelevant details for comparison.
    """
    content = content.strip()
    content = re.sub(r"\b(GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD)\b", "HTTP_METHOD", content)  # Normalize HTTP methods
    content = re.sub(r'assert .*?, ".*?"', 'assert', content)  # Normalize assert messages
    content = re.sub(r"[ \t]+", " ", content)  # Normalize spaces/tabs
    content = re.sub(r"\n\s*\n", "\n", content)  # Remove multiple blank lines
    return content


def tokenize_code(content):
    """
    Tokenize the code into keywords and meaningful tokens for comparison.
    """
    # Remove comments and docstrings
    content = re.sub(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|#.*', '', content)
    # Extract meaningful tokens
    return " ".join(re.findall(r"[a-zA-Z_]\w*|==|!=|<=|>=|<|>|=|\+|-|\*|/|%|\(|\)|\[|\]|\{|\}", content))


def extract_functions(content):
    """
    Extracts functions or methods from the code content using regex.
    """
    function_pattern = re.compile(r"^\s*def\s+\w+\(.*?\):.*?(?=^\s*def\s+\w+\(|\Z)", re.DOTALL | re.MULTILINE)
    return function_pattern.findall(content)


def get_line_number(function_snippet, file_path):
    """
    Find the starting line number of a function snippet in the given file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    for i, line in enumerate(lines):
        if function_snippet.strip().splitlines()[0] in line:
            return i + 1  # Line numbers are 1-based
    return "Unknown"


def find_duplicates_within_file(file_path, functions, similarity_threshold=0.8):
    """
    Finds duplicates within a single file by comparing all functions to each other.
    """
    duplicates = []
    for i, func1 in enumerate(functions):
        for j, func2 in enumerate(functions):
            if i >= j:  # Avoid self-comparisons and duplicate comparisons
                continue

            # Tokenize and calculate similarity
            tokenized_func1 = tokenize_code(func1)
            tokenized_func2 = tokenize_code(func2)
            similarity = fuzz.ratio(tokenized_func1, tokenized_func2) / 100.0

            # Apply length penalty for short functions
            length_penalty = min(len(func1.splitlines()), len(func2.splitlines())) / 10
            similarity *= 1 + (length_penalty * 0.1)  # Adjust penalty weight as needed

            if similarity >= similarity_threshold:
                duplicates.append((func1, func2, similarity, file_path))
    return duplicates


def display_duplicates(duplicates):
    """
    Displays duplicate functions and their similarity scores in the terminal.
    """
    if duplicates:
        console.rule("Duplicates Found")
        for func1, func2, similarity, file_path in duplicates:
            table = Table(title=f"File: {file_path}", title_style="bold cyan")
            table.add_column("Function 1", style="dim")
            table.add_column("Function 2", style="dim")
            table.add_column("Similarity", justify="center", style="bold green")
            table.add_row(func1.strip(), func2.strip(), f"{similarity * 100:.2f}%")
            console.print(table)
        console.print(f"[bold green]Total duplicate clusters detected:[/] {len(duplicates)}")
    else:
        console.print("[bold green]No duplicates found.[/]")


def save_html_report(duplicates, output_file):
    """
    Save a detailed HTML report for detected duplicates.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("""
        <html>
        <head>
            <title>Duplicate Code Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2 { color: #333; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; }
                th { background-color: #f4f4f4; }
                .similarity { color: green; font-weight: bold; }
                pre { background: #f8f8f8; padding: 10px; border-radius: 5px; overflow: auto; }
            </style>
        </head>
        <body>
        <h1>Duplicate Code Report</h1>
        """)
        for func1, func2, similarity, file_path in duplicates:
            line_num1 = get_line_number(func1, file_path)
            line_num2 = get_line_number(func2, file_path)
            f.write(f"<h2>File: {file_path}</h2>")
            f.write("<table><tr><th>Function 1</th><th>Function 2</th><th>Similarity</th></tr>")
            f.write(f"<tr><td><pre>Line {line_num1}:\n{func1}</pre></td>")
            f.write(f"<td><pre>Line {line_num2}:\n{func2}</pre></td>")
            f.write(f"<td class='similarity'>{similarity * 100:.2f}%</td></tr>")
            f.write("</table>")
        f.write("</body></html>")


def main():
    directory = r"Z:\Jarvis\AI Recipe\backend\tests\unit\routes"
    extensions = [".py"]
    similarity_threshold = 0.75  # Adjusted threshold for more sensitivity

    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(tuple(extensions))]
    console.log(f"Scanning {len(files)} files for duplicates...")

    total_duplicates = 0
    duplicate_clusters = []
    report_file_path = f"reports/duplicate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        preprocessed_content = preprocess_code(content)
        functions = extract_functions(preprocessed_content)
        duplicates = find_duplicates_within_file(file_path, functions, similarity_threshold)
        total_duplicates += len(duplicates)
        duplicate_clusters.extend(duplicates)

        if duplicates:
            display_duplicates(duplicates)

    save_html_report(duplicate_clusters, report_file_path)

    console.rule("Scan Complete!")
    console.print(f"Total files scanned: {len(files)}")
    if total_duplicates > 0:
        console.print(f"Total duplicate clusters detected: {len(duplicate_clusters)}")
        console.print(f"[bold cyan]HTML report saved to:[/] {report_file_path}")
    else:
        console.print("[bold green]No duplicates found.[/]")


if __name__ == "__main__":
    main()
