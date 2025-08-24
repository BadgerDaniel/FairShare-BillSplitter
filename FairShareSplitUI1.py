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
    
    # New dictionaries to track detailed information
    person_items = {person: [] for person in person_list}
    person_tax_amounts = copy.deepcopy(person_dict)
    person_tip_amounts = copy.deepcopy(person_dict)

    running_total_preTaxTip = 0

    for item, cost, names in items:
        split_cost_of_item = cost / len(names)
        running_total_preTaxTip += split_cost_of_item * len(names)

        for name in names:
            person_dict[name] += split_cost_of_item
            # Track what each person ate and their portion cost
            person_items[name].append({
                'item': item,
                'total_cost': cost,
                'portion_cost': split_cost_of_item,
                'shared_with': names
            })

    total_tax_tip = tax_amount + tip_amount
    total_bill = running_total_preTaxTip + total_tax_tip

    for person in person_dict_percent_of_bill.keys():
        person_dict_percent_of_bill[person] = person_dict[person] / running_total_preTaxTip

    for person in person_dict:
        person_tip_to_pay = person_dict_percent_of_bill[person] * tip_amount
        person_tax_to_pay = person_dict_percent_of_bill[person] * tax_amount
        person_tax_tip_to_pay = person_tax_to_pay + person_tip_to_pay
        person_final_total = person_tax_tip_to_pay + person_dict[person]
        person_dict_final[person] = round(person_final_total, 2)
        
        # Store tax and tip amounts for detailed breakdown
        person_tax_amounts[person] = round(person_tax_to_pay, 2)
        person_tip_amounts[person] = round(person_tip_to_pay, 2)

    return {
        'final_amounts': person_dict_final,
        'pre_tax_tip_amounts': person_dict,
        'percentages': person_dict_percent_of_bill,
        'tax_amounts': person_tax_amounts,
        'tip_amounts': person_tip_amounts,
        'person_items': person_items,
        'total_pre_tax_tip': running_total_preTaxTip,
        'total_tax': tax_amount,
        'total_tip': tip_amount,
        'total_bill': total_bill
    }

def display_detailed_breakdown(result):
    """Display comprehensive bill breakdown"""
    
    # Total amounts section
    st.header("📊 Total Bill Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pre-Tax & Tip", f"${result['total_pre_tax_tip']:.2f}")
    with col2:
        st.metric("Tax", f"${result['total_tax']:.2f}")
    with col3:
        st.metric("Tip", f"${result['total_tip']:.2f}")
    with col4:
        st.metric("**Total Bill**", f"**${result['total_bill']:.2f}**")
    
    st.divider()
    
    # Per-person breakdown
    st.header("👥 Per-Person Breakdown")
    
    for person in result['final_amounts'].keys():
        with st.expander(f"**{person}** - Total: ${result['final_amounts'][person]:.2f}", expanded=True):
            
            # Items they ate
            st.subheader("🍽️ Items Consumed")
            if result['person_items'][person]:
                items_data = []
                for item_info in result['person_items'][person]:
                    shared_text = f" (shared with {', '.join(item_info['shared_with'])})" if len(item_info['shared_with']) > 1 else ""
                    items_data.append({
                        "Item": item_info['item'],
                        "Total Cost": f"${item_info['total_cost']:.2f}",
                        "Your Portion": f"${item_info['portion_cost']:.2f}",
                        "Details": shared_text
                    })
                
                items_df = pd.DataFrame(items_data)
                st.dataframe(items_df, use_container_width=True)
                
                # Summary of their food costs
                food_total = result['pre_tax_tip_amounts'][person]
                st.info(f"**Total Food Cost: ${food_total:.2f}**")
            else:
                st.write("No items consumed")
            
            # Percentage breakdown
            st.subheader("📊 Cost Breakdown")
            percentage = result['percentages'][person] * 100
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Food Cost", f"${food_total:.2f}")
            with col2:
                st.metric("Bill %", f"{percentage:.1f}%")
            with col3:
                st.metric("Tax Portion", f"${result['tax_amounts'][person]:.2f}")
            with col4:
                st.metric("Tip Portion", f"${result['tip_amounts'][person]:.2f}")
            
            # Final calculation breakdown
            st.subheader("🧮 Final Calculation")
            breakdown_text = f"""
            - **Food Cost**: ${food_total:.2f}
            - **Tax** ({percentage:.1f}% of ${result['total_tax']:.2f}): ${result['tax_amounts'][person]:.2f}
            - **Tip** ({percentage:.1f}% of ${result['total_tip']:.2f}): ${result['tip_amounts'][person]:.2f}
            - **Total**: ${result['final_amounts'][person]:.2f}
            """
            st.markdown(breakdown_text)

