import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS for cleaner aesthetics
def set_custom_styles():
    st.markdown(
        """
        <style>
        /* Background color */
        .stApp {
            background-color: #fafafa;
        }
        /* Title and Subheader styling */
        .stApp h1, .stApp h2 {
            color: #3a3a3a;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
        }
        /* Text styling */
        .stApp p, .stApp div, .stApp span, .stApp label {
            color: #4f4f4f;
            font-family: 'Verdana', sans-serif;
        }
        /* Button styling */
        .stButton>button {
            color: white;
            background-color: #2e6ef7;
            border-radius: 5px;
            padding: 0.6em 1.2em;
            font-weight: bold;
        }
        /* Input field styling */
        input {
            border: 2px solid #2e6ef7;
            border-radius: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to calculate fixed expense ratio
def calculate_fixed_expense_ratio(income, fixed_expenses):
    if income == 0:
        return 0
    return (fixed_expenses / income) * 100

# Function to generate feedback message based on ratio
def get_ratio_message(ratio):
    if ratio > 80:
        return "Your fixed expenses are high compared to your income. This may limit your ability to meet other financial goals."
    elif 60 <= ratio <= 80:
        return "Your fixed expenses are moderate but worth monitoring, especially for long-term planning."
    else:
        return "Your fixed expense ratio is in a healthy range, allowing more flexibility for savings and investments."

# Function to create pie chart
def create_pie_chart(data, title, colors=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})
    ax.set_title(title, fontweight="bold")
    plt.axis('equal')
    return fig

# Function to create bar chart
def create_bar_chart(data, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(data.keys(), data.values(), color='#2e6ef7')
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel('Amount ($)', fontweight="bold")
    plt.xticks(rotation=45, ha='right')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(data.values()),
                f'${height:.2f}', ha='center', va='bottom')
        
    plt.tight_layout()
    return fig

def main():
    # Apply custom styles
    set_custom_styles()

    st.title("Expense Breakdown Tracker")

    st.subheader("Step 1: Enter Your Expenses")

    st.write("""
    In this section we want to help understand you - today! What do you like & want to do with your money that helps you live the life you want to live today.

    We will look at your spending categories to give some insights on how you spend your money and how this compares to the money you want to spend to reach your dream life goals. When inputting expenses: please make it as accurate as possible for the best results. Reference your last three months of income & spending to average a normal month. Checking your credit card / debit card bills is a great way to go. We find this also makes it easier to be honest with expenses.
    """)

    # Initialize session state variables
    if 'fixed_expenses' not in st.session_state:
        st.session_state.fixed_expenses = {}
    if 'variable_expenses' not in st.session_state:
        st.session_state.variable_expenses = {}

    # Expense categories
    fixed_categories = ['Housing', 'Utilities', 'Insurance', 'Transportation', 'Debt Payments', 'Groceries']
    variable_categories = ['Fun (trips, vacations etc.)']

    st.subheader("Fixed Expenses")
    fixed_expenses_data = {}
    for category in fixed_categories:
        amount = st.number_input(f"{category}:", min_value=0.0, step=10.0)
        fixed_expenses_data[category] = amount

    st.subheader("Variable Expenses")
    variable_expenses_data = {}
    for category in variable_categories:
        amount = st.number_input(f"{category}:", min_value=0.0, step=10.0)
        variable_expenses_data[category] = amount

    # Input additional expenses
    st.subheader("Step 2: Enter Expense Limit from 'Future You' Tool")
    future_you_limit = st.number_input("Enter the expense limit suggested by the Future You tool:", min_value=0.0, step=10.0)

    # Calculate total expenses
    if st.button("Calculate Expenses"):
        total_expenses = sum(fixed_expenses_data.values()) + sum(variable_expenses_data.values())
        fixed_total = sum(fixed_expenses_data.values())
        variable_total = sum(variable_expenses_data.values())

        st.subheader("Results")

        st.write(f"**Total Fixed Expenses:** ${fixed_total:.2f}")
        st.write(f"**Total Variable Expenses:** ${variable_total:.2f}")
        st.write(f"**Total Expenses:** ${total_expenses:.2f}")
        st.write(f"**Expense Limit (Future You):** ${future_you_limit:.2f}")

        if total_expenses > future_you_limit:
            st.write(f"**Uh oh! You are above your Future You limit by ${total_expenses - future_you_limit:.2f}. Try playing around with certain expense categories to see if you can get it within your Future You limit. If not, let's revisit the Future You tool and see where we can make adjustments so that you can enjoy life now, and enjoy life in the future!**")
        else:
            st.write(f"**Great! You are below your Future You limit by ${future_you_limit - total_expenses:.2f}.**")

        # Bar chart for expense breakdown
        all_expenses_data = {**fixed_expenses_data, **variable_expenses_data}
        fig = create_bar_chart(all_expenses_data, 'Expense Breakdown')
        st.pyplot(fig)

        # Pie chart for expenses vs Future You limit
        allocation_data = {
            'Expenses': total_expenses,
            'Remaining from Future You Limit': max(0, future_you_limit - total_expenses)
        }
        fig2 = create_pie_chart(allocation_data, 'Comparison to Future You Limit', colors=['#ff9999','#66b3ff'])
        st.pyplot(fig2)

if __name__ == "__main__":
    main()
