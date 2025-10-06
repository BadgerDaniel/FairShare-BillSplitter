import streamlit as st
import pandas as pd
import copy
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

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

def format_item_display(item_name, cost, num_people_shared):
    """
    Format item display to show fractional portions when shared
    
    Args:
        item_name: Name of the item
        cost: Individual cost for this person
        num_people_shared: Number of people who shared this item
    
    Returns:
        Formatted string showing the item with fractional portion
    """
    if num_people_shared == 1:
        return f"{item_name}: ${cost:.2f}"
    else:
        # Create fraction string
        fraction_str = f"{1}/{num_people_shared}"
        return f"{fraction_str} of {item_name}: ${cost:.2f}"

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

def money_owed(items, tax_amount, tip_amount, extra_fees=0.0, discount_amount=0.0):
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
            # Track what each person ate and their individual costs, including how many people shared the item
            person_items[name].append((item, split_cost_of_item, len(normalized_names)))
            person_individual_costs[name] += split_cost_of_item

    total_tax_tip_fees = tax_amount + tip_amount + extra_fees

    for person in person_dict_percent_of_bill.keys():
        person_dict_percent_of_bill[person] = person_dict[person] / running_total_preTaxTip

    for person in person_dict:
        person_tip_to_pay = person_dict_percent_of_bill[person] * tip_amount
        person_tax_to_pay = person_dict_percent_of_bill[person] * tax_amount
        person_extra_fees_to_pay = person_dict_percent_of_bill[person] * extra_fees
        person_discount_to_apply = person_dict_percent_of_bill[person] * discount_amount
        person_tax_tip_fees_to_pay = person_tax_to_pay + person_tip_to_pay + person_extra_fees_to_pay
        person_final_total = person_tax_tip_fees_to_pay + person_dict[person] - person_discount_to_apply
        person_dict_final[person] = round(person_final_total, 2)

    # New: Return detailed breakdown
    detailed_results = {}
    for person in person_list:
        person_percentage = person_dict_percent_of_bill[person]
        person_tax = person_dict_percent_of_bill[person] * tax_amount
        person_tip = person_dict_percent_of_bill[person] * tip_amount
        
        person_extra_fees = person_dict_percent_of_bill[person] * extra_fees
        person_discount = person_dict_percent_of_bill[person] * discount_amount
        
        detailed_results[person] = {
            'items_eaten': person_items[person],
            'subtotal_before_tax_tip': round(person_individual_costs[person], 2),
            'percentage_of_bill': round(person_percentage * 100, 2),
            'tax_amount': round(person_tax, 2),
            'tip_amount': round(person_tip, 2),
            'extra_fees_amount': round(person_extra_fees, 2),
            'discount_amount': round(person_discount, 2),
            'final_total': round(person_dict_final[person], 2)
        }

    return detailed_results, person_dict_final, running_total_preTaxTip

def calculate_total_bill(items, tax_amount, tip_amount, extra_fees=0.0, discount_amount=0.0):
    """Calculate the total bill amount including tax, tip, extra fees, and discount"""
    subtotal = sum(cost for _, cost, _ in items)
    total = subtotal + tax_amount + tip_amount + extra_fees - discount_amount
    return subtotal, total

def owed_from_xl(filepath, tax_amount, tip_amount, file_type="excel", extra_fees=0.0, discount_amount=0.0):
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
            # Determine number of servings per person column
            consumers = []
            for col in df.columns[2:]:
                val = row[col]
                if pd.isnull(val):
                    continue
                try:
                    count = int(val)
                except:
                    # non-numeric (e.g., ✓), treat as one serving
                    count = 1
                consumers.extend([col] * count)
            items.append((item_name, item_cost, consumers))

        return money_owed(items, tax_amount, tip_amount, extra_fees, discount_amount)
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None, None, None

