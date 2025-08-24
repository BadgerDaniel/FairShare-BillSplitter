# Fair Share Bill Splitter

A comprehensive bill splitting application that fairly calculates how much each person owes based on what they actually consumed, including detailed breakdowns of tax and tip portions.

## ✨ New Features

### 1. Total Bill Summary
- **Pre-Tax & Tip Total**: Shows the combined cost of all food items
- **Tax Amount**: Total tax on the bill
- **Tip Amount**: Total tip amount
- **Total Bill**: Everything combined (food + tax + tip)

### 2. Per-Person Detailed Breakdown
For each person, the app now shows:

#### 🍽️ Items Consumed
- **Item Name**: What they ate
- **Total Cost**: Full price of the item
- **Your Portion**: Their share of the cost (if split)
- **Details**: Shows who else shared the item (if applicable)

#### 📊 Cost Breakdown
- **Food Cost**: Total cost of their food items
- **Bill Percentage**: What percentage of the total bill they generated
- **Tax Portion**: Their calculated share of the tax
- **Tip Portion**: Their calculated share of the tip

#### 🧮 Final Calculation
- **Food**: Base food cost
- **Tax**: Their portion of tax (based on their bill percentage)
- **Tip**: Their portion of tip (based on their bill percentage)
- **Total**: Final amount they owe

## 🚀 How to Use

### Option 1: Upload Excel File
1. Prepare an Excel file with columns:
   - First column: `Item` (item names)
   - Second column: `amount` (prices)
   - Subsequent columns: Person names (mark with any value like 'X' if they consumed that item)
2. Upload the file
3. Enter tax and tip amounts
4. View detailed breakdown

### Option 2: Manual Input
1. Enter the number of items
2. For each item, specify:
   - Item name
   - Price
   - People who consumed it (comma-separated)
3. Enter tax and tip amounts
4. Click Calculate to see results

## 💡 Example

**Sample Bill:**
- Pizza: $20.00 (shared by Alice & Bob)
- Pasta: $15.00 (Alice only)
- Salad: $10.00 (shared by Bob & Charlie)
- Drinks: $5.00 (Charlie only)
- Tax: $10.97
- Tip: $10.73

**Results:**
- **Total Bill**: $71.70
- **Alice**: $35.85 (50% of bill, highest spender)
- **Bob**: $21.51 (30% of bill, medium spender)
- **Charlie**: $14.34 (20% of bill, lowest spender)

## 🔧 Technical Details

The app calculates:
1. **Individual food costs** by splitting shared items equally
2. **Bill percentages** based on each person's food cost relative to total
3. **Tax portions** by applying each person's percentage to the total tax
4. **Tip portions** by applying each person's percentage to the total tip
5. **Final amounts** by summing food + tax portion + tip portion

## 📱 Running the App

```bash
streamlit run FairShareSplitUI1.py
```

## 🎯 Use Cases

- **Restaurant bills** with shared appetizers and individual entrees
- **Group dining** where people order different items
- **Business lunches** with expense tracking
- **Any situation** where you need to split costs fairly based on consumption

## ✨ Benefits

- **Fair splitting**: Each person pays for what they actually consumed
- **Transparency**: Clear breakdown of how amounts are calculated
- **Accuracy**: Handles shared items, tax, and tips proportionally
- **User-friendly**: Both Excel upload and manual input options
- **Detailed reporting**: Complete visibility into cost allocation