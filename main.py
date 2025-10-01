#!/usr/bin/env python3
"""
Grade 3 Question Generator
A simple CLI tool to generate and store math and grammar questions using llama-stack.
"""

import argparse
import sys
from database import QuestionDatabase
from generator import QuestionGenerator


def generate_questions(args):
    """Generate new questions and store in database."""
    db = QuestionDatabase(args.db)
    generator = QuestionGenerator(args.llama_url)

    subject = args.subject
    count = args.count

    print(f"Generating {count} {subject} question(s)...")

    try:
        questions = generator.generate_batch(subject, count)

        saved_count = 0
        duplicate_count = 0

        for q in questions:
            # Check if question already exists in database
            if db.question_exists(q["question"]):
                duplicate_count += 1
                print(f"\n⚠ Skipping duplicate question: {q['question'][:50]}...")
                continue

            question_id = db.add_question(
                subject=q["subject"],
                question=q["question"],
                answer=q["answer"]
            )
            saved_count += 1
            print(f"\n[Question #{question_id}]")
            print(f"Q: {q['question']}")
            print(f"A: {q['answer']}")

        print(f"\n✓ Successfully saved {saved_count} question(s)!")
        if duplicate_count > 0:
            print(f"⚠ Skipped {duplicate_count} duplicate question(s).")

    except Exception as e:
        print(f"Error generating questions: {e}", file=sys.stderr)
        sys.exit(1)


def list_questions(args):
    """List questions from the database."""
    db = QuestionDatabase(args.db)

    subject = args.subject if args.subject != "all" else None
    questions = db.get_questions(subject=subject, limit=args.limit)

    if not questions:
        print("No questions found in the database.")
        return

    print(f"\nShowing {len(questions)} question(s):\n")

    for q in questions:
        print(f"[ID: {q['id']} | Subject: {q['subject']}]")
        print(f"Q: {q['question']}")
        print(f"A: {q['answer']}")
        print(f"Created: {q['created_at']}")
        print("-" * 60)


def practice_mode(args):
    """Start practice mode with random questions."""
    db = QuestionDatabase(args.db)

    subject = args.subject if args.subject != "all" else None
    questions = db.get_random_questions(subject=subject, count=args.count)

    if not questions:
        print("No questions found in the database. Generate some first!")
        return

    print(f"\n=== Practice Mode: {args.count} Question(s) ===\n")

    correct = 0
    for i, q in enumerate(questions, 1):
        print(f"Question {i}/{len(questions)} [{q['subject']}]")
        print(f"Q: {q['question']}")

        user_answer = input("Your answer: ").strip()

        if user_answer.lower() == q['answer'].lower():
            print("✓ Correct!\n")
            correct += 1
        else:
            print(f"✗ Incorrect. The correct answer is: {q['answer']}\n")

    print(f"\n=== Results: {correct}/{len(questions)} correct ({correct*100//len(questions)}%) ===")


def _generate_multiple_choice_options(correct_answer: str, subject: str) -> list:
    """Generate 3 wrong options based on the correct answer."""
    import random

    options = [correct_answer]

    if subject == "math":
        # Try to parse the answer as a number
        try:
            correct_num = int(correct_answer)
            # Generate nearby wrong answers
            wrong_options = set()
            while len(wrong_options) < 3:
                offset = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
                wrong_num = correct_num + offset
                if wrong_num > 0 and wrong_num != correct_num:
                    wrong_options.add(str(wrong_num))
            options.extend(list(wrong_options))
        except ValueError:
            # If answer is not a simple number, generate generic wrong options
            options.extend(["Not enough information", "Cannot be determined", "None of the above"])
    else:
        # Grammar questions - generate plausible wrong answers
        grammar_wrong = [
            "adjective", "noun", "verb", "adverb", "pronoun",
            "preposition", "conjunction", "interjection",
            "mice", "childs", "mouses", "children", "goose", "geese",
            "period", "comma", "question mark", "exclamation point"
        ]
        # Filter out the correct answer and pick 3 random wrong ones
        available_wrong = [w for w in grammar_wrong if w.lower() != correct_answer.lower()]
        options.extend(random.sample(available_wrong, min(3, len(available_wrong))))

    # Shuffle so correct answer isn't always first
    random.shuffle(options)
    return options[:4]  # Ensure we have exactly 4 options


