from main import config
from agents import Agent, Runner, function_tool
import streamlit as st
from whtsapptool import send_whatsapp_message
import asyncio

# Product search tool
@function_tool
def search_product(query: str):
    """
    Search product in the database if it is available or not.
    Handles case-insensitive matching for categories and items.
    """
    product = {
        "Electronics": ["Smartphone", "Laptop", "Wireless Earbuds", "Smartwatch", "Bluetooth Speaker"],
        "Clothing": ["Men's T-Shirts", "Women's Dresses", "Jeans", "Hoodies", "Jackets"],
        "Beauty & Personal Care": ["Face Wash", "Moisturizer", "Shampoo", "Lipstick", "Perfume"],
    }

    query_lower = query.lower()

    # First check for category match
    for category, items in product.items():
        if query_lower == category.lower():
            return f"Products in '{category}':\n- " + "\n- ".join(items)

    # Then check for item match
    for category, items in product.items():
        for item in items:
            if query_lower in item.lower():
                return f"Item '{item}' found in category '{category}'"

    return f"No products found for query: '{query}'. Try categories like: {', '.join(product.keys())}"

# Create agent
find_product_agent = Agent(
    name="find_product",
    instructions="You are the product search agent. You can use the tool to search products in the list.",
    tools=[search_product, send_whatsapp_message],
    model=config.model,
)

# Streamlit UI setup
st.set_page_config(page_title="🛍️ Product Search Agent")
st.title("🛍️ Product Search Chat")

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Show full chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Enter a category (e.g. Electronics, Clothing)..."):
    # Show user message
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant "Thinking"
    with st.chat_message("assistant"):
        st.markdown("Thinking...")

    # Run agent
    try:
        result = asyncio.run(Runner.run(find_product_agent, input=st.session_state.history))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(Runner.run(find_product_agent, input=st.session_state.history))

    response = result.final_output

    # Save assistant response
    st.session_state.history.append({"role": "assistant", "content": response})
     
    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response)