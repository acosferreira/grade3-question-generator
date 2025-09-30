# Grade 3 Question Generator - Features

## Overview
A Python CLI application for generating and practicing grade 3 level educational questions with multiple quiz modes.

## Key Features

### 1. Question Generation
- **Math Questions**: Addition, subtraction, multiplication, division, word problems
- **Grammar Questions**: Parts of speech, plurals, verb tenses, punctuation
- **LLM-Powered**: Uses Ollama or llama-stack for intelligent question generation
- **Fallback Mode**: Works without LLM using built-in templates

### 2. Storage
- SQLite database for persistent question storage
- Track all generated questions with timestamps
- Filter and search by subject

### 3. Quiz Modes

#### Practice Mode
- Fixed number of questions (configurable)
- See all questions even if you get them wrong
- Final score and percentage at the end

#### Interactive Quiz Mode
- Continue as long as you answer correctly
- One wrong answer ends the quiz
- Track your streak

#### Multiple Choice Quiz Mode ✨ NEW
- Same as quiz mode but with 4 options
- Automatically generates plausible wrong answers
- Choose answer by number (1-4)
- Smart wrong answer generation:
  - **Math**: Numbers close to correct answer
  - **Grammar**: Related grammar terms

### 4. Customization
- Filter by subject (math/grammar/all)
- Adjustable question count
- Custom LLM endpoint support
- Multiple choice or text input

## Command Reference

```bash
# Generate questions
python main.py generate math --count 5
python main.py generate grammar --count 10

# List stored questions
python main.py list
python main.py list --subject math --limit 20

# Practice mode (fixed questions)
python main.py practice --count 5
python main.py practice --subject grammar --count 10

# Quiz mode (continuous until wrong)
python main.py quiz
python main.py quiz --subject math

# Multiple choice quiz
python main.py quiz --multiple-choice
python main.py quiz --subject math --multiple-choice
```

## Technical Features

- Python 3.8+ compatible
- SQLite for zero-config database
- OpenAI-compatible API integration
- Graceful fallback when LLM unavailable
- Keyboard interrupt handling
- Input validation
- Cross-platform (Linux, macOS, Windows)

## Educational Benefits

- **Self-Paced Learning**: Students progress at their own speed
- **Immediate Feedback**: Instant validation of answers
- **Streak Tracking**: Motivates students to keep improving
- **Multiple Formats**: Text and multiple choice support different learning styles
- **Unlimited Practice**: Generate new questions anytime
- **No Internet Required**: Works offline with fallback mode
