from langchain import PromptTemplate

QA_PROMPT_TEXT = """Use the following pieces of information to answer the user’s question.
If you don’t know the answer, just say that you don’t know, don’t try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful and Caring answer:
"""

QA_PROMPT_TEMPLATE = PromptTemplate(
    template=QA_PROMPT_TEXT,                        
    input_variables=['context', 'question']
)