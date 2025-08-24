@echo off
echo Activating FairShare Bill Splitter Virtual Environment...
echo.
call "venv\Scripts\activate.bat"
echo.
echo Virtual environment activated! You can now:
echo - Run the Streamlit app: streamlit run FairShareSplitUI1.py
echo - Run tests: python test_standalone.py
echo - Install packages: pip install package_name
echo.
echo To deactivate, type: deactivate
echo.
cmd /k
