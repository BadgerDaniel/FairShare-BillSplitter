# FairShare Bill Splitter 🍽️💰

A comprehensive Python application that simplifies the task of dividing restaurant bills fairly among diners. It calculates the amount owed by each person, factoring in their share of the meal cost, tax, and tip.

## ✨ Features

- **📊 Total Bill Display** - Shows subtotal, tax, tip, and final total
- **👥 Detailed Individual Breakdowns** - For each person shows:
  - Items they ate and individual costs
  - Their percentage of the bill (pre-tax/tip)
  - Tax amount based on their percentage
  - Tip amount based on their percentage
  - Final total amount owed
- **🔧 Smart Name Normalization** - Handles various input formats:
  - `"scott"` → `"Scott"`
  - `"  JOHN  "` → `"John"`
  - `"CALLIE"` → `"Callie"`
  - `"alice, bob"` → `["Alice", "Bob"]`
  - `"scott, callie"` → `["Scott", "Callie"]`
  - Automatically removes duplicates
  - Case-insensitive matching
- **📁 Multiple Input Methods** - Supports both Python dictionaries and Excel files
- **🌐 Web Interface** - Clean Streamlit GUI for easy interaction
- **📓 Jupyter Notebook** - Interactive development and testing environment

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### 1. Clone and Setup
```bash
git clone https://github.com/BadgerDaniel/FairShare-BillSplitter.git
cd FairShare-BillSplitter
```

### 2. Virtual Environment Setup

#### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Or use the provided script
.\activate_venv.ps1
```

#### Windows (Command Prompt)
```cmd
# Create virtual environment
python -m venv venv

# Activate (Command Prompt)
venv\Scripts\activate.bat

# Or use the provided script
activate_venv.bat
```

#### Linux/Mac
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install core dependencies only
pip install pandas openpyxl numpy streamlit
```

### 4. Run the Application

#### Streamlit Web App
```bash
streamlit run FairShareSplitUI1.py
```
The app will open in your browser at `http://localhost:8501`

#### Standalone Functions
```bash
python test_standalone.py
```

#### Jupyter Notebook
```bash
jupyter notebook
```

## 📁 Project Structure

```
FairShareBillSplitter/
├── venv/                          # Virtual environment
├── FairShareSplitUI1.py          # Main Streamlit application
├── enhanced_functions.py          # Standalone enhanced functions
├── BillSplitter.ipynb            # Jupyter notebook
├── ExampleExcelData-ChineseRestaurant.xlsx  # Sample data
├── requirements.txt               # Python dependencies
├── activate_venv.ps1             # PowerShell activation script
├── activate_venv.bat             # Command Prompt activation script
├── test_standalone.py            # Test script for enhanced functions
├── test_name_normalization.py    # Name normalization tests
└── README.md                     # This file
```

## 🧪 Testing

### Run All Tests
```bash
python test_standalone.py
```

### Test Name Normalization
```bash
python test_name_normalization.py
```

### Run with pytest (if installed)
```bash
pytest
```

## 💻 Development

### Code Formatting
```bash
# Format code with Black
black .

# Lint code with flake8
flake8 .
```

### Adding New Features
1. Create a feature branch
2. Implement your changes
3. Add tests
4. Update documentation
5. Submit a pull request

## 📊 Example Usage

### Python Dictionary Input
```python
from enhanced_functions import print_detailed_breakdown

items = [
    ("Pizza", 20, ["scott, callie"]),
    ("Pasta", 15, ["SCOTT", "callie"]),
    ("Salad", 10, ["john", "scott", "Callie"]),
    ("Drinks", 5, ["JOHN"])
]

tax_amount = 10.97
tip_amount = 10.73

# Get detailed breakdown
detailed_result, simple_result, subtotal = print_detailed_breakdown(items, tax_amount, tip_amount)
```

### Excel File Input
The application supports Excel files with columns:
- `Item`: Name of the food item
- `amount`: Cost of the item
- Additional columns: Names of people who ate the item

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
# Optional: Set default tax and tip percentages
DEFAULT_TAX_PERCENTAGE=8.5
DEFAULT_TIP_PERCENTAGE=18.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Original concept by [BadgerDaniel](https://github.com/BadgerDaniel)
- Enhanced with modern Python practices and improved user experience
- Built with Streamlit, Pandas, and other open-source tools

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/BadgerDaniel/FairShare-BillSplitter/issues) page
2. Create a new issue with detailed information
3. Include your Python version and operating system

---

**Happy Bill Splitting! 🎉**
