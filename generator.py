import requests
import json
from typing import Dict, List


class QuestionGenerator:
    """Generate grade 3 questions using LLM (Ollama/llama-stack)."""

    def __init__(self, llama_stack_url: str = "http://localhost:11434"):
        self.llama_stack_url = llama_stack_url
        self.is_ollama = "11434" in llama_stack_url  # Detect Ollama by default port

    def generate_math_question(self) -> Dict[str, str]:
        """Generate a grade 3 math question."""
        import random

        # Add variety by suggesting different topics
        topics = [
            "addition or subtraction",
            "multiplication (up to 10x10) or simple division",
            "word problems about money or shopping",
            "word problems about time or daily activities",
            "word problems about counting objects or sharing items"
        ]
        selected_topic = random.choice(topics)

        prompt = f"""Generate ONE unique grade 3 math question about {selected_topic}. Include both the question and answer.
Format your response EXACTLY as:
QUESTION: [the question]
ANSWER: [the answer]

Make the question creative and different each time. Use different numbers, contexts, and scenarios.
Keep it appropriate for 8-9 year olds."""

        response = self._call_llama(prompt)
        return self._parse_response(response, "math")

    def generate_grammar_question(self) -> Dict[str, str]:
        """Generate a grade 3 English grammar question."""
        import random

        # Add variety by suggesting different topics
        topics = [
            "identifying parts of speech (nouns, verbs, adjectives, or adverbs)",
            "punctuation and capitalization",
            "plurals and irregular plurals",
            "verb tenses (past, present, future)",
            "sentence structure and simple/compound sentences"
        ]
        selected_topic = random.choice(topics)

        prompt = f"""Generate ONE unique grade 3 English grammar question about {selected_topic}. Include both the question and answer.
Format your response EXACTLY as:
QUESTION: [the question]
ANSWER: [the answer]

Make the question creative and different each time. Use different words, examples, and scenarios.
Keep it appropriate for 8-9 year olds."""

        response = self._call_llama(prompt)
        return self._parse_response(response, "grammar")

    def generate_batch(self, subject: str, count: int = 5) -> List[Dict[str, str]]:
        """Generate multiple questions at once, avoiding duplicates."""
        questions = []
        seen_questions = set()
        max_attempts = count * 3  # Allow up to 3x attempts to get unique questions
        attempts = 0

        while len(questions) < count and attempts < max_attempts:
            attempts += 1

            if subject == "math":
                q = self.generate_math_question()
            elif subject == "grammar":
                q = self.generate_grammar_question()
            else:
                continue

            # Check if question is unique (case-insensitive)
            question_key = q["question"].lower().strip()
            if question_key not in seen_questions:
                seen_questions.add(question_key)
                questions.append(q)

        return questions

    def _call_llama(self, prompt: str) -> str:
        """Call LLM API (Ollama/llama-stack) to generate content."""
        try:
            # Choose model based on backend
            model = "llama3.2:1b" if self.is_ollama else "llama3.2"

            # OpenAI-compatible chat completion API
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful elementary school teacher creating educational questions for grade 3 students."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.9,
                "max_tokens": 200,
                "stream": False
            }

            # Ollama uses /api/chat, llama-stack uses /v1/chat/completions
            endpoint = f"{self.llama_stack_url}/api/chat" if self.is_ollama else f"{self.llama_stack_url}/v1/chat/completions"

            response = requests.post(
                endpoint,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                # Ollama response format
                if self.is_ollama and "message" in result:
                    return result["message"]["content"]
                # OpenAI/llama-stack format
                elif "choices" in result:
                    return result["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"Unexpected response format: {result}")
            else:
                raise Exception(f"LLM API error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            # Fallback to simple generation if LLM is not available
            print("⚠ LLM endpoint not available, using fallback templates...")
            return self._fallback_generation(prompt)
        except Exception as e:
            print(f"⚠ Error calling LLM: {e}")
            print("Using fallback templates...")
            return self._fallback_generation(prompt)

    def _fallback_generation(self, prompt: str) -> str:
        """Fallback question generation when LLM is unavailable."""
        import random

        if "math" in prompt.lower():
            # Simple math question templates
            templates = [
                ("What is {a} + {b}?", lambda a, b: a + b),
                ("What is {a} - {b}?", lambda a, b: a - b),
                ("What is {a} × {b}?", lambda a, b: a * b),
                ("If you have {a} apples and get {b} more, how many apples do you have?", lambda a, b: a + b),
            ]
            template, calc = random.choice(templates)
            a, b = random.randint(1, 20), random.randint(1, 20)
            if "subtract" in template or "-" in template:
                a, b = max(a, b), min(a, b)  # Ensure no negative answers
            question = template.format(a=a, b=b)
            answer = str(calc(a, b))
            return f"QUESTION: {question}\nANSWER: {answer}"

        else:
            # Simple grammar question templates
            templates = [
                ("What is the plural of 'child'?", "children"),
                ("What is the plural of 'mouse'?", "mice"),
                ("Is 'run' a noun or a verb?", "verb"),
                ("Is 'happy' a noun or an adjective?", "adjective"),
                ("Which word is a noun: 'quickly', 'table', 'run'?", "table"),
            ]
            question, answer = random.choice(templates)
            return f"QUESTION: {question}\nANSWER: {answer}"

    def _parse_response(self, response: str, subject: str) -> Dict[str, str]:
        """Parse the LLM response into question and answer."""
        lines = response.strip().split('\n')
        question = ""
        answer = ""

        # First pass: look for QUESTION: and ANSWER: labels
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("QUESTION:"):
                question = line_stripped.replace("QUESTION:", "").strip()
            elif line_stripped.startswith("ANSWER:"):
                answer = line_stripped.replace("ANSWER:", "").strip()

        # Second pass: if still missing, try to extract from multiline format
        if not question or not answer:
            full_text = response.strip()

            # Try splitting by "ANSWER:" keyword
            if "ANSWER:" in full_text:
                parts = full_text.split("ANSWER:", 1)
                question_part = parts[0].replace("QUESTION:", "").strip()
                answer_part = parts[1].strip()

                if question_part and answer_part:
                    question = question_part
                    answer = answer_part

            # If still not found, try simple line-based extraction
            elif not question or not answer:
                non_empty_lines = [line.strip() for line in lines if line.strip()]
                if len(non_empty_lines) >= 2:
                    # First non-empty line is question, last is answer
                    question = non_empty_lines[0].replace("QUESTION:", "").strip()
                    answer = non_empty_lines[-1].replace("ANSWER:", "").strip()
                elif len(non_empty_lines) == 1:
                    # Only one line - treat as question with unknown answer
                    question = non_empty_lines[0].replace("QUESTION:", "").strip()
                    answer = "N/A"

        # Clean up any remaining labels
        question = question.replace("QUESTION:", "").strip()
        answer = answer.replace("ANSWER:", "").strip()

        return {
            "subject": subject,
            "question": question if question else "N/A",
            "answer": answer if answer else "N/A"
        }
