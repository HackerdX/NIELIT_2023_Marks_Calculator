import fitz
import re


def calculate_score(answers):
    score = 0
    correct = 0
    incorrect = 0
    not_attempted = 0
    for answer in answers:
        given = answer["Given"]

        if given == "Not Attempted":
            # "Not Attempted" question, skip
            not_attempted += 1
            pass
        elif isinstance(given, int) and given == int(answer["Correct"]):
            score += 1
            correct += 1
        elif isinstance(given, int) and given != int(answer["Correct"]):
            score -= 0.25
            incorrect += 1
            print(f"Question ID: {answer['Current_Question']}, Given: {answer['Given']}, Correct: {answer['Correct']}")
    print(f"Correct: {correct}, NotCorrect: {incorrect}, NotAttempted: {not_attempted}");
    return max(0, score)


def parse_pdf(file_path):
    doc = fitz.open(file_path)
    answers = []

    # Read the entire document by accumulating text from all pages
    full_text = ""
    for page_number in range(doc.page_count):
        page = doc[page_number]
        full_text += page.get_text("text")

    # Find "Question ID" and "Answer Given by Candidate" together
    matches = re.finditer(
        r'(?:Question ID|Section):-\s*(\d+).*?Answer Given by Candidate:-\s*(?:\s*,\s*Option ID\s*:\s*-\s*(\d+)|\s*Not Attempted)?',
        full_text, re.DOTALL)

    for match in matches:
        current_question = match.group(1)
        given_answer_part = match.group(0)  # The part containing "Answer Given by Candidate"

        # Search for "Options ID" within the "Answer Given by Candidate" part
        options_match = re.search(
            r'Answer Given by Candidate:-\s*(?:\s*,\s*Option ID\s*:\s*-\s*(\d+))',
            given_answer_part, re.DOTALL
        )

        if options_match:
            given_number = int(options_match.group(1))
        else:
            given_number = "Not Attempted"

        # Search for "Correct Answer" within the remaining text
        correct_answer_match = re.search(
            r'Correct Answer\s*:-\s*Option\s*ID\s*:-\s*(\d+)',
            full_text[match.end():], re.MULTILINE | re.DOTALL
        )

        if correct_answer_match:
            correct_answer = correct_answer_match.group(1)
        else:
            correct_answer = None

        answers.append({"Current_Question": current_question, "Given": given_number, "Correct": correct_answer})

    total_score = calculate_score(answers)
    print(f"Total Score: {total_score}")
    print(f"Total Count: {len(answers)}")


if __name__ == "__main__":
    pdf_file_path = r"/Users/hackerx/Desktop/Upcoming Exams 2023-2024/NIELIT_ASNWER_KEY/Response_Sheet_SB_Engineer.pdf"
    parse_pdf(pdf_file_path)
