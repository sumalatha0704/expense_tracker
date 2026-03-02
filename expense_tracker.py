# expense_tracker.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tracker_logic import calculate_total, validate_amount, save_to_csv, load_from_csv

CATEGORIES = ["Food", "Transport", "Housing", "Entertainment", "Health", "Other"]

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")
        self.expenses = []
        self._build_ui()

    def _build_ui(self):
        # --- Input Frame ---
        input_frame = ttk.LabelFrame(self.root, text="Add Expense", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=0, column=0, sticky="w")
        self.desc_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.desc_var, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, sticky="w")
        self.cat_var = tk.StringVar(value=CATEGORIES[0])
        ttk.Combobox(input_frame, textvariable=self.cat_var, values=CATEGORIES, width=15).grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Amount ($):").grid(row=0, column=4, sticky="w")
        self.amt_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.amt_var, width=10).grid(row=0, column=5, padx=5)

        ttk.Button(input_frame, text="Add", command=self.add_expense).grid(row=0, column=6, padx=5)

        # --- Table ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("Description", "Category", "Amount")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200 if col != "Amount" else 100)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Bottom Bar ---
        bottom = ttk.Frame(self.root)
        bottom.pack(fill="x", padx=10, pady=5)

        self.total_label = ttk.Label(bottom, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(side="left")

        ttk.Button(bottom, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=10)
        ttk.Button(bottom, text="Save CSV", command=self.save_csv).pack(side="right", padx=5)
        ttk.Button(bottom, text="Load CSV", command=self.load_csv).pack(side="right", padx=5)

    def add_expense(self):
        desc = self.desc_var.get().strip()
        cat = self.cat_var.get()
        try:
            amount = validate_amount(self.amt_var.get())
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
        if not desc:
            messagebox.showerror("Invalid Input", "Description cannot be empty.")
            return

        expense = {"description": desc, "category": cat, "amount": amount}
        self.expenses.append(expense)
        self.tree.insert("", "end", values=(desc, cat, f"${amount:.2f}"))
        self._update_total()
        self.desc_var.set("")
        self.amt_var.set("")

    def delete_selected(self):
        selected = self.tree.selection()
        for item in selected:
            idx = self.tree.index(item)
            self.expenses.pop(idx)
            self.tree.delete(item)
        self._update_total()

    def _update_total(self):
        total = calculate_total(self.expenses)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def save_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            save_to_csv(self.expenses, path)
            messagebox.showinfo("Saved", f"Expenses saved to {path}")

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            self.expenses = load_from_csv(path)
            self.tree.delete(*self.tree.get_children())
            for e in self.expenses:
                self.tree.insert("", "end", values=(e["description"], e["category"], f"${e['amount']:.2f}"))
            self._update_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()