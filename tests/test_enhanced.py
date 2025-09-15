#!/usr/bin/env python3
"""
Test script for the enhanced FairShare Bill Splitter functionality
"""

import sys
import os

# Add the parent directory and scripts directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Import the enhanced function from the scripts folder
from enhanced_functions import money_owed_enhanced, calculate_total_bill

def test_enhanced_functionality():
    """Test the enhanced bill splitting functionality"""
    
    # Test data
    items = [
        ("Pizza", 20, ["Alice", "Bob"]),
        ("Pasta", 15, ["Alice"]),
        ("Salad", 10, ["Bob", "Charlie"]),
        ("Drinks", 5, ["Charlie"])
    ]
    
    tax_amount = 10.97
    tip_amount = 10.73
    
    print("=== TESTING ENHANCED FAIRSHARE BILL SPLITTER ===\n")
    
    # Test the enhanced function
    try:
        detailed_result, simple_result, subtotal = money_owed_enhanced(items, tax_amount, tip_amount)
        subtotal_bill, total_bill = calculate_total_bill(items, tax_amount, tip_amount)
        
        print("✅ Enhanced function executed successfully!")
        print(f"\n📊 BILL SUMMARY:")
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
            
        # Verify calculations
        print("\n" + "="*50)
        print("🔍 VERIFICATION:")
        calculated_total = sum(simple_result.values())
        expected_total = subtotal + tax_amount + tip_amount
        print(f"Sum of individual amounts: ${calculated_total:.2f}")
        print(f"Expected total: ${expected_total:.2f}")
        print(f"Match: {'✅' if abs(calculated_total - expected_total) < 0.01 else '❌'}")
        
    except Exception as e:
        print(f"❌ Error testing enhanced functionality: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_functionality()
