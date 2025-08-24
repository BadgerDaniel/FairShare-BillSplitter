import streamlit as st
import pandas as pd
import copy

def normalize_name(name):
    """
    Normalize a name by trimming whitespace and converting to title case
    
    Args:
        name: Raw name string
    
    Returns:
        str: Normalized name (trimmed and title case)
    """
    if not name or not isinstance(name, str):
        return ""
    return name.strip().title()

def normalize_names_list(names):
    """
    Normalize a list of names by trimming whitespace and converting to title case
    
    Args:
        names: List of name strings (can include comma-separated values)
    
    Returns:
        list: List of normalized names
    """
    if not names:
        return []
    
    normalized = []
    for name_entry in names:
        if not name_entry or not isinstance(name_entry, str):
            continue
            
        # Split by comma if the entry contains commas
        if ',' in name_entry:
            # Split by comma and process each part
            name_parts = name_entry.split(',')
            for part in name_parts:
                normalized_name = normalize_name(part)
                if normalized_name:  # Only add non-empty names
                    normalized.append(normalized_name)
        else:
            # Single name, normalize it
            normalized_name = normalize_name(name_entry)
            if normalized_name:  # Only add non-empty names
                normalized.append(normalized_name)
    
    return normalized

def money_owed(items, tax_amount, tip_amount):
    person_list = []

    for item, cost, names in items:
        # Normalize the names for this item
        normalized_names = normalize_names_list(names)
        for name in normalized_names:
            person_list.append(name)

    person_list = list(set(person_list))  # Remove duplicates
    person_dict = dict.fromkeys(person_list)

    for x in person_dict.keys():
        person_dict[x] = 0

    person_dict_percent_of_bill = copy.deepcopy(person_dict)
    person_dict_final = copy.deepcopy(person_dict)
    
    # New: Track items each person ate
    person_items = {person: [] for person in person_list}
    
    # New: Track individual costs for each person
    person_individual_costs = {person: 0 for person in person_list}

    running_total_preTaxTip = 0

    for item, cost, names in items:
        # Normalize names for this item
        normalized_names = normalize_names_list(names)
        if not normalized_names:  # Skip items with no valid names
            continue
            
        split_cost_of_item = cost / len(normalized_names)
        running_total_preTaxTip += split_cost_of_item * len(normalized_names)

        for name in normalized_names:
            person_dict[name] += split_cost_of_item
            # Track what each person ate and their individual costs
            person_items[name].append((item, split_cost_of_item))
            person_individual_costs[name] += split_cost_of_item

    total_tax_tip = tax_amount + tip_amount

    for person in person_dict_percent_of_bill.keys():
        person_dict_percent_of_bill[person] = person_dict[person] / running_total_preTaxTip

    for person in person_dict:
        person_tip_to_pay = person_dict_percent_of_bill[person] * tip_amount
        person_tax_to_pay = person_dict_percent_of_bill[person] * tax_amount
        person_tax_tip_to_pay = person_tax_to_pay + person_tip_to_pay
        person_final_total = person_tax_tip_to_pay + person_dict[person]
        person_dict_final[person] = round(person_final_total, 2)

    # New: Return detailed breakdown
    detailed_results = {}
    for person in person_list:
        person_percentage = person_dict_percent_of_bill[person]
        person_tax = person_dict_percent_of_bill[person] * tax_amount
        person_tip = person_dict_percent_of_bill[person] * tip_amount
        
        detailed_results[person] = {
            'items_eaten': person_items[person],
            'subtotal_before_tax_tip': round(person_individual_costs[person], 2),
            'percentage_of_bill': round(person_percentage * 100, 2),
            'tax_amount': round(person_tax, 2),
            'tip_amount': round(person_tip, 2),
            'final_total': round(person_dict_final[person], 2)
        }

    return detailed_results, person_dict_final, running_total_preTaxTip

def calculate_total_bill(items, tax_amount, tip_amount):
    """Calculate the total bill amount including tax and tip"""
    subtotal = sum(cost for _, cost, _ in items)
    total = subtotal + tax_amount + tip_amount
    return subtotal, total

