import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Apply custom styles using markdown
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

    st.write("""
    In this section, we will help you understand your current financial situation.
    We'll look at your overall money allocation and provide insights on how to optimize
    your monthly expenses and savings.
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

        # Calculate savings and investments percentage
        if monthly_income == 0:
            savings_investments_percentage = 0
        else:
            savings_investments_percentage = ((savings + investments) / monthly_income) * 100

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

    # More sections and functionality can be added here...

if __name__ == "__main__":
    main()
