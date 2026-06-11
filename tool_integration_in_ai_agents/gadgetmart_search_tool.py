from pydantic import BaseModel , Field , ValidationError
from sqlalchemy import create_engine , select 
from sqlalchemy.orm import declarative_base , Mapped , mapped_column , sessionmaker
from typing import Optional

Base = declarative_base()

class Product (Base):
    __tablename__ = "products"
    id : Mapped[int] = mapped_column (autoincrement=True , primary_key= True)
    name : Mapped[str] = mapped_column()
    category : Mapped[str] = mapped_column()
    price : Mapped[int] = mapped_column()
    in_stock : Mapped[bool] = mapped_column()

engine = create_engine("sqlite:///gadgetmart.db" , echo= False)
Base.metadata.create_all(engine)
Session_local = sessionmaker(bind=engine)

SAMPLE_PRODUCTS = [
    {"name": "iPhone 15", "category": "mobile", "price": 79900, "in_stock": True},
    {"name": "Samsung Galaxy S24", "category": "mobile", "price": 74999, "in_stock": True},
    {"name": "OnePlus 12R", "category": "mobile", "price": 42999, "in_stock": True},
    {"name": "Google Pixel 8", "category": "mobile", "price": 54999, "in_stock": False},
    {"name": "Redmi Note 13", "category": "mobile", "price": 18999, "in_stock": True},
    {"name": "Motorola Edge 40", "category": "mobile", "price": 29999, "in_stock": True},
]

class ProductSearchInput (BaseModel):
    category : str = Field (... , min_length = 1)
    max_price : int = Field (... , gt = 0)
    in_stock : bool = True

def insert_data()-> None:
    with Session_local() as session:
        existing = session.scalar(
            select(Product).limit(1)
        )
        if existing:
            return
        
        products = [Product(**row) for row in SAMPLE_PRODUCTS]
        session.add_all(products)
        session.commit()

def search_product (input_data: dict ):
    """
    Tool function: validate dict input, query ORM, return rows or an error dict.
    """
    try:
        # Unpack the incoming dict into a validated Pydantic object
        validated_input = ProductSearchInput(**input_data)
    except ValidationError as err:
        # Return structured failure instead of raising to the agent runtime
        return {
            "success": False,
            "error": "Invalid input provided",
            "details": err.errors(),
        }
    
    with Session_local() as session:
        query = select(Product).where(
            Product.category == validated_input.category,
            Product.price <= validated_input.max_price,
            Product.in_stock == validated_input.in_stock,
        )
        products_from_db = session.scalars(query).all()
        return {
            "success": True,
            "products": [
                {
                    "name": p.name,
                    "price": p.price
                }
                for p in products_from_db
            ]
        }
    
def agent_flow():

    tool_calls = [
        {
            "tool_name": "search_product_tool",
            "arguments": {
                "category": "mobile",
                "max_price": 50000,
                "in_stock": True,
            },
        }
    ]

    for tool_call in tool_calls:
        arguments = tool_call["arguments"]

        tool_output = search_product(arguments)

        if tool_output["success"]:
            for product in tool_output["products"]:
                print(f'{product["name"]} — ₹{product["price"]}')
        else:
            print(f'Search failed: {tool_output["error"]}')


# Standard entry point when running: seed data, then run the simulated agent flow
if __name__ == "__main__":
    insert_data()
    agent_flow()
