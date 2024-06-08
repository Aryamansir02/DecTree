# Decision Tree GUI Application

This application provides a graphical user interface (GUI) for building and using a decision tree to predict transaction outcomes.

## Features

- **Load CSV File**: Load transaction data from a CSV file.
- **Build Decision Tree**: Interactively construct a decision tree.
- **Predict Outcomes**: Use the decision tree to predict outcomes for transactions.
- **Save Results**: Save prediction results to a CSV file.

## Dependencies

- Python 3.x
- Tkinter
- Pandas

Install Pandas with:

pip install pandas

## Usage

1. Save the script to a file (e.g., `decision_tree_gui.py`).
2. Run the script using Python:

python decision_tree_gui.py


## Steps

1. **Load CSV**: Click "Load CSV File" and select your CSV file.
2. **Build Tree**: Click "Build Decision Tree" and follow prompts.
3. **Predict**: Click "Predict with Decision Tree" to generate predictions.
4. **Save Results**: Save the predictions to a CSV file when prompted.

## The CSV file should include:

- `Trans Date`
- `Description/Narration`
- `Balance INR`
- `Debit(Dr.) INR`
- `Credit(Cr.) INR`

This is because this program currently only runs for my copy of May-2024-AccStateReport - AU_760615AccStmtDownloadReport.csv, though removing the preprocessing code will enable it to run on any well formatted csv

Ensure to build the decision tree before predicting.

Working On:

- Tree display
- Dropdowns for simpledialog boxes
