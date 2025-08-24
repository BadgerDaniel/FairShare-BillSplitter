# 📋 Excel/CSV File Format Instructions

## Required Format for FairShare Bill Splitter

Your Excel or CSV file must follow this exact structure:

### Column Requirements:
1. **Item** - Name of the food item (required)
2. **amount** - Cost of the item (required, numeric)
3. **Person columns** - One column per person (required)

### Example Structure:

| Item | amount | Alice | Bob | Charlie | David |
|------|--------|-------|-----|---------|-------|
| Pizza | 20.00 | ✓ | ✓ | | |
| Pasta | 15.00 | ✓ | | | |
| Salad | 10.00 | | ✓ | ✓ | |
| Drinks | 5.00 | | | ✓ | |
| Dessert | 12.00 | ✓ | ✓ | ✓ | ✓ |

### How to Mark Who Ate What:

- **✓** (checkmark) or **any text** = Person ate this item
- **Empty cell** = Person did NOT eat this item
- **X, Yes, 1, etc.** = Any text will work (case-insensitive)

### Important Notes:

1. **Column names are case-sensitive**: Use exactly `Item` and `amount`
2. **Person columns**: Can have any names you want
3. **Amount column**: Must contain valid numbers
4. **No empty rows**: Remove any completely empty rows
5. **File types supported**: `.xlsx`, `.xls`, `.csv`

### Tips for Creating Your File:

1. **Start with the template**: Use the provided sample file
2. **Copy and paste**: Easier than typing everything
3. **Check formatting**: Ensure amounts are numbers, not text
4. **Save properly**: Use the correct file extension
5. **Test with small data**: Try with 2-3 items first

### Common Mistakes to Avoid:

- ❌ Missing `Item` or `amount` columns
- ❌ Using different column names
- ❌ Empty `Item` or `amount` cells
- ❌ Text in the `amount` column
- ❌ Special characters in column names

### Example Valid Entries:

```
Item: "Margherita Pizza", "Chicken Pasta", "Caesar Salad"
amount: 18.50, 16.75, 12.00
Person columns: "John", "Jane", "Mike", "Sarah"
```

### Download Templates:

- **CSV Template**: `sample_bill_template.csv`
- **Excel Template**: Available in the app (click "Download Sample Template")

---

**Need Help?** If you're having trouble, try the sample template first, then gradually add your own data!
