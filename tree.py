import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import pandas as pd
from treelib import Tree

class TreeNode:
    def __init__(self, attribute=None, value=None, condition=None, left=None, right=None, result=None, path=""):
        self.attribute = attribute
        self.value = value
        self.condition = condition
        self.left = left
        self.right = right
        self.result = result
        self.path = path

    def is_leaf(self):
        return self.result is not None

class DecisionTree:
    def __init__(self):
        self.root = None
        self.node_counter = 0

    def build_tree(self, gui):
        self.root = self._build_tree_recursively(gui, "", 0)

    def _build_tree_recursively(self, gui, path, num):
        current_path.set(path)
        gui.update_idletasks()
        attribute = simpledialog.askstring("Input", f"Enter attribute to split on (or 'result' to mark as leaf): ", parent=gui)
        if attribute == 'result':
            result = simpledialog.askstring("Input", "Enter result (Fraud/Not Fraud):", parent=gui)
            node_id = f"{attribute} {result} {self.node_counter}"
            self.node_counter += 1
            if path:
                ls = list(path.split('->')[-1].split(' '))
                op = ' '.join(ls[:-1]).strip()
                treel.create_node(node_id, node_id, parent=op)
            else:
                treel.create_node(node_id, node_id)
            text_widget.delete(1.0,tk.END)
            text_widget.insert(tk.END, treel.show(stdout=False))

            return TreeNode(result=result, path=path)

        value = simpledialog.askstring("Input", f"Enter value to compare for {attribute}", parent=gui)
        condition = simpledialog.askstring("Input", f"Enter condition for {attribute} (choose from >=, <=, ==):", parent=gui)
        node_id = f"{attribute} {condition} {value} {self.node_counter}"
        self.node_counter += 1
        if path:
            ls = list(path.split('->')[-1].split(' '))
            op = ' '.join(ls[:-1]).strip()
            treel.create_node(node_id, node_id, parent=op)
        else:
            treel.create_node(node_id, node_id)
        text_widget.delete(1.0,tk.END)
        text_widget.insert(tk.END, treel.show(stdout=False))

        messagebox.showinfo("Building Tree", f"Building left subtree for {attribute} {condition} {value}")
        left = self._build_tree_recursively(gui, path + f" -> {node_id} (left)", num + 1)

        messagebox.showinfo("Building Tree", f"Building right subtree for {attribute} {condition} {value}")
        right = self._build_tree_recursively(gui, path + f" -> {node_id} (right)", num + 1)

        return TreeNode(attribute=attribute, value=value, condition=condition, left=left, right=right, path=path)

    def predict(self, data):
        return self._predict_recursively(self.root, data)

    def _predict_recursively(self, node, data):
        if node.is_leaf():
            return node.result

        attribute_value = data[node.attribute]
        if node.condition == "==" and attribute_value == node.value:
            return self._predict_recursively(node.left, data)
        elif node.condition == ">=" and attribute_value >= float(node.value):
            return self._predict_recursively(node.left, data)
        elif node.condition == "<=" and attribute_value <= float(node.value):
            return self._predict_recursively(node.left, data)
        else:
            return self._predict_recursively(node.right, data)

def classify_transaction(description):
    if 'AU QR' in description:
        return 'AU QR Settlement'
    elif 'IMPS' in description:
        return 'IMPS'
    elif 'PSP SETTLEMENT' in description:
        return 'PSP Settlement'
    else:
        return 'Other'

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            global df
            df = pd.read_csv(file_path)
            df['Balance INR'] = df['Balance INR'].str.replace(',', '').astype(float)

            df['Previous Balance INR'] = df['Balance INR'].shift(1).fillna(df['Balance INR'][0])

            df['Debit(Dr.) INR'] = df['Debit(Dr.) INR'].str.replace(',', '').replace('-', 0).astype(float)
            df['Credit(Cr.) INR'] = df['Credit(Cr.) INR'].str.replace(',', '').replace('-', 0).astype(float)

            df['Transaction Amount'] = df['Credit(Cr.) INR'] - df['Debit(Dr.) INR']
            df['Transaction Type'] = df['Description/Narration'].apply(classify_transaction)

            df['Daily Transaction Count'] = df.groupby('Trans Date')['Transaction Amount'].transform('count')
            df['Daily Debit Total'] = df.groupby('Trans Date')['Debit(Dr.) INR'].transform('sum')
            df['Daily Credit Total'] = df.groupby('Trans Date')['Credit(Cr.) INR'].transform('sum')

            df['Transaction Sequence'] = df.groupby('Trans Date').cumcount() + 1
            df['Transaction to Balance Ratio'] = df['Transaction Amount'] / df['Previous Balance INR'].replace(0, 1)
            df['Trans Date'] = pd.to_datetime(df['Trans Date'])

            df = df.sort_values(by=['Trans Date', 'Transaction Sequence'])

            messagebox.showinfo("File Loaded", "CSV file loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

def save_csv(results):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            results_df = pd.DataFrame(results)
            df["results"] = results_df["prediction"]
            df.to_csv(file_path, index=False)
            messagebox.showinfo("File Saved", "CSV file saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV file: {e}")

def build_tree_gui():
    if df.empty:
        messagebox.showerror("Error", "Please load a CSV file first.")
        return
    tree.build_tree(root)
    messagebox.showinfo("Tree Built", "The decision tree has been successfully built.")
    # tree_struct.set(treel.show(stdout=False))
    # text_widget.insert(tk.END, treel.show(stdout=False))

def predict_gui():
    if df.empty:
        messagebox.showerror("Error", "Please load a CSV file first.")
        return
    if tree.root is None:
        messagebox.showerror("Error", "Please build the decision tree first.")
        return
        
    results = []
    for index, row in df.iterrows():
        result = tree.predict(row)
        results.append({"index": index, "prediction": result})

    save_csv(results)

treel = Tree()

root = tk.Tk()
root.title("Decision Tree GUI")

tree = DecisionTree()
df = pd.DataFrame()

current_path = tk.StringVar()

# tree_struct = tk.StringVar()
# tree_draw = tk.Label(root, textvariable=tree_struct)
# tree_draw.pack(pady=10)
text_widget=tk.Text(root)
text_widget.pack()
load_button = tk.Button(root, text="Load CSV File", command=load_csv)
load_button.pack(pady=10)

build_button = tk.Button(root, text="Build Decision Tree", command=build_tree_gui)
build_button.pack(pady=10)

predict_button = tk.Button(root, text="Predict with Decision Tree", command=predict_gui)
predict_button.pack(pady=10)

root.mainloop()
