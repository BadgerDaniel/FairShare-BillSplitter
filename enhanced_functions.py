#!/usr/bin/env python3
"""
Enhanced FairShare Bill Splitter Functions
Standalone module with enhanced functionality for detailed bill breakdowns
"""

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

def money_owed_enhanced(items, tax_amount, tip_amount):
    """
    Enhanced function that returns detailed breakdown for each person
    
    Args:
        items: List of tuples (item_name, cost, [people_who_ate_it])
        tax_amount: Total tax amount
        tip_amount: Total tip amount
    
    Returns:
        tuple: (detailed_results, simple_result, running_total_preTaxTip)
    """
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
    
    # Track items each person ate
    person_items = {person: [] for person in person_list}
    
    # Track individual costs for each person
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

    # Return detailed breakdown
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
    """
    Calculate the total bill amount including tax and tip
    
    Args:
        items: List of tuples (item_name, cost, [people_who_ate_it])
        tax_amount: Total tax amount
        tip_amount: Total tip amount
    
    Returns:
        tuple: (subtotal, total)
    """
    subtotal = sum(cost for _, cost, _ in items)
    total = subtotal + tax_amount + tip_amount
    return subtotal, total

def print_detailed_breakdown(items, tax_amount, tip_amount):
    """
    Print a detailed breakdown of the bill splitting
    
    Args:
        items: List of tuples (item_name, cost, [people_who_ate_it])
        tax_amount: Total tax amount
        tip_amount: Total tip amount
    """
    detailed_result, simple_result, subtotal = money_owed_enhanced(items, tax_amount, tip_amount)
    subtotal_bill, total_bill = calculate_total_bill(items, tax_amount, tip_amount)
    
    print("=== ENHANCED BILL SPLITTING RESULTS ===\n")
    
    print(f"📊 BILL SUMMARY:")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax: ${tax_amount:.2f}")
    print(f"Tip: ${tip_amount:.2f}")
    print(f"Total Bill: ${total_bill:.2f}")
    print(f"Tax + Tip: ${tax_amount + tip_amount:.2f}")
    print("\n" + "="*50 + "\n")
    
    print("👥 INDIVIDUAL BREAKDOWNS:")
    for person, details in detailed_result.items():
        print(f"\n📋 {person} - ${details['final_total']:.2f}")
        print(f"   Items eaten:")
        for item, cost in details['items_eaten']:
            print(f"   • {item}: ${cost:.2f}")
        print(f"   Subtotal: ${details['subtotal_before_tax_tip']:.2f}")
        print(f"   Bill %: {details['percentage_of_bill']:.1f}%")
        print(f"   Tax: ${details['tax_amount']:.2f}")
        print(f"   Tip: ${details['tip_amount']:.2f}")
        print(f"   Final Total: ${details['final_total']:.2f}")
        print("-" * 30)
    
    print("\n" + "="*50 + "\n")
    print("💰 FINAL AMOUNTS OWED:")
    for person, amount in simple_result.items():
        print(f"{person}: ${amount:.2f}")
    
    # Verification
    print("\n" + "="*50)
    print("🔍 VERIFICATION:")
    calculated_total = sum(simple_result.values())
    expected_total = subtotal + tax_amount + tip_amount
    print(f"Sum of individual amounts: ${calculated_total:.2f}")
    print(f"Expected total: ${expected_total:.2f}")
    print(f"Match: {'✅' if abs(calculated_total - expected_total) < 0.01 else '❌'}")
    
    return detailed_result, simple_result, subtotal
