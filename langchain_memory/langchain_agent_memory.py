from langchain_classic.agents import AgentExecutor , create_tool_calling_agent
from langchain_core.messages import AIMessage , HumanMessage 
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

ORDERS = {
    "ORD-101": {
        "status": "out for delivery",
        "city": "Delhi",
        "amount": 2500,
        "delivery_days": 2
    },
    "ORD-102": {
        "status": "cancelled",
        "city": "Bangalore",
        "amount": 4000,
        "delivery_days": 0
    },
}
@tool
def get_order_status(order_id : str):
    """
    Returns the status of the order id given by the user.

    Use this tool when the user is asking about the order tracking status.
    """
    order = ORDERS.get(order_id)
    if not order :
        return f" No order found with the order id : {order_id}"
    
    return f" The order status for the order id {order_id} is {order['status']}"

tools = [
    get_order_status
]

llm = ChatGoogleGenerativeAI(
    model= "gemini-2.5-flash",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a helpful customer support agent.

        Rules:
        - If the user gives an order id, remember it for this conversation.
        - If the user asks a follow-up like "track it" or "where is it", use the order id from chat history.
        - Use tools when order status is required.
        - If no order id is available, politely ask the user for the order id.
        """
    ),

    # previous message of the conversation will be inserted in the chat_history.
    # optional=True makes the chat_history parameter as optional.
    MessagesPlaceholder(variable_name="chat_history", optional=True),

    ("human", "{input}"),

    # Tool-Calling agent intermediate steps will be store here.
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent= agent,
    tools=tools,
    verbose=True
) 

chat_history = []

def ask_agent(user_input : str):
    response = agent_executor.invoke(
        {
            "input" : user_input,
            "chat_history": chat_history
        }
    )
    chat_history.append(HumanMessage(user_input))
    chat_history.append(AIMessage(response['output']))

    return response['output']

print("Turn-1")
user_input = "Hi, my order id ORD-102."
print("User Input: ", user_input)
print("AI response: ", ask_agent(user_input))

print("====================================\n")

print("Turn-2")
user_input = "What is the status of it ?"
print("User Input: ", user_input)
print("AI response: ", ask_agent(user_input))

print("====================================\n")   

print (len(chat_history))