def quiz_mode(args):
    """Start interactive quiz mode - answer correctly to continue."""
    db = QuestionDatabase(args.db)
    generator = QuestionGenerator(args.llama_url)

    subject = args.subject if args.subject != "all" else None
    use_multiple_choice = getattr(args, 'multiple_choice', False)

    mode_text = "Multiple Choice Quiz" if use_multiple_choice else "Quiz Mode"
    print(f"\n=== {mode_text} ===")
    print("Answer questions correctly to continue!")
    if use_multiple_choice:
        print("Enter the option number (1-4)")
    print("Type 'quit' to exit\n")

    correct_streak = 0
    total_answered = 0

    try:
        while True:
            # Get a random question from database or generate a new one
            questions = db.get_random_questions(subject=subject, count=1)

            if not questions:
                print("No questions in database. Generating a new one...\n")
                # Generate a new question
                if subject:
                    if subject == "math":
                        q_data = generator.generate_math_question()
                    else:
                        q_data = generator.generate_grammar_question()
                else:
                    # Random subject
                    import random
                    subj = random.choice(["math", "grammar"])
                    if subj == "math":
                        q_data = generator.generate_math_question()
                    else:
                        q_data = generator.generate_grammar_question()

                # Save to database
                db.add_question(
                    subject=q_data["subject"],
                    question=q_data["question"],
                    answer=q_data["answer"]
                )
                q = q_data
            else:
                q = questions[0]

            # Display question
            print(f"[{q['subject'].upper()}] Streak: {correct_streak}")
            print(f"Q: {q['question']}\n")

            if use_multiple_choice:
                # Generate multiple choice options
                options = _generate_multiple_choice_options(q['answer'], q['subject'])
                correct_index = options.index(q['answer'])

                # Display options
                for i, option in enumerate(options, 1):
                    print(f"{i}. {option}")

                user_input = input("\nYour answer (1-4): ").strip()

                # Check for quit
                if user_input.lower() == 'quit':
                    print(f"\n🎯 Quiz ended! Total answered: {total_answered}, Correct streak: {correct_streak}")
                    break

                total_answered += 1

                # Check answer
                try:
                    user_choice = int(user_input) - 1
                    if 0 <= user_choice < len(options) and user_choice == correct_index:
                        correct_streak += 1
                        print(f"✓ Correct! The answer is: {q['answer']}\n")
                    else:
                        if 0 <= user_choice < len(options):
                            print(f"✗ Incorrect. You chose: {options[user_choice]}")
                        else:
                            print(f"✗ Invalid option.")
                        print(f"The correct answer is: {q['answer']}")
                        print(f"\n🎯 Quiz ended! Total answered: {total_answered}, Correct streak: {correct_streak}")
                        break
                except (ValueError, IndexError):
                    print(f"✗ Invalid input.")
                    print(f"The correct answer is: {q['answer']}")
                    print(f"\n🎯 Quiz ended! Total answered: {total_answered}, Correct streak: {correct_streak}")
                    break

            else:
                # Original text-based answer mode
                user_answer = input("Your answer: ").strip()

                # Check for quit
                if user_answer.lower() == 'quit':
                    print(f"\n🎯 Quiz ended! Total answered: {total_answered}, Correct streak: {correct_streak}")
                    break

                total_answered += 1

                # Check answer
                if user_answer.lower() == q['answer'].lower():
                    correct_streak += 1
                    print(f"✓ Correct! Keep going!\n")
                else:
                    print(f"✗ Incorrect. The correct answer is: {q['answer']}")
                    print(f"\n🎯 Quiz ended! Total answered: {total_answered}, Correct streak: {correct_streak}")
                    break

    except KeyboardInterrupt:
        print(f"\n\n🎯 Quiz interrupted! Total answered: {total_answered}, Correct streak: {correct_streak}")


def main():
    parser = argparse.ArgumentParser(
        description="Grade 3 Question Generator using LLM (Ollama/llama-stack)"
    )

    parser.add_argument(
        "--db",
        default="questions.db",
        help="Database file path (default: questions.db)"
    )

    parser.add_argument(
        "--llama-url",
        default="http://localhost:11434",
        help="LLM server URL (default: http://localhost:11434 for Ollama)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate new questions")
    gen_parser.add_argument(
        "subject",
        choices=["math", "grammar"],
        help="Question subject"
    )
    gen_parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of questions to generate (default: 5)"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List stored questions")
    list_parser.add_argument(
        "--subject",
        choices=["all", "math", "grammar"],
        default="all",
        help="Filter by subject (default: all)"
    )
    list_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of questions to show (default: 10)"
    )

    # Practice command
    practice_parser = subparsers.add_parser("practice", help="Practice with random questions")
    practice_parser.add_argument(
        "--subject",
        choices=["all", "math", "grammar"],
        default="all",
        help="Filter by subject (default: all)"
    )
    practice_parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of questions to practice (default: 5)"
    )

    # Quiz command
    quiz_parser = subparsers.add_parser("quiz", help="Interactive quiz mode - answer correctly to continue!")
    quiz_parser.add_argument(
        "--subject",
        choices=["all", "math", "grammar"],
        default="all",
        help="Filter by subject (default: all)"
    )
    quiz_parser.add_argument(
        "--multiple-choice",
        action="store_true",
        help="Use multiple choice format (4 options)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "generate":
        generate_questions(args)
    elif args.command == "list":
        list_questions(args)
    elif args.command == "practice":
        practice_mode(args)
    elif args.command == "quiz":
        quiz_mode(args)


if __name__ == "__main__":
    main()
