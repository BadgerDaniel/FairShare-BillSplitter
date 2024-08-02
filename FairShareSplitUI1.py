import streamlit as st
import pandas as pd
import copy

def money_owed(items, tax_amount, tip_amount):
    person_list = []

    for item, cost, names in items:
        for name in names:
            person_list.append(name)

    person_list = list(set(person_list))
    person_dict = dict.fromkeys(person_list)

    for x in person_dict.keys():
        person_dict[x] = 0

    person_dict_percent_of_bill = copy.deepcopy(person_dict)
    person_dict_final = copy.deepcopy(person_dict)

    running_total_preTaxTip = 0

    for item, cost, names in items:
        split_cost_of_item = cost / len(names)
        running_total_preTaxTip += split_cost_of_item * len(names)

        for name in names:
            person_dict[name] += split_cost_of_item

    total_tax_tip = tax_amount + tip_amount

    for person in person_dict_percent_of_bill.keys():
        person_dict_percent_of_bill[person] = person_dict[person] / running_total_preTaxTip

    for person in person_dict:
        person_tip_to_pay = person_dict_percent_of_bill[person] * tip_amount
        person_tax_to_pay = person_dict_percent_of_bill[person] * tax_amount
        person_tax_tip_to_pay = person_tax_to_pay + person_tip_to_pay
        person_final_total = person_tax_tip_to_pay + person_dict[person]
        person_dict_final[person] = round(person_final_total, 2)

    return person_dict_final

def owed_from_xl(filepath, tax_amount, tip_amount):
    df = pd.read_excel(filepath)
    items = []
    for index, row in df.iterrows():
        item_name = row['Item']
        item_cost = row['amount']
        consumers = [row[col] for col in df.columns[2:] if not pd.isnull(row[col])]
        items.append((item_name, item_cost, consumers))

    return money_owed(items, tax_amount, tip_amount)

st.title("Fair Share Bill Splitter")

option = st.selectbox(
    "How would you like to input the bill details?",
    ("Upload Excel file", "Enter manually")
)

if option == "Upload Excel file":
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    tax_amount = st.number_input("Enter tax amount", min_value=0.0, format="%.2f")
    tip_amount = st.number_input("Enter tip amount", min_value=0.0, format="%.2f")
    
    if uploaded_file and tax_amount and tip_amount:
        result = owed_from_xl(uploaded_file, tax_amount, tip_amount)
        st.write("Amounts owed by each person:")
        st.json(result)
else:
    st.write("Enter the items, prices, and the people who ate each item.")
    item_count = st.number_input("How many different items?", min_value=1, step=1)
    
    items = []
    for i in range(item_count):
        item_name = st.text_input(f"Item {i+1} name")
        item_price = st.number_input(f"Item {i+1} price", min_value=0.0, format="%.2f")
        item_people = st.text_input(f"People who ate item {i+1} (comma-separated)").split(",")
        items.append((item_name, item_price, item_people))
    
    tax_amount = st.number_input("Enter tax amount", min_value=0.0, format="%.2f")
    tip_amount = st.number_input("Enter tip amount", min_value=0.0, format="%.2f")
    
    if st.button("Calculate"):
        result = money_owed(items, tax_amount, tip_amount)
        st.write("Amounts owed by each person:")
        st.json(result)
