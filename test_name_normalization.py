#!/usr/bin/env python3
"""
Test script to demonstrate the new name normalization functionality
Shows how different name formats are handled consistently
"""

from enhanced_functions import print_detailed_breakdown

def test_name_normalization():
    """Test various name input formats to show normalization"""
    
    print("=== TESTING NAME NORMALIZATION ===\n")
    
    # Test different name formats
    test_cases = [
        # Test case 1: Mixed case and spacing
        ("Mixed Case Test", [
            ("Pizza", 20, ["scott", "CALLIE", "  John  "]),
            ("Pasta", 15, ["SCOTT", "callie"]),
            ("Salad", 10, ["john", "scott", "Callie"]),
            ("Drinks", 5, ["JOHN"])
        ]),
        
        # Test case 2: Comma-separated with spaces
        ("Comma Separated Test", [
            ("Burger", 18, ["alice, bob", "charlie, david"]),
            ("Fries", 8, ["alice", "bob, charlie"]),
            ("Soda", 4, ["david, alice"])
        ]),
        
        # Test case 3: Mixed formats
        ("Mixed Format Test", [
            ("Steak", 25, ["  MARY  ", "john", "MARY", "JOHN"]),
            ("Wine", 30, ["mary", "john", "mary, john"]),
            ("Dessert", 12, ["MARY", "JOHN"])
        ])
    ]
    
    tax_amount = 8.50
    tip_amount = 12.00
    
    for test_name, items in test_cases:
        print(f"\n{'='*60}")
        print(f"🧪 {test_name}")
        print(f"{'='*60}")
        
        # Show original input
        print("\n📝 Original Input:")
        for item, cost, names in items:
            print(f"   {item}: ${cost:.2f} - {names}")
        
        # Show normalized names
        print("\n✨ Normalized Names:")
        from enhanced_functions import normalize_names_list
        for item, cost, names in items:
            normalized = normalize_names_list(names)
            print(f"   {item}: {normalized}")
        
        # Calculate and show results
        print(f"\n📊 Results for {test_name}:")
        try:
            detailed_result, simple_result, subtotal = print_detailed_breakdown(items, tax_amount, tip_amount)
            
            # Show summary of unique people
            unique_people = list(simple_result.keys())
            print(f"\n👥 Unique People Found: {', '.join(unique_people)}")
            print(f"Total People: {len(unique_people)}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "-"*60)

def main():
    """Run the name normalization tests"""
    print("Testing Enhanced FairShare Bill Splitter - Name Normalization")
    print("=" * 70)
    print("This test demonstrates how different name formats are handled:")
    print("• 'scott' → 'Scott'")
    print("• '  JOHN  ' → 'John'")
    print("• 'CALLIE' → 'Callie'")
    print("• 'alice, bob' → ['Alice', 'Bob']")
    print("• Duplicates are automatically removed")
    print("=" * 70)
    
    test_name_normalization()
    
    print("\n✅ All name normalization tests completed!")
    print("\n💡 Key Benefits:")
    print("• No more errors from case sensitivity")
    print("• Consistent name formatting")
    print("• Automatic duplicate removal")
    print("• Flexible input formats")

if __name__ == "__main__":
    main()
