from langchain_openai import ChatOpenAI
from config import OPENAI_MODEL_NAME, OPENAI_API_KEY
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import logger
from models import Prompt
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.callbacks import get_openai_callback

class OpenAI:
    """
    OpenAI interaction class
    """

    def __init__(
        self, 
        vector_store,
    )-> None:
        self.vector_store = vector_store
        self.openai_api_key = OPENAI_API_KEY
        self.model_name = OPENAI_MODEL_NAME

    def connect(self):
        """
        Connect the chat openai instance
        """
        params = {
            "openai_api_key": self.openai_api_key,
            "model": self.model_name,
        }

        return ChatOpenAI(**params)
    
    def build_prompts(self, prompts: list[Prompt])-> ChatPromptTemplate:
        """
        Build Prompts like system message, human message
        """
        messages=[]

        for prompt in prompts:
            if not prompt.content or prompt.content.strip() == "":
                continue
            if prompt.type == "system":
                messages.append(
                    SystemMessage(
                        content=prompt.content,
                    )
                )
            elif prompt.type == "human":
                messages.append(
                    HumanMessage(
                        content=prompt.content,
                    )
                )

        return ChatPromptTemplate(messages=messages, input_variables=[])
    
    def build_chain(self,prompts,client) -> ChatPromptTemplate:
        """
        Build the chain
        """
        try:
            chain = prompts | client | StrOutputParser()
        except Exception as e:
            logger.exception(
                "A Exception occurred while building langchain chain: %s",
                e,
                stack_info=True,
            )
            raise e
        
        return chain
        
    def invoke_langchain_chain(self, chain) -> str:
        """
        Invoke langchain chain and return the response with usage information. 
        """
        with get_openai_callback() as cb:
            response = chain.invoke({})
            extra = cb
        
        return response, extra
    
    def execute_prompts(
        self,
        prompts: list,
    ):
        """
        Execute prompts
        """

        if not prompts:
            raise Exception("No Prompts given")
        
        # prepare prompts
        prompts = self.build_prompts(prompts)

        # connect
        client = self.connect()

        # build chain
        chain = self.build_chain(prompts, client)

        # Invoke chain
        response, extra = self.invoke_langchain_chain(chain)

        logger.debug(
            f"""
            Total Tokens: {extra.total_tokens}
            Prompt Tokens: {extra.prompt_tokens}
            Completion Tokens: {extra.completion_tokens}
            Total Cost: {extra.total_cost}
            Model Name: {self.model_name}
            """
        )

        return response



    


    
