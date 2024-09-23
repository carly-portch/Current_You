import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to inject CSS directly
def set_bg_style():
    st.markdown(
        """
        <style>
        /* Background color */
        .stApp {
            background-color: #f0f2f6;
        }
        /* Title color */
        .stApp h1 {
            color: #2e6ef7;
        }
        /* Subheader color */
        .stApp h2 {
            color: #2e6ef7;
        }
        /* Button styling */
        .stButton>button {
            color: white;
            background-color: #2e6ef7;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
        /* Input styling */
        input {
            border: 1px solid #2e6ef7;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def calculate_fixed_expense_ratio(income, fixed_expenses):
    if income == 0:
        return 0
    return (fixed_expenses / income) * 100

def get_ratio_message(ratio):
    if ratio > 80:
        return "Your fixed expenses are quite high compared to your income. This can result in anxiety or stress as well as missing your goals."
    elif 60 <= ratio <= 80:
        return "Your fixed expenses are on the higher side but manageable, especially if you live in a high cost of living area or have a young family."
    else:
        return "You have a great fixed expense ratio leaving lots of money for play and investing."

def create_pie_chart(data, title, colors=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})
    ax.set_title(title)
    plt.axis('equal')
    return fig

def create_bar_chart(data, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(data.keys(), data.values(), color='#2e6ef7')
    ax.set_title(title)
    ax.set_ylabel('Amount ($)')
    plt.xticks(rotation=45, ha='right')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(data.values()),
                f'${height:.2f}',
                ha='center', va='bottom')
        
    plt.tight_layout()
    return fig

def main():
    # Apply custom styles
    set_bg_style()
    
    st.title("Personal Finance Tracker 💰")

    # Initialize session state variables
    if 'total_expenses' not in st.session_state:
        st.session_state.total_expenses = 0.0
    if 'fixed_expenses' not in st.session_state:
        st.session_state.fixed_expenses = []
    if 'variable_expenses' not in st.session_state:
        st.session_state.variable_expenses = []

    # Second Section: Expense Breakdown
    st.header("Expense Breakdown")
    st.write("""
    Enter your current expense breakdown and see how it compares to the expense limit suggested by the 'Future You' tool.
    """)

    # Input for "Future You" expense limit
    future_you_expense_limit = st.number_input("Enter your expense limit from the 'Future You' tool:", min_value=0.0, step=10.0)

    st.subheader("Fixed Expenses")

    # Fixed expenses default categories
    fixed_expenses_data = {}
    fixed_categories = ['Housing', 'Utilities', 'Insurance', 'Transportation', 'Debt Payments', 'Groceries']
    for category in fixed_categories:
        amount = st.number_input(f"{category}:", min_value=0.0, step=10.0)
        fixed_expenses_data[category] = amount

    # Initialize counters for additional expenses
    if 'fixed_counter' not in st.session_state:
        st.session_state.fixed_counter = 0
    if 'variable_counter' not in st.session_state:
        st.session_state.variable_counter = 0

    # Function to add new fixed expense
    if st.button("➕ Add Fixed Expense Category"):
        st.session_state.fixed_counter += 1

    # Display additional fixed expense inputs
    for i in range(st.session_state.fixed_counter):
        extra_category = st.text_input(f"Fixed Expense Category {i+1} Name:", key=f"fixed_extra_name_{i}")
        extra_amount = st.number_input(f"{extra_category} Amount:", min_value=0.0, step=10.0, key=f"fixed_extra_amount_{i}")
        if extra_category:
            fixed_expenses_data[extra_category] = extra_amount

    st.subheader("Variable Expenses")

    # Variable expenses default categories
    variable_expenses_data = {}
    variable_categories = ['Fun (trips, vacations etc.)']
    for category in variable_categories:
        amount = st.number_input(f"{category}:", min_value=0.0, step=10.0)
        variable_expenses_data[category] = amount

    # Function to add new variable expense
    if st.button("➕ Add Variable Expense Category"):
        st.session_state.variable_counter += 1

    # Display additional variable expense inputs
    for i in range(st.session_state.variable_counter):
        extra_category = st.text_input(f"Variable Expense Category {i+1} Name:", key=f"variable_extra_name_{i}")
        extra_amount = st.number_input(f"{extra_category} Amount:", min_value=0.0, step=10.0, key=f"variable_extra_amount_{i}")
        if extra_category:
            variable_expenses_data[extra_category] = extra_amount

    # Calculate and display results for the second section
    if st.button("Calculate Expenses"):
        # Combine expenses
        expense_data = {**fixed_expenses_data, **variable_expenses_data}
        calculated_total_expenses = sum(expense_data.values())

        # Compare with "Future You" expense limit
        if calculated_total_expenses > future_you_expense_limit:
            st.warning(f"Your total expenses (${calculated_total_expenses:.2f}) exceed your limit from the 'Future You' tool (${future_you_expense_limit:.2f}) by ${calculated_total_expenses - future_you_expense_limit:.2f}.")
        elif calculated_total_expenses < future_you_expense_limit:
            st.success(f"Your total expenses (${calculated_total_expenses:.2f}) are below your limit from the 'Future You' tool (${future_you_expense_limit:.2f}) by ${future_you_expense_limit - calculated_total_expenses:.2f}.")
        else:
            st.info(f"Your total expenses (${calculated_total_expenses:.2f}) exactly match your limit from the 'Future You' tool (${future_you_expense_limit:.2f}).")

        fixed_expenses_total = sum(fixed_expenses_data.values())
        variable_expenses_total = sum(variable_expenses_data.values())
        
        # Bar chart for expense breakdown
        fig = create_bar_chart(expense_data, 'Expense Breakdown')
        st.pyplot(fig)

        # Create a new pie chart for income and expenses allocation
        allocation_data = {
            'Fixed Expenses': fixed_expenses_total,
            'Variable Expenses': variable_expenses_total,
        }

        fig2 = create_pie_chart(allocation_data, 'Expense Allocation')
        st.pyplot(fig2)

if __name__ == "__main__":
    main()
