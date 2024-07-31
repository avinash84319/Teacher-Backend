from model import answer_question
from templates import template_question_dictionary,template_difficulty_dictionary,template_marks_dictionary
import json


def generate_template(exp_json):
    no_of_questions=exp_json["no_of_questions"]
    question_type=exp_json["question_type"]
    difficulty=exp_json["difficulty"]
    marks=exp_json["marks"]
    template=template_question_dictionary[question_type]
    difficulty=template_difficulty_dictionary[difficulty]
    marks=template_marks_dictionary[marks]
    return template.format(no_of_questions=no_of_questions,difficulty=difficulty,marks=marks)


def generate_questions(data):

    print("generating questions now")
    text = data['text']
    
    questions=[]
    for i,section in enumerate(data['sections']):
        questions.extend(data['sections'][i]['questions'])

    print(f'Questions from users: {questions}')

    # generate complete questions prompt
    template=""

    #generate the jsons for the questions
    for i,question_type in enumerate(['mcq','subjective','true_false','fill_in_the_blank','match_the_following','one_word']):
        for j,difficulty in enumerate(['easy','medium','hard']):
            for k,marks in enumerate([1,2,5]):
                count = 0
                for question in questions:
                    print(f'Question: {question}')
                    print(question['type']==question_type,question['difficulty']==difficulty,question['marks']==marks)
                    if question['type']==question_type and question['difficulty']==difficulty and question['marks']==marks:
                        count+=1
                if count>0:
                    template+=generate_template({"no_of_questions":count,"question_type":question_type,"difficulty":difficulty,"marks":marks})
    
    print(f'Template: {template}')

    if template=="":
        print("No questions to generate")
        return data

    #generate the questions
    generated_questions = answer_question(template,text)

    print(f'Generated questions: {generated_questions}')

    generated_questions=generated_questions["questions"]
    

    #store the questions in the data according to the sections and required format
    done_indexes=[-1]*len(generated_questions)

    for s,section in enumerate(data['sections']):
        for i,question in enumerate(data['sections'][s]['questions']):
            for j,generated_question in enumerate(generated_questions):
                print(f'Question: {generated_question}')
                print(data['sections'][s]['questions'][i])
                if question['type']==generated_question['type'] and question['difficulty']==generated_question['difficulty'] and str(question['marks'])==str(generated_question['marks']) and done_indexes[j]==-1:
                    data['sections'][s]['questions'][i]['questionDetails']=generated_question
                    done_indexes[j]=i
                    break
            

    return data

