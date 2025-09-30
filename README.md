# Grade 3 Question Generator

A Python CLI tool that generates grade 3 level math and English grammar questions using LLM (Ollama/llama-stack) and stores them in SQLite.

## Features

- Generate math questions (addition, subtraction, multiplication, division, word problems)
- Generate English grammar questions (parts of speech, punctuation, plurals, verb tenses)
- Store questions in SQLite database
- Practice mode with random questions
- Works with Ollama, llama-stack, or falls back to simple templates

## Requirements

- Python 3.8+
- (Optional) Ollama or llama-stack for LLM-generated questions
- Without LLM: Uses built-in template-based question generation

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Choose Your LLM Backend (Optional)

The tool works in three modes:

#### **Option A: Ollama (Recommended - Easiest)**

Best for local development, runs on CPU, easy setup:

```bash
# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a small model (1-3GB)
ollama pull llama3.2:1b

# Start Ollama (runs in background)
ollama serve
```

Then use the tool with Ollama endpoint:
```bash
python main.py --llama-url http://localhost:11434 generate math --count 5
```

#### **Option B: llama-stack (Advanced)**

For advanced users with GPU resources:

```bash
# Install llama-stack
pip install llama_stack

# Download a model
llama model download --source meta --model-id Llama-3.2-1B-Instruct

# Build and run server (requires configuration)
llama stack build --run --template meta-reference-gpu
```

Note: Requires significant setup and GPU resources. See [llama-stack docs](https://github.com/meta-llama/llama-stack).

#### **Option C: No LLM (Fallback Mode)**

The tool includes built-in question templates and works immediately without any LLM:

```bash
# Just run it - fallback templates activate automatically
python main.py generate math --count 5
```

## Usage

### Generate Questions

Generate 5 math questions:
```bash
python main.py generate math --count 5
```

Generate 10 grammar questions:
```bash
python main.py generate grammar --count 10
```

With Ollama:
```bash
python main.py --llama-url http://localhost:11434 generate math
```

With custom LLM endpoint:
```bash
python main.py --llama-url http://localhost:8000 generate math
```

### List Questions

List all questions:
```bash
python main.py list
```

List only math questions:
```bash
python main.py list --subject math --limit 20
```

### Practice Mode

Practice with 5 random questions:
```bash
python main.py practice --count 5
```

Practice only grammar:
```bash
python main.py practice --subject grammar --count 10
```

### Quiz Mode (Interactive)

Interactive quiz that continues until you get one wrong:
```bash
python main.py quiz
```

Math-only quiz:
```bash
python main.py quiz --subject math
```

Grammar-only quiz:
```bash
python main.py quiz --subject grammar
```

**Multiple Choice Quiz:**
```bash
python main.py quiz --multiple-choice
```

Multiple choice with specific subject:
```bash
python main.py quiz --subject math --multiple-choice
```

**Quiz Features:**
- Answer correctly to get the next question automatically
- Get one wrong and the quiz ends
- Shows your streak and total questions answered
- Type `quit` to exit anytime
- Multiple choice mode: Choose from 4 options (1-4)
- Text mode: Type the answer directly

## Database

Questions are stored in `questions.db` (SQLite) with the following schema:

- `id`: Auto-incrementing primary key
- `subject`: "math" or "grammar"
- `question`: The question text
- `answer`: The correct answer
- `difficulty`: Grade level (default: 3)
- `created_at`: Timestamp

## LLM Integration

The tool supports OpenAI-compatible chat completion APIs:

- **Ollama**: Default endpoint `http://localhost:11434`
- **llama-stack**: Custom endpoint via `--llama-url`
- **Fallback**: Automatic template-based generation if LLM unavailable

The generator automatically detects if the LLM endpoint is available and falls back to templates if not.

## Example Session

```bash
# Generate some questions
$ python main.py generate math --count 3

Generating 3 math question(s)...

[Question #1]
Q: What is 15 + 8?
A: 23

[Question #2]
Q: What is 12 × 5?
A: 60

[Question #3]
Q: If you have 20 cookies and eat 7, how many are left?
A: 13

✓ Successfully generated and saved 3 question(s)!

# Practice mode
$ python main.py practice --count 2

=== Practice Mode: 2 Question(s) ===

Question 1/2 [math]
Q: What is 15 + 8?
Your answer: 23
✓ Correct!

Question 2/2 [grammar]
Q: What is the plural of 'child'?
Your answer: children
✓ Correct!

=== Results: 2/2 correct (100%) ===

# Quiz mode (interactive)
$ python main.py quiz --subject math

=== Quiz Mode ===
Answer questions correctly to continue!
Type 'quit' to exit

[MATH] Streak: 0
Q: What is 7 + 5?
Your answer: 12
✓ Correct! Keep going!

[MATH] Streak: 1
Q: What is 9 × 3?
Your answer: 27
✓ Correct! Keep going!

[MATH] Streak: 2
Q: What is 15 - 8?
Your answer: 6
✗ Incorrect. The correct answer is: 7

🎯 Quiz ended! Total answered: 3, Correct streak: 2

# Multiple choice quiz mode
$ python main.py quiz --subject math --multiple-choice

=== Multiple Choice Quiz ===
Answer questions correctly to continue!
Enter the option number (1-4)
Type 'quit' to exit

[MATH] Streak: 0
Q: Sarah has 5 pencils in her pencil case. Her friend gives her 2 more pencils. How many pencils does Sarah have now?

1. 9
2. 5
3. 7
4. 12

Your answer (1-4): 3
✓ Correct! The answer is: 7

[MATH] Streak: 1
Q: What is 12 × 5?

1. 60
2. 57
3. 65
4. 55

Your answer (1-4): 1
✓ Correct! The answer is: 60

[MATH] Streak: 2
Q: What is 20 - 8?

1. 10
2. 15
3. 12
4. 13

Your answer (1-4): 3
✓ Correct! The answer is: 12
```

## License

MIT
