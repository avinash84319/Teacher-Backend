from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import os
# from langchain_google_genai import ChatGoogleGenerativeAI

LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="pr-downright-finer-90"

def make_chain_image():

    # model2 = ChatGoogleGenerativeAI(
    # model="gemini-1.5-pro",
    # temperature=0,
    # max_tokens=None,
    # timeout=None,
    # max_retries=2,
    # # other params...
    # )
    
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
            "Questions json :- {questions}"

            "GENERATE THIS QUESTIONS ACCORDING TO THE TEXT PROVIDED :- {text}"
            "MAKE SURE YOU DONT REPEAT THE QUESTIONS"
            "MAKE SURE YOU PERSONALIZE THE QUESTIONS ACCORDING TO THE STUDENTS PREVIOUS ASSESMENT DETAILS"
            "GIVE IN JSON FORMAT ONLY DONT GIVE ANY EXTRA INFORMATION"
    )

    model = ChatOllama(model="llama3.1",format="json")

    chain =  final_prompt | model | JsonOutputParser()

    # chain2 = final_prompt | model2 | JsonOutputParser()

    return chain

def answer_question(question_json,text,student_info,previous_questions):
    chain= make_chain_image()
    
    ans =""
    ans = chain.invoke({"student_info":student_info,"questions":question_json,"text":text,"previous_questions":previous_questions})
    
    return ans

def check_model():

    model = ChatOllama(model="llama3.1",format="json")
    
    try:
        model.invoke("hello")
        return True
    except Exception as e:
        return e