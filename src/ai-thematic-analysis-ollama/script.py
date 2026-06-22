import json
from docx import Document
from openai import OpenAI
import os

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_file_name = "transcript_fictive"
input_file_path = os.path.join(BASE_DIR, "input", f"{input_file_name}.docx")
output_file_path = os.path.join(BASE_DIR, "output", "analysis_results.csv")

paragraphs = [p.text for p in Document(input_file_path).paragraphs]
transcript = "\n".join(paragraphs)

# Define your chunk size (e.g., 50,000 characters is safely within a 32k context window)
# Will depend on the available VRAM
CHUNK_SIZE = 5000

# Minimal line to split text into chunks
chunks = [transcript[i : i + CHUNK_SIZE] for i in range(0, len(transcript), CHUNK_SIZE)]

with open(output_file_path, "w", encoding="utf-8") as f:
    f.write("document, verbatim, theme, sentiment" + "\n")

research_question = "Uses, needs and acceptability of AI in legal advisory services."

# Then loop through your chunks to call the API
for i, chunk in enumerate(chunks):
    # Your client.chat.completions.create() code goes here...
    print(f"Processing chunk {i + 1}/{len(chunks)}")

    response = client.chat.completions.create(
        model="qwen2.5:7b",  # <-- Make sure you ran 'ollama run qwen2.5:7b'
        messages=[
            {
                "role": "system",
                "content": 
                    f"""
                    You are an expert researcher in inductive thematic analysis. 
                    Analyze the given transcript and extract all meaningful verbatims that answers this research question: "{research_question}"

                    For each extraction, induce the theme and classify the sentiment naturally from the text.

                    ### Output Constraints
                    - Output raw lines immediately. No markdown formatting (no ```), no headers, one line per verbatim.
                    - Format: "{input_file_name}","verbatim","theme","sentiment"
                    - Use comma delimiters. Wrap every value in double quotes. Convert internal double quotes to single quotes.
                    - Keep verbatims short but self-contained (understandable without context). Rely strictly on facts; do not extrapolate.

                    ### Reference Examples
                    "{input_file_name}","It takes me four clicks just to export a simple PDF report.","Export friction","Negative"
                    "{input_file_name}","I check the dashboard every single morning before I even open my email.","Daily workflow routine","Neutral"
                    "{input_file_name}","The auto-save feature saved my life when my browser crashed yesterday.","Data protection safety","Positive"
                    """,
            },
            {
                "role": "user",
                "content": chunk,
            },
        ],
        temperature=0.0,
        top_p=0.1,
        # REMOVED: "format": "json" from extra_body so Ollama allows raw text
        extra_body={"options": {"num_ctx": 32000}}, # num_ctx forces higher context window, but final window depends on available VRAM
        stream=False,
    )

    # Get the raw CSV line from the model
    result_csv_line = response.choices[0].message.content.strip()

    with open(output_file_path, "a", encoding="utf-8") as f:
        # Add a newline character at the end so the next run starts on a fresh row
        f.write(result_csv_line + "\n")

print(f"Analysis completed and appended to {output_file_path}.")
