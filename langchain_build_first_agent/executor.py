from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

# Fake Database.
ORDERS = {
    "ORD-101": {
        "status": "shipped",
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
    "ORD-103": {
        "status": "delivered",
        "city": "Mumbai",
        "amount": 1500,
        "delivery_days": 0
    }
}

@tool 
def get_order_status(order_id: str) -> str:
    """
    Get the current status of order id provided in the input.
    Use this tool when the user ask about the order status for a specific order_id.
    """
    order = ORDERS.get(order_id)

    if not order:
        return f"There is no such order with the id {order_id}"
    
    return f"The status of {order_id} is {order['status']}"


@tool
def estimate_delivery_timeline(order_id: str) -> str:
    """
    estimates delivery timeline for the order id.
    Use this tool when the user asks for the ETA , delivery timeline for a specific order_id
    """
    order = ORDERS.get(order_id)

    if not order:
        return f"There is no such order with the id {order_id}"

    if {order['status']} == ['cancelled']:
        return f"The order with {order_id} is already cancelled"
    
    if {order['status']} == ['delivered']:
        return f"The order with {order_id} is alredy {order['status']}"
    
    if {order['status']} == ['shipped']:
        return f"the order with {order_id} is already shipped and is excepted to arrive in {order['delivery_days']}"
    
    return f"Delivery status is not available for order id :{order_id}"

@tool
def calculate_refund_amount(order_id: str) -> str:
    """
    it will calucute the refund amonut of the given order id. 
    Use this tool when user ask about refund for a specific order id"""

    order = ORDERS.get(order_id)

    if not order:
        return f"There is no such order with the id {order_id}"
    
    if order['status'] == 'cancelled':
        return f"refund amount of the order id : {order_id} is {order['amount']}"
    
    if order['status'] == 'delivered':
        return (
            f"Order id {order_id} has already been delivered."
            f"refund eligibility depends on the policy "
            )
    
    if order['status'] == 'shipped':
        return f"order id {order_id} has been shipped. Refund cant be calculated at this stage."
    

tools = [
    get_order_status,
    estimate_delivery_timeline,
    calculate_refund_amount
]

llm= ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages(
     [
        (
            "system",
            """
            You are a helpful e-commerce support assistant.

            Rules:
            1. Use tools only when required.
            2. If the user asks about a specific order, use the relevant tool.
            3. If the user asks a general conceptual question, answer directly without tools.
            4. If order id is missing, ask the user for the order id.
            5. Keep the final answer clear and beginner-friendly.
            """
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

agent = create_tool_calling_agent(
    tools=tools,
    llm=llm,
    prompt=prompt
)
    
agent_executor = AgentExecutor(
    tools=tools,
    llm= llm,
    agent=agent,
    max_iterations=3,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
    verbose=True,
)


test_queries = [
    "What is the status of order ORD-101?", 
    "What is the status of order ORD-103 and how much refund will I get?",  
    "What services can you help me with?",  
    "What is the status of order ORD-999?"
]

for query_no, query in enumerate(test_queries, start=1):
    print(f"\n{'=' * 50}")
    print(f"Query {query_no}: {query}")

    result = agent_executor.invoke({"input": query})

    print("\nFinal Output:")
    print(result["output"])

    print("\nIntermediate Steps:")
    for step_no, (action, observation) in enumerate(
        result["intermediate_steps"], start=1
    ):
        print(f"\nStep {step_no}")
        print(f"Tool selected: {action.tool}")
        print(f"Tool input: {action.tool_input}")
        print(f"Tool observation: {observation}")