def generate_text_export(simple_breakdown, detailed_breakdowns, totals):
    """Generate a text export of the bill breakdown"""
    text_content = []
    text_content.append("=" * 60)
    text_content.append("FAIR SHARE BILL SPLITTER - BREAKDOWN")
    text_content.append("=" * 60)
    text_content.append("")
    
    # Simple breakdown
    text_content.append("SIMPLE BREAKDOWN:")
    text_content.append("-" * 30)
    for person, amount in simple_breakdown.items():
        text_content.append(f"{person}: ${amount:.2f}")
    text_content.append("")
    
    # Totals
    text_content.append("TOTALS:")
    text_content.append("-" * 30)
    text_content.append(f"Subtotal: ${totals['subtotal']:.2f}")
    text_content.append(f"Tax: ${totals['tax']:.2f}")
    text_content.append(f"Tip: ${totals['tip']:.2f}")
    text_content.append(f"Extra Fees: ${totals['extra_fees']:.2f}")
    text_content.append(f"TOTAL: ${totals['total']:.2f}")
    text_content.append("")
    
    # Detailed breakdowns
    text_content.append("DETAILED BREAKDOWN:")
    text_content.append("-" * 30)
    for person, details in detailed_breakdowns.items():
        text_content.append(f"\n{person.upper()}:")
        # Extract item names from the items_eaten list of tuples
        item_names = [item[0] for item in details['items_eaten']]
        text_content.append(f"  Items: {', '.join(item_names)}")
        text_content.append(f"  Item Total: ${details['subtotal_before_tax_tip']:.2f}")
        text_content.append(f"  Bill %: {details['percentage_of_bill']:.1f}%")
        text_content.append(f"  Tax: ${details['tax_amount']:.2f}")
        text_content.append(f"  Tip: ${details['tip_amount']:.2f}")
        text_content.append(f"  Extra Fees: ${details['extra_fees_amount']:.2f}")
        text_content.append(f"  FINAL TOTAL: ${details['final_total']:.2f}")
    
    return "\n".join(text_content)

