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

    # Add descriptive text below the title
    st.write("""
    In this section we want to help understand you - today! What do you like & want to do with your money that helps you live the life you want to live today.
    """)

    # Initialize session state variables
    if 'total_expenses' not in st.session_state:
        st.session_state.total_expenses = 0.0
    if 'monthly_income' not in st.session_state:
        st.session_state.monthly_income = 0.0
    if 'savings' not in st.session_state:
        st.session_state.savings = 0.0
    if 'investments' not in st.session_state:
        st.session_state.investments = 0.0

    # First Section: Overview
    st.header("Monthly Overview")
    col1, col2 = st.columns(2)
    with col1:
        monthly_income = st.number_input("Enter your monthly income:", min_value=0.0, step=100.0)
        st.session_state.monthly_income = monthly_income
        savings = st.number_input("Amount allocated to savings:", min_value=0.0, step=10.0)
        st.session_state.savings = savings
    
    with col2:
        investments = st.number_input("Amount allocated to investments:", min_value=0.0, step=10.0)
        st.session_state.investments = investments
        total_expenses = st.number_input("Total monthly expenses:", min_value=0.0, step=10.0)
        st.session_state.total_expenses = total_expenses

    # Calculate and display results for the first section
    if st.button("Calculate Overview"):
        total_allocations = savings + investments + total_expenses

        st.subheader("Results")
        st.write(f"**Total Monthly Income:** ${monthly_income:.2f}")
        st.write(f"**Total Allocations:** ${total_allocations:.2f}")
        st.write(f"**Difference:** ${monthly_income - total_allocations:.2f}")

        # Pie chart for income allocation
        income_data = {
            'Savings': savings,
            'Investments': investments,
            'Expenses': total_expenses,
        }
        unallocated = max(0, monthly_income - total_allocations)
        if unallocated > 0:
            income_data['Unallocated'] = unallocated

        fig = create_pie_chart(income_data, 'Income Allocation')
        st.pyplot(fig)

    # Second Section: Expense Breakdown
    st.header("Expense Breakdown")
    
    st.subheader("Future You Tool")
    future_you_expense_limit = st.number_input("Enter your monthly expense limit from the Future You tool:", min_value=0.0, step=10.0)

    st.subheader("Fixed Expenses")
    # Fixed expenses default categories
    fixed_expenses_data = {}
    fixed_categories = ['Housing', 'Utilities', 'Insurance', 'Transportation', 'Debt Payments', 'Groceries']
    for category in fixed_categories:
        amount = st.number_input(f"{category}:", min_value=0.0, step=10.0)
        fixed_expenses_data[category] = amount

    # Additional fixed expenses
    if 'fixed_counter' not in st.session_state:
        st.session_state.fixed_counter = 0

    if st.button("➕ Add Fixed Expense Category"):
        st.session_state.fixed_counter += 1

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

    # Additional variable expenses
    if 'variable_counter' not in st.session_state:
        st.session_state.variable_counter = 0

    if st.button("➕ Add Variable Expense Category"):
        st.session_state.variable_counter += 1

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

        if abs(calculated_total_expenses - st.session_state.total_expenses) > 0.01:
            st.warning(f"The sum of your expenses (${calculated_total_expenses:.2f}) does not match the total expenses you entered (${st.session_state.total_expenses:.2f}). Please adjust your entries.")
        else:
            st.subheader("Expense Comparison")
            difference = future_you_expense_limit - calculated_total_expenses
            if difference > 0:
                st.write(f"**Great job!** You are ${difference:.2f} below your Future You expense limit.")
            elif difference < 0:
                st.write(f"**Heads up!** You are ${-difference:.2f} above your Future You expense limit.")
            else:
                st.write("You have hit your Future You expense limit exactly.")

            # Bar chart for expense breakdown
            fig = create_bar_chart(expense_data, 'Expense Breakdown')
            st.pyplot(fig)

if __name__ == "__main__":
    main()
