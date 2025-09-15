# FairShare Bill Splitter 🍽️💰

A comprehensive Python application that simplifies the task of dividing restaurant bills fairly among diners.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### 1. Setup Virtual Environment

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

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run FairShareSplitUI1.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
FairShareBillSplitter/
├── FairShareSplitUI1.py          # Main Streamlit application
├── requirements.txt               # Python dependencies
├── activate_venv.bat             # Windows CMD activation script
├── activate_venv.ps1             # PowerShell activation script
├── docs/                         # Documentation
│   ├── README.md                 # Detailed documentation
│   ├── sample_bill_template_instructions.md
│   └── BillSplitter_Enhanced.md
├── notebooks/                    # Jupyter notebooks
│   ├── BillSplitter.ipynb
│   └── BillSplitter_Enhanced.ipynb
├── tests/                        # Test files
│   ├── test_enhanced.py
│   ├── test_name_normalization.py
│   └── test_standalone.py
├── data/                         # Sample data files
│   ├── ExampleExcelData-ChineseRestaurant.xlsx
│   ├── sample_bill_template.csv
│   └── BillSplitter.pdf
├── scripts/                      # Additional Python scripts
│   ├── enhanced_functions.py
│   └── FairShareSplitUI1_Enhanced.py
└── venv/                         # Virtual environment
```

## 🧪 Testing

### Run All Tests
```bash
python tests/test_standalone.py
python tests/test_name_normalization.py
python tests/test_enhanced.py
```

## 📖 Documentation

For detailed documentation, see the [docs/README.md](docs/README.md) file.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Happy Bill Splitting! 🎉**