def generate_pdf_export(simple_breakdown, detailed_breakdowns, totals):
    """Generate a PDF export of the bill breakdown"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("FAIR SHARE BILL SPLITTER", title_style))
    story.append(Paragraph("Bill Breakdown Report", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    # Simple breakdown table
    story.append(Paragraph("Simple Breakdown", styles['Heading3']))
    simple_data = [["Person", "Amount Owed"]]
    for person, amount in simple_breakdown.items():
        simple_data.append([person, f"${amount:.2f}"])
    
    simple_table = Table(simple_data)
    simple_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(simple_table)
    story.append(Spacer(1, 20))
    
    # Totals
    story.append(Paragraph("Totals", styles['Heading3']))
    totals_data = [
        ["Subtotal", f"${totals['subtotal']:.2f}"],
        ["Tax", f"${totals['tax']:.2f}"],
        ["Tip", f"${totals['tip']:.2f}"],
        ["Extra Fees", f"${totals['extra_fees']:.2f}"],
        ["TOTAL", f"${totals['total']:.2f}"]
    ]
    
    totals_table = Table(totals_data)
    totals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 4), (-1, 4), colors.darkblue),
        ('TEXTCOLOR', (0, 4), (-1, 4), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 4), (-1, 4), 14),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 20))
    
    # Detailed breakdowns
    story.append(Paragraph("Detailed Breakdown", styles['Heading3']))
    for person, details in detailed_breakdowns.items():
        story.append(Paragraph(f"<b>{person}</b>", styles['Heading4']))
        # Extract item names from the items_eaten list of tuples
        item_names = [item[0] for item in details['items_eaten']]
        story.append(Paragraph(f"Items: {', '.join(item_names)}", styles['Normal']))
        story.append(Paragraph(f"Item Total: ${details['subtotal_before_tax_tip']:.2f}", styles['Normal']))
        story.append(Paragraph(f"Bill %: {details['percentage_of_bill']:.1f}%", styles['Normal']))
        story.append(Paragraph(f"Tax: ${details['tax_amount']:.2f}", styles['Normal']))
        story.append(Paragraph(f"Tip: ${details['tip_amount']:.2f}", styles['Normal']))
        story.append(Paragraph(f"Extra Fees: ${details['extra_fees_amount']:.2f}", styles['Normal']))
        story.append(Paragraph(f"<b>Final Total: ${details['final_total']:.2f}</b>", styles['Normal']))
        story.append(Spacer(1, 10))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

st.title("Fair Share Bill Splitter")

# UI Style Selector
ui_style = st.radio(
    "Choose UI Style:",
    ["Classic UI", "Compact UI"],
    help="Classic UI: Full-featured with detailed breakdowns. Compact UI: Streamlined and easier to navigate.",
    horizontal=True
)

# Add info about name normalization
st.info("💡 **Tip**: Names are automatically trimmed and normalized. 'scott, callie' and 'Scott,Callie' will both become 'Scott' and 'Callie'.")

if ui_style == "Classic UI":
    option = st.radio(
        "How would you like to input the bill details?",
        ("Enter manually", "Upload Excel file"),
        horizontal=True
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
        st.write("• **Person columns**: Enter the number of servings eaten (e.g., 2 for two servings). Non-numeric entries count as one serving.")
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
        
        tax_amount = st.number_input("Enter tax amount", min_value=0.0, format="%.2f", key="classic_excel_tax")
        tip_amount = st.number_input("Enter tip amount", min_value=0.0, format="%.2f", key="classic_excel_tip")
        extra_fees = st.number_input("Enter extra fees/surcharges", min_value=0.0, format="%.2f", key="classic_excel_extra_fees")
        
        if uploaded_file and tax_amount and tip_amount:
            detailed_result, simple_result, subtotal = owed_from_xl(uploaded_file, tax_amount, tip_amount, file_type, extra_fees)
            
            # Check if file reading was successful
            if detailed_result is not None:
                # Display total bill information
                total_bill = subtotal + tax_amount + tip_amount + extra_fees
                st.subheader("📊 Bill Summary")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Subtotal", f"${subtotal:.2f}")
                with col2:
                    st.metric("Tax", f"${tax_amount:.2f}")
                with col3:
                    st.metric("Tip", f"${tip_amount:.2f}")
                with col4:
                    st.metric("Extra Fees", f"${extra_fees:.2f}")
                with col5:
                    st.metric("Total Bill", f"${total_bill:.2f}", delta=f"+${tax_amount + tip_amount + extra_fees:.2f}")
                
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
                            for item_data in details['items_eaten']:
                                if len(item_data) == 3:  # New format with num_people_shared
                                    item, cost, num_people_shared = item_data
                                    formatted_item = format_item_display(item, cost, num_people_shared)
                                else:  # Old format for backward compatibility
                                    item, cost = item_data
                                    formatted_item = f"{item}: ${cost:.2f}"
                                st.write(f"• {formatted_item}")
                            st.write(f"**Subtotal:** ${details['subtotal_before_tax_tip']:.2f}")
                        
                        with col2:
                            st.write("**Cost Breakdown:**")
                            st.write(f"• Items Subtotal: ${details['subtotal_before_tax_tip']:.2f}")
                            st.write(f"• Bill Percentage: {details['percentage_of_bill']:.1f}%")
                            st.write(f"• Tax ({details['percentage_of_bill']:.1f}%): ${details['tax_amount']:.2f}")
                            st.write(f"• Tip ({details['percentage_of_bill']:.1f}%): ${details['tip_amount']:.2f}")
                            st.write(f"• Extra Fees ({details['percentage_of_bill']:.1f}%): ${details['extra_fees_amount']:.2f}")
                            if details.get('discount_amount', 0) > 0:
                                st.write(f"• Discount ({details['percentage_of_bill']:.1f}%): -${details['discount_amount']:.2f}")
                            st.write(f"**Final Total:** ${details['final_total']:.2f}")
                
                # Export buttons for Excel results
                st.divider()
                st.subheader("📤 Export Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Prepare totals for export
                    totals_excel = {
                        'subtotal': subtotal,
                        'tax': tax_amount,
                        'tip': tip_amount,
                        'extra_fees': extra_fees,
                        'total': total_bill
                    }
                    
                    # Generate text export
                    text_content_excel = generate_text_export(simple_result, detailed_result, totals_excel)
                    st.download_button(
                        label="📄 Download Text Report",
                        data=text_content_excel,
                        file_name="bill_breakdown_excel.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    # Generate PDF export
                    pdf_content_excel = generate_pdf_export(simple_result, detailed_result, totals_excel)
                    st.download_button(
                        label="📋 Download PDF Report",
                        data=pdf_content_excel,
                        file_name="bill_breakdown_excel.pdf",
                        mime="application/pdf"
                    )
        else:
            st.error("Failed to read the file. Please check the format and try again.")
    
    elif option == "Enter manually":
        st.write("Enter the items, prices, and the people who ate each item.")
        st.write("💡 **Note**: Names will be automatically normalized (trimmed and title-cased).")
        st.write("🍽️ **Multiple Servings**: To indicate someone ate multiple servings, repeat their name (e.g., 'Alice, Alice' for 2 servings).")
        
        item_count = st.number_input("How many different items?", min_value=1, step=1, key="classic_manual_item_count")
    
        items = []
        for i in range(item_count):
            st.subheader(f"Item {i+1}")
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                item_name = st.text_input(f"Item name", key=f"classic_manual_item_name_{i}", placeholder="e.g., Pizza")
            
            with col2:
                item_price = st.number_input(f"Price", min_value=0.0, format="%.2f", key=f"classic_manual_item_price_{i}")
            
            with col3:
                item_people_input = st.text_input(f"People who ate this item (comma-separated)", key=f"classic_manual_item_people_{i}", placeholder="e.g., Alice, Bob or Alice, Alice for 2 servings")
            
            # Process the comma-separated names
            if item_people_input:
                item_people = [name.strip() for name in item_people_input.split(",") if name.strip()]
            else:
                item_people = []
                
            items.append((item_name, item_price, item_people))
            
            # Add a small divider between items (except for the last one)
            if i < item_count - 1:
                st.divider()
        
        st.divider()
        st.subheader("💰 Additional Charges")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            tax_amount = st.number_input("Tax Amount", min_value=0.0, format="%.2f", key="classic_manual_tax")
        with col2:
            tip_amount = st.number_input("Tip Amount", min_value=0.0, format="%.2f", key="classic_manual_tip")
        with col3:
            extra_fees = st.number_input("Extra Fees/Surcharges", min_value=0.0, format="%.2f", key="classic_manual_extra_fees")
        with col4:
            discount_amount = st.number_input("Discount/Coupon Amount", min_value=0.0, format="%.2f", key="classic_manual_discount")
        
        if st.button("Calculate"):
            if items and any(items):  # Check if items list is not empty
                detailed_result, simple_result, subtotal = money_owed(items, tax_amount, tip_amount, extra_fees, discount_amount)
                
                # Display total bill information
                total_bill = subtotal + tax_amount + tip_amount + extra_fees - discount_amount
                st.subheader("📊 Bill Summary")
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    st.metric("Subtotal", f"${subtotal:.2f}")
                with col2:
                    st.metric("Tax", f"${tax_amount:.2f}")
                with col3:
                    st.metric("Tip", f"${tip_amount:.2f}")
                with col4:
                    st.metric("Extra Fees", f"${extra_fees:.2f}")
                with col5:
                    st.metric("Discount", f"-${discount_amount:.2f}", delta=f"-${discount_amount:.2f}")
                with col6:
                    st.metric("Total Bill", f"${total_bill:.2f}", delta=f"+${tax_amount + tip_amount + extra_fees - discount_amount:.2f}")
                
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
                            for item_data in details['items_eaten']:
                                if len(item_data) == 3:  # New format with num_people_shared
                                    item, cost, num_people_shared = item_data
                                    formatted_item = format_item_display(item, cost, num_people_shared)
                                else:  # Old format for backward compatibility
                                    item, cost = item_data
                                    formatted_item = f"{item}: ${cost:.2f}"
                                st.write(f"• {formatted_item}")
                            st.write(f"**Subtotal:** ${details['subtotal_before_tax_tip']:.2f}")
                        
                        with col2:
                            st.write("**Cost Breakdown:**")
                            st.write(f"• Items Subtotal: ${details['subtotal_before_tax_tip']:.2f}")
                            st.write(f"• Bill Percentage: {details['percentage_of_bill']:.1f}%")
                            st.write(f"• Tax ({details['percentage_of_bill']:.1f}%): ${details['tax_amount']:.2f}")
                            st.write(f"• Tip ({details['percentage_of_bill']:.1f}%): ${details['tip_amount']:.2f}")
                            st.write(f"• Extra Fees ({details['percentage_of_bill']:.1f}%): ${details['extra_fees_amount']:.2f}")
                            if details.get('discount_amount', 0) > 0:
                                st.write(f"• Discount ({details['percentage_of_bill']:.1f}%): -${details['discount_amount']:.2f}")
                            st.write(f"**Final Total:** ${details['final_total']:.2f}")
                
                # Export buttons
                st.divider()
                st.subheader("📤 Export Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Prepare totals for export
                    totals = {
                        'subtotal': subtotal,
                        'tax': tax_amount,
                        'tip': tip_amount,
                        'extra_fees': extra_fees,
                        'total': total_bill
                    }
                    
                    # Generate text export
                    text_content = generate_text_export(simple_result, detailed_result, totals)
                    st.download_button(
                        label="📄 Download Text Report",
                        data=text_content,
                        file_name="bill_breakdown.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    # Generate PDF export
                    pdf_content = generate_pdf_export(simple_result, detailed_result, totals)
                    st.download_button(
                        label="📋 Download PDF Report",
                        data=pdf_content,
                        file_name="bill_breakdown.pdf",
                        mime="application/pdf"
                    )
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
        tax_amount_compact = st.number_input("Tax Amount", min_value=0.0, format="%.2f", key="compact_tax")
    
    with col2:
        tip_amount_compact = st.number_input("Tip Amount", min_value=0.0, format="%.2f", key="compact_tip")
    
    extra_fees_compact = st.number_input("Extra Fees/Surcharges", min_value=0.0, format="%.2f", key="compact_extra_fees")
    
    discount_amount_compact = st.number_input("Discount/Coupon Amount", min_value=0.0, format="%.2f", key="compact_discount")
    
    # Process file or show manual entry
    if uploaded_file_compact and tax_amount_compact and tip_amount_compact:
        detailed_result_compact, simple_result_compact, subtotal_compact = owed_from_xl(
            uploaded_file_compact, tax_amount_compact, tip_amount_compact, file_type_compact, extra_fees_compact, discount_amount_compact
        )
        
        if detailed_result_compact is not None:
            # Compact results display
            total_bill_compact = subtotal_compact + tax_amount_compact + tip_amount_compact + extra_fees_compact - discount_amount_compact
            
            # Bill summary in compact cards
            st.subheader("📊 Bill Summary")
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.metric("Subtotal", f"${subtotal_compact:.2f}")
            with col2:
                st.metric("Tax", f"${tax_amount_compact:.2f}")
            with col3:
                st.metric("Tip", f"${tip_amount_compact:.2f}")
            with col4:
                st.metric("Extra Fees", f"${extra_fees_compact:.2f}")
            with col5:
                st.metric("Discount", f"-${discount_amount_compact:.2f}")
            with col6:
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
    # Initialize manual compact items list
    if 'compact_items' not in st.session_state:
        st.session_state['compact_items'] = []

    st.divider()
    st.subheader("✏️ Quick Manual Entry")

    st.write("**Add Items One by One:**")
    st.write("🍽️ **Multiple Servings**: To indicate someone ate multiple servings, repeat their name (e.g., 'Alice, Alice' for 2 servings).")
    col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
    
    with col1:
        item_name_compact = st.text_input("Item Name", key="compact_manual_item_name", placeholder="e.g., Pizza")
    
    with col2:
        item_price_compact = st.number_input("Price", min_value=0.0, format="%.2f", key="compact_manual_item_price")
    
    with col3:
        item_people_compact = st.text_input("People (comma-separated)", key="compact_manual_item_people", placeholder="e.g., Alice, Bob or Alice, Alice for 2 servings")
    
    with col4:
        st.write("")  # Empty space for alignment
        if st.button("Add Item", type="primary"):
            if item_name_compact and item_price_compact and item_people_compact:
                # Process the item
                people_list = [name.strip() for name in item_people_compact.split(",") if name.strip()]
                if people_list:
                    st.session_state['compact_items'].append((item_name_compact, item_price_compact, people_list))
                    st.success(f"Added: {item_name_compact} - ${item_price_compact:.2f} for {', '.join(people_list)}")
                else:
                    st.error("Please enter valid names")
            else:
                st.error("Please fill all fields")

# Display running list of items if any
if 'compact_items' in st.session_state and st.session_state['compact_items']:
    st.subheader("📋 Items Entered (Compact Manual)")
    df_items = pd.DataFrame([
        {"Item": name, "Price": price, "People": ", ".join(people)}
        for name, price, people in st.session_state['compact_items']
    ])
    st.dataframe(df_items, use_container_width=True)

# Calculate Bill button for manual compact items
if st.button("Calculate Bill (Compact)"):
    if 'compact_items' in st.session_state and st.session_state['compact_items']:
        detailed_result_compact_manual, simple_result_compact_manual, subtotal_compact_manual = money_owed(
            st.session_state['compact_items'], tax_amount_compact, tip_amount_compact, extra_fees_compact, discount_amount_compact
        )
        total_bill_compact_manual = subtotal_compact_manual + tax_amount_compact + tip_amount_compact + extra_fees_compact - discount_amount_compact
        st.subheader("📊 Compact Manual Bill Summary")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.metric("Subtotal", f"${subtotal_compact_manual:.2f}")
        with col2:
            st.metric("Tax", f"${tax_amount_compact:.2f}")
        with col3:
            st.metric("Tip", f"${tip_amount_compact:.2f}")
        with col4:
            st.metric("Extra Fees", f"${extra_fees_compact:.2f}")
        with col5:
            st.metric("Discount", f"-${discount_amount_compact:.2f}")
        with col6:
            st.metric("Total", f"${total_bill_compact_manual:.2f}")
        st.subheader("💰 Final Amounts (Compact Manual)")
        st.json(simple_result_compact_manual)
        st.subheader("👥 Individual Breakdowns (Compact Manual)")
        for person, details in detailed_result_compact_manual.items():
            with st.expander(f"{person} - ${details['final_total']:.2f}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Items:** {len(details['items_eaten'])}")
                    st.write(f"**Subtotal:** ${details['subtotal_before_tax_tip']:.2f}")
                with col2:
                    st.write(f"**Bill %:** {details['percentage_of_bill']:.1f}%")
                    st.write(f"**Total:** ${details['final_total']:.2f}")
        
        # Export buttons for Compact UI
        st.divider()
        st.subheader("📤 Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            # Prepare totals for export
            totals_compact = {
                'subtotal': subtotal_compact_manual,
                'tax': tax_amount_compact,
                'tip': tip_amount_compact,
                'extra_fees': extra_fees_compact,
                'total': total_bill_compact_manual
            }
            
            # Generate text export
            text_content_compact = generate_text_export(simple_result_compact_manual, detailed_result_compact_manual, totals_compact)
            st.download_button(
                label="📄 Download Text Report",
                data=text_content_compact,
                file_name="bill_breakdown_compact.txt",
                mime="text/plain"
            )
        
        with col2:
            # Generate PDF export
            pdf_content_compact = generate_pdf_export(simple_result_compact_manual, detailed_result_compact_manual, totals_compact)
            st.download_button(
                label="📋 Download PDF Report",
                data=pdf_content_compact,
                file_name="bill_breakdown_compact.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Please add some items before calculating the bill.")
