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
        /* Expense Calculation Results Styling */
        .stApp .stMarkdown h3 {
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            color: #2e6ef7;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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

    st.title("Current You Tool")

    st.subheader("Step 1: Enter Your Expenses")

    st.write("""
    In this tool, we focus on getting to know your current financial habits. What do you currently spend your money on?

    We’ll analyze your spending categories to offer insights into your current expenses and compare them to the money you'd like to spend on a monthly basis to reach your future you goals. When entering your expenses, aim for accuracy to get the best insights. Using the past three months of income and spending as a guide will help provide an average for a typical month. Reviewing your credit card and bank statements is a great way to start.
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

    # Input expense limit from Future You tool
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

        # Check if total expenses exceed, match, or are below Future You limit
        if total_expenses > future_you_limit:
            over_limit = total_expenses - future_you_limit
            st.write(f"### Uh oh! You are over your Future You limit by ${over_limit:.2f}. Consider adjusting your expenses or revisiting the Future You tool.")

            # Calculate percentages for pie chart
            over_percentage = (over_limit) * 100
            allocation_data = {
                'Future You Limit': future_you_limit,
                f'Over Future You Limit ({over_percentage:.1f}%)': over_limit
            }

            # Pie chart showing over limit as percentage of the goal
            fig2 = create_pie_chart(allocation_data, 'Expenses vs Future You Limit', colors=['#ff9999', '#66b3ff'])
            st.pyplot(fig2)

        elif total_expenses == future_you_limit:
            st.write(f"### Great! Your current expenses are in line with your Future You goals. This means you are on track to achieve your future goals, while also living life as you are today.")

        else:
            st.write(f"### Great! You are under your Future You limit by ${future_you_limit - total_expenses:.2f}.")
            
            # Pie chart showing remaining limit
            allocation_data = {
                'Expenses': total_expenses,
                'Remaining from Future You Limit': future_you_limit - total_expenses
            }
            fig2 = create_pie_chart(allocation_data, 'Comparison to Future You Limit', colors=['#ff9999', '#66b3ff'])
            st.pyplot(fig2)

        # Bar chart for expense breakdown
        all_expenses_data = {**fixed_expenses_data, **variable_expenses_data}
        fig = create_bar_chart(all_expenses_data, 'Expense Breakdown')
        st.pyplot(fig)

if __name__ == "__main__":
    main()
