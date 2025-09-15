#!/usr/bin/env python3
"""
Test script for the standalone enhanced FairShare Bill Splitter functions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from enhanced_functions import print_detailed_breakdown

def main():
    """Test the enhanced functionality with sample data"""
    
    # Sample restaurant bill data
    items = [
        ("Pizza", 20, ["Alice", "Bob"]),
        ("Pasta", 15, ["Alice"]),
        ("Salad", 10, ["Bob", "Charlie"]),
        ("Drinks", 5, ["Charlie"])
    ]
    
    tax_amount = 10.97
    tip_amount = 10.73
    
    print("Testing Enhanced FairShare Bill Splitter")
    print("=" * 50)
    
    # Test the enhanced functionality
    try:
        detailed_result, simple_result, subtotal = print_detailed_breakdown(items, tax_amount, tip_amount)
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
