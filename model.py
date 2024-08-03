from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser

def make_chain_image():

    template = """ 

    The source text is as follows:
    {text}
    
    based on the text, generate all the following json fields with proper values for the following jsons:
    {prompt}

    and give the output in list of questions and no of questions in the list should be equal to the number of jsons in the prompt
    
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

def check_model():
    
    return answer_question("hello","hello")