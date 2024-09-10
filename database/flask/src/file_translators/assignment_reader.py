import json
import argparse


def assignment_JSON(file_path):
    """Utility function to parse a JSON file containing questions data

    Args:
        file_path (JSON): JSON file containing questions data

    Returns:
        List: List of questions, each question is a dictionary with the following fields:
            - questions_name: name of the question
            - visibility: visibility of the question
            - status: status of the question
            - output: details of the output of the question
            - max_score: maximum score of the question
    """

    # Extracting questions to a list of dictionaries, including parsing the 'output' field
    with open(file_path, "r") as file:
        full_data = json.load(file)

        # Extracting questions to a list of dictionaries, including parsing the 'output' field
        extracted_questions = []

        for number, questions in enumerate(full_data["tests"]):
            visibility_value = questions.get("visibility", "")
            is_visible = True if visibility_value == "visible" else False

            questions_dict = {
                "question_id": number + 1,
                "questions_name": questions.get("name", ""),
                "visibility": is_visible,
                "status": questions.get("status", ""),
                "output": questions.get("output", ""),
                "max_score": questions.get("max_score", "0"),
                "score": questions.get("score", "0"),
            }

            extracted_questions.append(questions_dict)

    return extracted_questions


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process a JSON file containing questions data."
    )
    parser.add_argument(
        "file_path", type=str, help="Path to the JSON file to be processed"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    json_extracted = assignment_JSON(args.file_path)
    print(sum(float(d.get("score", 0)) for d in json_extracted))
