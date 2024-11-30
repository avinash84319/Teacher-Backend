from helper.model import answer_question
import json

def generate_template(data):
    
    template={}
    template["type"]=data["type"]
    template["difficulty"]=data["difficulty"]
    template["marks"]=data["marks"]
    
    if data["type"]=="mcq":
        template["question"]=""
        template["options"]="[]"
        template["correct_answer_index"]=""

    elif data["type"]=="subjective":
        template["question"]=""
        template["answer"]=""

    elif data["type"]=="true_false":
        template["question"]=""
        template["answer"]=""

    elif data["type"]=="fill_in_the_blank":
        template["question"]=""
        template["answer"]=""

    elif data["type"]=="match_the_following":
        template["question"]=""
        template["options1"]="[]"
        template["options2"]="[]"
        template["correct_answers"]="[]"

    elif data["type"]=="one_word":
        template["question"]=""
        template["answer"]=""

    return template


def generate_questions(data,text,analytics,previous_questions):

    print("generating questions now")
    
    questions=[]
    for i,section in enumerate(data['sections']):
        questions.extend(data['sections'][i]['questions'])

    print(f'Questions from users: {questions}')

    # generate complete questions prompt
    template=""

    for question in questions:
        template+=str(generate_template(question))+","

    template='{questions:['+template[:-1]+']}'
    template=template+"the no of questions required are :"+str(len(questions))
    
    print(f'Template: {template}')

    if template=="":
        print("No questions to generate")
        return data

    #generate the questions
    generated_questions = answer_question(template,text,analytics,previous_questions)

    print(f'Generated questions: {generated_questions}')

    generated_questions=generated_questions["questions"]
    
    questions_jsons=[]

    #store the questions in the data according to the sections and required format
    done_indexes=[-1]*len(generated_questions)

    for s,section in enumerate(data['sections']):
        for i,question in enumerate(data['sections'][s]['questions']):
            for j,generated_question in enumerate(generated_questions):
                print(f'Question: {generated_question}')
                print(data['sections'][s]['questions'][i])
                if question['type']==generated_question['type'] and question['difficulty']==generated_question['difficulty'] and str(question['marks'])==str(generated_question['marks']) and done_indexes[j]==-1:
                    data['sections'][s]['questions'][i]['questionDetails']=generated_question
                    questions_jsons.append(generated_question)
                    done_indexes[j]=i
                    break
            

    return data,questions_jsons