def owed_from_xl(filepath, tax_amount, tip_amount):
    df = pd.read_excel(filepath)
    items = []
    for index, row in df.iterrows():
        item_name = row['Item']
        item_cost = row['amount']
        consumers = [row[col] for col in df.columns[2:] if not pd.isnull(row[col])]
        items.append((item_name, item_cost, consumers))

    return money_owed(items, tax_amount, tip_amount)

def main():
    st.title("Fair Share Bill Splitter")
    st.markdown("Split your restaurant bill fairly based on what each person actually consumed!")

    option = st.selectbox(
        "How would you like to input the bill details?",
        ("Upload Excel file", "Enter manually")
    )

    if option == "Upload Excel file":
        st.info("**Excel Format:** First column should be 'Item', second column should be 'amount', and subsequent columns should contain person names. Mark with any value (like 'X') if a person consumed that item.")
        uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
        tax_amount = st.number_input("Enter tax amount", min_value=0.0, format="%.2f")
        tip_amount = st.number_input("Enter tip amount", min_value=0.0, format="%.2f")
        
        if uploaded_file and tax_amount and tip_amount:
            try:
                result = owed_from_xl(uploaded_file, tax_amount, tip_amount)
                
                if not result['final_amounts']:
                    st.error("No valid data found in the Excel file. Please check the format.")
                    return
                    
                st.write("**Final amounts owed by each person:**")
                
                # Display final amounts in a clean format
                final_amounts = result['final_amounts']
                for person, amount in final_amounts.items():
                    st.metric(f"{person}", f"${amount:.2f}")
                
                st.divider()
                display_detailed_breakdown(result)
                
            except Exception as e:
                st.error(f"Error processing the Excel file: {str(e)}")
                st.info("Please ensure your Excel file has columns: 'Item', 'amount', and person names in subsequent columns.")
    else:
        st.info("**Manual Input:** Enter each item, its price, and the people who consumed it. Separate multiple people with commas.")
        item_count = st.number_input("How many different items?", min_value=1, step=1)
        
        items = []
        for i in range(item_count):
            item_name = st.text_input(f"Item {i+1} name")
            item_price = st.number_input(f"Item {i+1} price", min_value=0.0, format="%.2f")
            item_people_input = st.text_input(f"People who ate item {i+1} (comma-separated)")
            # Clean up the people list - remove empty strings and whitespace
            item_people = [name.strip() for name in item_people_input.split(",") if name.strip()]
            items.append((item_name, item_price, item_people))
        
        tax_amount = st.number_input("Enter tax amount", min_value=0.0, format="%.2f")
        tip_amount = st.number_input("Enter tip amount", min_value=0.0, format="%.2f")
        
        if st.button("Calculate"):
            # Validate inputs
            if not items or not all(items):
                st.error("Please fill in all item details.")
                return
                
            if not any(item[2] for item in items):  # Check if any people are specified
                st.error("Please specify at least one person for each item.")
                return
                
            try:
                result = money_owed(items, tax_amount, tip_amount)
                st.write("**Final amounts owed by each person:**")
                
                # Display final amounts in a clean format
                final_amounts = result['final_amounts']
                for person, amount in final_amounts.items():
                    st.metric(f"{person}", f"${amount:.2f}")
                
                st.divider()
                display_detailed_breakdown(result)
                
            except Exception as e:
                st.error(f"Error calculating bill split: {str(e)}")

if __name__ == "__main__":
    main()
