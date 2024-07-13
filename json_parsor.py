from templates import template_question_dictionary,template_difficulty_dictionary,template_marks_dictionary

exp_json={
    "no_of_questions": 10,
    "question_type": "mcqs",
    "difficulty": "easy",
    "marks": "1"
}

def generate_template(text,exp_json):
    no_of_questions=exp_json["no_of_questions"]
    question_type=exp_json["question_type"]
    difficulty=exp_json["difficulty"]
    marks=exp_json["marks"]
    template=template_question_dictionary[question_type]
    difficulty=template_difficulty_dictionary[difficulty]
    marks=template_marks_dictionary[marks]
    return template.format(text=text,no_of_questions=no_of_questions,difficulty=difficulty,marks=marks)