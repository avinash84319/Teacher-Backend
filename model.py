from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser


"""
example json format for mcq:
        question: "What is the capital of France?",
        options: ["Paris", "London", "Berlin", "Madrid"],
        correct_answer: 0  # index of the correct answer
        type: "mcq",
        difficulty: "easy",
        marks: 1

    example json format for subjective:
        question: "What is the capital of France?",
        answer: "Paris",
        type: "subjective",
        difficulty: "easy",
        marks: 1

    example json format for true_false:
        question: "Paris is the capital of France",
        answer: "True",
        type: "true_false",
        difficulty: "easy",
        marks: 1
    
    example json format for fill_in_the_blank:
        question: "The capital of France is ___",
        answer: "Paris",
        type: "fill_in_the_blank",
        difficulty: "easy",
        marks: 1

    example json format for match_the_following:
        question: "Match the following",
        options1: ["Paris", "London", "Berlin", "Madrid"],
        options2: ["Spain","France","Germany","England"],
        correct_answer: [1,3,2,0]  # index of the correct answer
        type: "match_the_following",
        difficulty: "easy",
        marks: 1

    example json format for one_word:
        question: "What is the capital of France?",
        answer: "Paris",
        type: "one_word",
        difficulty: "easy",
        marks: 1

"""


def make_chain_image():

    template = """ 
    You are a teacher and need to create a test for your students

    only give json output and based on the requirments generate the questions.

    The source text is as follows:

    {text}
    
    requirements are as follows:
    {prompt}

    only give correct no of questions don't give extra questions,
    don't repeat the same question, and keep the questions unique.
    also give for each question type,difficulty and marks.

    give output in json and all questions in a list.
    """
    
    final_prompt = ChatPromptTemplate.from_template(template)

    model = ChatOllama(model="llama3.1",format="json")

    # RAG pipeline
    chain = ( 
        final_prompt
        | model
        | JsonOutputParser()
    )

    return chain

def answer_question(prompt,text):
    chain = make_chain_image()
    return chain.invoke({"prompt": prompt,"text":text})