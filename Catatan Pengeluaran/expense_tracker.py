import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import csv

class Expense:
    def __init__(self, date, description, amount, category):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = [] 
        
        self.setup_gui()   
        self.load_expenses() 

    def setup_gui(self):
        # Configure root grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create a frame for the form
        form_frame = tk.Frame(self.root)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # Date input
        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Description input
        tk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = tk.Entry(form_frame)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Amount input
        tk.Label(form_frame, text="Amount (IDR):").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Category input
        tk.Label(form_frame, text="Category:").grid(row=3, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(form_frame)
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Add, Delete, and Exit buttons
        tk.Button(form_frame, text="Add Expense", command=self.add_expense, bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(form_frame, text="Delete Selected Expense", command=self.delete_expense, bg="red", fg="white").grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(form_frame, text="Exit", command=self.root.quit).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Expense table setup
        self.tree = ttk.Treeview(self.root, columns=("Date", "Description", "Amount", "Category"), show='headings')
        for col in ("Date", "Description", "Amount", "Category"):
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Total expenses label
        self.total_label = tk.Label(self.root, text="Total Expenses: IDR 0")
        self.total_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    def add_expense(self):
        try:
            date_str = self.date_entry.get()
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Please enter the date in YYYY-MM-DD format")

            description = self.description_entry.get()
            if not description:
                raise ValueError("Please fill in all fields!")
            
            amount_str = self.amount_entry.get()
            try:
                amount = float(amount_str)
            except ValueError:
                raise ValueError("Please enter a valid number in the 'Amount' field")
            
            category = self.category_entry.get()
            if not category:
                raise ValueError("Please fill in all fields!")
            
            expense = Expense(date, description, amount, category)
            self.expenses.append(expense)
            
            # Add the expense to the table
            self.tree.insert("", "end", values=(date_str, description, amount, category))
            
            # Save expenses to CSV
            self.save_expenses()
            
            # Update total expenses
            self.update_total_expenses()
            
            # Clear input fields
            self.clear_entries()
            
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Remove the selected item from the table and expenses list
            item_index = self.tree.index(selected_item)
            self.tree.delete(selected_item)
            del self.expenses[item_index]
            # Save changes to CSV
            self.save_expenses()
            # Update total expenses
            self.update_total_expenses()
        else:
            messagebox.showwarning("Selection Error", "Please select the data you want to delete!")

    def save_expenses(self):
        # Write all expenses to a CSV file
        with open("expenses.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Amount", "Category"])
            for expense in self.expenses:
                writer.writerow([expense.date, expense.description, expense.amount, expense.category])

    def load_expenses(self):
        try:
            # Load expenses from the CSV file if it exists
            with open("expenses.csv", newline="") as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
                    description = row[1]
                    amount = float(row[2])
                    category = row[3]
                    expense = Expense(date, description, amount, category)
                    self.expenses.append(expense)
                    self.tree.insert("", "end", values=(row[0], description, amount, category))
            # Update total expenses after loading
            self.update_total_expenses()
        except FileNotFoundError:
            # If the file does not exist, simply do nothing
            pass
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading expenses: {str(e)}")

    def clear_entries(self):
        # Clear all input fields
        self.date_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
    
    def update_total_expenses(self):
        # Calculate and update the total expenses
        total = sum(expense.amount for expense in self.expenses)
        self.total_label.config(text=f"Total Expenses: IDR {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
