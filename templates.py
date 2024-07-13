#original template which works perfectly fine
# template = """
    # Create some questions with there options and correct answers based on this text:
    # {text}
    # please give the output in json format and keep all questions in a list.
    # """


template_question_dictionary={
    "mcqs": "Create {no_of_questions} questions with four options and correct answers based on this text:{text} and {difficulty} and also {marks} please give the output in json format and keep all questions in a list.",
    "subjective": "Create a {no_of_questions} subjective question with the correct answers based on this text:{text} and {difficulty} and also {marks} please give the output in json format and keep all questions in a list.",
    "true_false": "Create {no_of_questions} true/false questions, also give the correct answer in only true or false based on this text:{text} and {difficulty} and also {marks} please give the output in json format and keep all questions in a list.",
    "fill_in_the_blank": "Create {no_of_questions} fill in the blank questions with the correct answers based on this text:{text} and {difficulty} and also {marks} please give the output in json format and keep all questions in a list.",
    "match_the_following": "Create {no_of_questions} match the following questions with the correct answers based on this text:{text} and {difficulty} and also {marks} please give the output in json format and keep all questions in a list.",
    "one_word": "Create {no_of_questions} one-word questions with the correct answers based on this text:{text} and {difficulty} and also {marks} please give the output in json format and keep all questions in a list.",
}

template_difficulty_dictionary={
    "easy":"keep the questions easy",
    "medium":"keep the questions medium",
    "hard":"keep the questions hard",
}

template_marks_dictionary={
    "1":"keep the length of the answers for 1 marks",
    "2":"keep the length of the answers for 2 marks",
    "5":"keep the length of the answers for 5 marks"
}

