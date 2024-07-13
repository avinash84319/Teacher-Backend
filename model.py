from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser


def make_chain_image():

    template = """ 
    You are a teacher and need to create a test for your students, based on the following text:
    {prompt}
    """
    
    final_prompt = ChatPromptTemplate.from_template(template)

    # Option 1: LLM
    model = ChatOllama(model="llava")
    # Option 2: Multi-modal LLM
    # model = LLaVA

    # RAG pipeline
    chain = ( 
        final_prompt
        | model
        | JsonOutputParser()
    )

    return chain

def answer_question(prompt):
    chain = make_chain_image()
    return chain.invoke({"prompt": prompt})