def owed_from_xl(filepath, tax_amount, tip_amount, file_type="excel"):
    """Read bill data from Excel or CSV file"""
    try:
        if file_type == "csv":
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        items = []
        for index, row in df.iterrows():
            item_name = row['Item']
            item_cost = row['amount']
            consumers = [row[col] for col in df.columns[2:] if not pd.isnull(row[col])]
            items.append((item_name, item_cost, consumers))

        return money_owed(items, tax_amount, tip_amount)
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None, None, None

st.title("Fair Share Bill Splitter")

# UI Style Selector
ui_style = st.selectbox(
    "Choose UI Style:",
    ["Classic UI", "Compact UI"],
    help="Classic UI: Full-featured with detailed breakdowns. Compact UI: Streamlined and easier to navigate."
)

# Add info about name normalization
st.info("💡 **Tip**: Names are automatically trimmed and normalized. 'scott, callie' and 'Scott,Callie' will both become 'Scott' and 'Callie'.")

if ui_style == "Classic UI":
    option = st.selectbox(
        "How would you like to input the bill details?",
        ("Upload Excel file", "Enter manually")
    )

    if option == "Upload Excel file":
        # File format selection
        file_format = st.radio(
            "Select file format:",
            ["Excel (.xlsx)", "CSV (.csv)"],
            horizontal=True
        )
        
        # File uploader with appropriate type
        file_type = "csv" if file_format == "CSV (.csv)" else "excel"
        file_extensions = ["csv"] if file_format == "CSV (.csv)" else ["xlsx", "xls"]
        
        uploaded_file = st.file_uploader(
            f"Choose a {file_format.split(' ')[0]} file", 
            type=file_extensions
        )
        
        # Show format demonstration table
        st.subheader("📋 Expected File Format")
        st.write("Your file should have the following structure:")
        
        # Create sample data for demonstration
        sample_data = {
            'Item': ['Pizza', 'Pasta', 'Salad', 'Drinks'],
            'amount': [20.00, 15.00, 10.00, 5.00],
            'Alice': ['✓', '✓', '', ''],
            'Bob': ['✓', '', '✓', ''],
            'Charlie': ['', '', '✓', '✓']
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)
        
        st.write("**Instructions:**")
        st.write("• **Item**: Name of the food item")
        st.write("• **amount**: Cost of the item")
        st.write("• **Person columns**: Put a checkmark (✓) or any text if the person ate that item")
        st.write("• **Empty cells**: Leave blank if the person didn't eat that item")
        
        # Download sample template
        if st.button("📥 Download Sample Template"):
            if file_format == "CSV (.csv)":
                sample_df.to_csv("sample_bill_template.csv", index=False)
                with open("sample_bill_template.csv", "r") as f:
                    st.download_button(
                        label="Download CSV Template",
                        data=f.read(),
                        file_name="sample_bill_template.csv",
                        mime="text/csv"
                    )
            else:
                sample_df.to_excel("sample_bill_template.xlsx", index=False)
                with open("sample_bill_template.xlsx", "rb") as f:
                    st.download_button(
                        label="Download Excel Template",
                        data=f.read(),
                        file_name="sample_bill_template.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        
        st.divider()
        
        tax_amount = st.number_input("Enter tax amount", min_value=0.0, format="%.2f")
        tip_amount = st.number_input("Enter tip amount", min_value=0.0, format="%.2f")
        
        if uploaded_file and tax_amount and tip_amount:
            detailed_result, simple_result, subtotal = owed_from_xl(uploaded_file, tax_amount, tip_amount, file_type)
            
            # Check if file reading was successful
            if detailed_result is not None:
                # Display total bill information
                total_bill = subtotal + tax_amount + tip_amount
                st.subheader("📊 Bill Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Subtotal", f"${subtotal:.2f}")
                with col2:
                    st.metric("Tax", f"${tax_amount:.2f}")
                with col3:
                    st.metric("Tip", f"${tip_amount:.2f}")
                with col4:
                    st.metric("Total Bill", f"${total_bill:.2f}", delta=f"+${tax_amount + tip_amount:.2f}")
                
                # Display simple summary first
                st.subheader("💰 Final Amounts Owed")
                st.json(simple_result)
                
                st.divider()
                
                # Display detailed breakdown for each person
                st.subheader("👥 Individual Breakdowns")
                for person, details in detailed_result.items():
                    with st.expander(f"📋 {person} - ${details['final_total']:.2f}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Items Eaten:**")
                            for item, cost in details['items_eaten']:
                                st.write(f"• {item}: ${cost:.2f}")
                            st.write(f"**Subtotal:** ${details['subtotal_before_tax_tip']:.2f}")
                        
                        with col2:
                            st.write("**Breakdown:**")
                            st.write(f"• Bill %: {details['percentage_of_bill']:.1f}%")
                            st.write(f"• Tax: ${details['tax_amount']:.2f}")
                            st.write(f"• Tip: ${details['tip_amount']:.2f}")
                            st.write(f"**Final Total:** ${details['final_total']:.2f}")
        else:
            st.error("Failed to read the file. Please check the format and try again.")
    
    elif option == "Enter manually":
        st.write("Enter the items, prices, and the people who ate each item.")
        st.write("💡 **Note**: Names will be automatically normalized (trimmed and title-cased).")
        
        item_count = st.number_input("How many different items?", min_value=1, step=1)
    
        items = []
        for i in range(item_count):
            item_name = st.text_input(f"Item {i+1} name")
            item_price = st.number_input(f"Item {i+1} price", min_value=0.0, format="%.2f")
            item_people_input = st.text_input(f"People who ate item {i+1} (comma-separated)")
            
            # Process the comma-separated names
            if item_people_input:
                item_people = [name.strip() for name in item_people_input.split(",") if name.strip()]
            else:
                item_people = []
                
            items.append((item_name, item_price, item_people))
        
        tax_amount = st.number_input("Enter tax amount", min_value=0.0, format="%.2f")
        tip_amount = st.number_input("Enter tip amount", min_value=0.0, format="%.2f")
        
        if st.button("Calculate"):
            if items and any(items):  # Check if items list is not empty
                detailed_result, simple_result, subtotal = money_owed(items, tax_amount, tip_amount)
                
                # Display total bill information
                total_bill = subtotal + tax_amount + tip_amount
                st.subheader("📊 Bill Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Subtotal", f"${subtotal:.2f}")
                with col2:
                    st.metric("Tax", f"${tax_amount:.2f}")
                with col3:
                    st.metric("Tip", f"${tip_amount:.2f}")
                with col4:
                    st.metric("Total Bill", f"${total_bill:.2f}", delta=f"+${tax_amount + tip_amount:.2f}")
                
                # Display simple summary first
                st.subheader("💰 Final Amounts Owed")
                st.json(simple_result)
                
                st.divider()
                
                # Display detailed breakdown for each person
                st.subheader("👥 Individual Breakdowns")
                for person, details in detailed_result.items():
                    with st.expander(f"📋 {person} - ${details['final_total']:.2f}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Items Eaten:**")
                            for item, cost in details['items_eaten']:
                                st.write(f"• {item}: ${cost:.2f}")
                            st.write(f"**Subtotal:** ${details['subtotal_before_tax_tip']:.2f}")
                        
                        with col2:
                            st.write("**Breakdown:**")
                            st.write(f"• Bill %: {details['percentage_of_bill']:.1f}%")
                            st.write(f"• Tax: ${details['tax_amount']:.2f}")
                            st.write(f"• Tip: ${details['tip_amount']:.2f}")
                            st.write(f"**Final Total:** ${details['final_total']:.2f}")
            else:
                st.error("Please enter at least one item with valid information.")

elif ui_style == "Compact UI":
    st.subheader("🚀 Compact Bill Splitter")
    st.write("Streamlined interface for quick bill splitting")
    
    # Compact file upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        file_format_compact = st.radio(
            "File Format:",
            ["Excel (.xlsx)", "CSV (.csv)"],
            horizontal=True
        )
        
        file_type_compact = "csv" if file_format_compact == "CSV (.csv)" else "excel"
        file_extensions_compact = ["csv"] if file_format_compact == "CSV (.csv)" else ["xlsx", "xls"]
        
        uploaded_file_compact = st.file_uploader(
            "Upload your bill file",
            type=file_extensions_compact
        )
    
    with col2:
        st.write("**Quick Format:**")
        st.write("Item | amount | Person1 | Person2 | ...")
        st.write("Pizza | 20.00 | ✓ | ✓ |")
        
        # Download template button
        if st.button("📥 Get Template"):
            sample_data_compact = {
                'Item': ['Pizza', 'Pasta'],
                'amount': [20.00, 15.00],
                'Alice': ['✓', '✓'],
                'Bob': ['✓', '']
            }
            sample_df_compact = pd.DataFrame(sample_data_compact)
            
            if file_format_compact == "CSV (.csv)":
                sample_df_compact.to_csv("compact_template.csv", index=False)
                with open("compact_template.csv", "r") as f:
                    st.download_button(
                        label="Download CSV",
                        data=f.read(),
                        file_name="compact_template.csv",
                        mime="text/csv"
                    )
            else:
                sample_df_compact.to_excel("compact_template.xlsx", index=False)
                with open("compact_template.xlsx", "rb") as f:
                    st.download_button(
                        label="Download Excel",
                        data=f.read(),
                        file_name="compact_template.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    # Compact input section
    col1, col2 = st.columns(2)
    
    with col1:
        tax_amount_compact = st.number_input("Tax Amount", min_value=0.0, format="%.2f")
    
    with col2:
        tip_amount_compact = st.number_input("Tip Amount", min_value=0.0, format="%.2f")
    
    # Process file or show manual entry
    if uploaded_file_compact and tax_amount_compact and tip_amount_compact:
        detailed_result_compact, simple_result_compact, subtotal_compact = owed_from_xl(
            uploaded_file_compact, tax_amount_compact, tip_amount_compact, file_type_compact
        )
        
        if detailed_result_compact is not None:
            # Compact results display
            total_bill_compact = subtotal_compact + tax_amount_compact + tip_amount_compact
            
            # Bill summary in compact cards
            st.subheader("📊 Bill Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Subtotal", f"${subtotal_compact:.2f}")
            with col2:
                st.metric("Tax", f"${tax_amount_compact:.2f}")
            with col3:
                st.metric("Tip", f"${tip_amount_compact:.2f}")
            with col4:
                st.metric("Total", f"${total_bill_compact:.2f}")
            
            # Final amounts owed (compact)
            st.subheader("💰 Final Amounts")
            st.json(simple_result_compact)
            
            # Individual breakdowns in compact format
            st.subheader("👥 Individual Breakdowns")
            for person, details in detailed_result_compact.items():
                with st.expander(f"{person} - ${details['final_total']:.2f}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Items:** {len(details['items_eaten'])}")
                        st.write(f"**Subtotal:** ${details['subtotal_before_tax_tip']:.2f}")
                    with col2:
                        st.write(f"**Bill %:** {details['percentage_of_bill']:.1f}%")
                        st.write(f"**Total:** ${details['final_total']:.2f}")
        else:
            st.error("Failed to read file. Check format and try again.")
    
    # Compact manual entry
    st.divider()
    st.subheader("✏️ Quick Manual Entry")
    
    col1, col2 = st.columns(2)
    with col1:
        item_name_compact = st.text_input("Item Name")
        item_price_compact = st.number_input("Item Price", min_value=0.0, format="%.2f")
    
    with col2:
        item_people_compact = st.text_input("People (comma-separated)")
        if st.button("Add Item"):
            if item_name_compact and item_price_compact and item_people_compact:
                # Process the item
                people_list = [name.strip() for name in item_people_compact.split(",") if name.strip()]
                if people_list:
                    st.success(f"Added: {item_name_compact} - ${item_price_compact:.2f} for {', '.join(people_list)}")
                else:
                    st.error("Please enter valid names")
            else:
                st.error("Please fill all fields")
