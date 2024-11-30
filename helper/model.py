from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import os

#langsmith trace
from langsmith.run_helpers import traceable
from langchain_google_vertexai import ChatVertexAI

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"]="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"
os.environ["LANGCHAIN_PROJECT"]="pr-roasted-imagination-39"

def make_chain_image():

    model2 = ChatVertexAI(
    model="gemini-1.5-flash-001",
    temperature=0,
    max_tokens=None,
    max_retries=6,
    stop=None,
    # other params...
    )
    
    final_prompt = ChatPromptTemplate.from_template(
            "You are expert Teacher and Question generator"
            "User will give you a json structer with questions with difficulty level,marks and type of question"
            "You have to generate questions based on the given json structure"
            "Generate the questions and return the json structure with the questions and filling all the fields properly"

            "User will also provide you with the student information json which will contain the students previos assesment details"
            "make sure while generating the questions you take care of the students previous assesment details and generate the questions accordingly"
            "You have to generate the questions according to the analysis of the students previous assesment details"
            "Personalize the questions according to the students previous assesment details"

            "For the same question paper but in previous section the questions you already generated are :- {previous_questions}"
            "So for the next section you have to generate new questions, make sure you dont repeat the questions"

            "Student previous information :- {student_info}"

            "GENERATE THIS QUESTIONS ACCORDING TO THE TEXT PROVIDED :- {text}"

            "USER has selected some topics to get questions from :- {topics}"
            "Equally priortize all topics user provided"

            "Extra instructions from users :- {instruction}"

            "If there is conflict between topics and instruction follow instructions"

            "Questions json :- {questions}"

            "MAKE SURE YOU DONT REPEAT THE QUESTIONS"
            "MAKE SURE YOU PERSONALIZE THE QUESTIONS ACCORDING TO THE STUDENTS PREVIOUS ASSESMENT DETAILS"
            "GIVE IN JSON FORMAT ONLY DONT GIVE ANY EXTRA INFORMATION"
    )

    model = ChatOllama(model="llama3.1",format="json")

    chain =  final_prompt | model | JsonOutputParser()

    chain2 = final_prompt | model2 | JsonOutputParser()

    return chain,chain2

@traceable(run_type="llm")
def answer_question(question_json,text,student_info,previous_questions,instruction,topics):
    chain,chain2= make_chain_image()
    
    ans =""
    # ans = chain.invoke({"student_info":student_info,"questions":question_json,"text":text,"previous_questions":previous_questions})

    ans = chain2.invoke({"student_info":student_info,"questions":question_json,"text":text,"previous_questions":previous_questions,"instruction":instruction,"topics":topics})
    
    return ans

def check_model():

    model = ChatOllama(model="llama3.1",format="json")
    
    try:
        model.invoke("hello")
        return True
    except Exception as e:
        return e

def give_headings(text):

    try:

        model = ChatVertexAI(
        model="gemini-1.5-flash-001",
        temperature=0,
        max_tokens=None,
        max_retries=6,
        stop=None,
        # other params...
        )
        
        final_prompt = ChatPromptTemplate.from_template(
            "Given this text :- {text}"
            "Give the outline or all topics in the text"
            "give in json format with array of topics"
            "Format give only single array of topics"
            "give Topics which are sutiables for question generation"
        )

        chain =  final_prompt | model | JsonOutputParser()

        res = chain.invoke({"text":text})

        return res

    except Exception as e:

        print("while generating topics error :- " + str(e))

        return False

    