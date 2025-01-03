import tkinter as tk
from tkinter import messagebox, simpledialog

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced To-Do List")
        self.root.geometry("400x600")
        self.root.config(bg="#ffecd2")

        # Title Label
        self.title_label = tk.Label(root, text="My To-Do List", font=("Helvetica", 18, "bold"), bg="#ff6f91", fg="white", pady=10)
        self.title_label.pack(fill=tk.X)

        # Search Bar
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_tasks)
        self.search_entry = tk.Entry(root, textvariable=self.search_var, font=("Helvetica", 12))
        self.search_entry.pack(pady=10, padx=20, fill=tk.X)

        # Listbox for tasks
        self.task_list = tk.Listbox(root, font=("Helvetica", 12), bg="#fff", fg="#333", selectbackground="#ff6f91", height=15)
        self.task_list.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Buttons Frame
        self.button_frame = tk.Frame(root, bg="#ffecd2")
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add", font=("Helvetica", 10), bg="#ff6f91", fg="white", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(self.button_frame, text="Update", font=("Helvetica", 10), bg="#f3a683", fg="white", command=self.update_task)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", font=("Helvetica", 10), bg="#f78fb3", fg="white", command=self.delete_task)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.done_button = tk.Button(self.button_frame, text="Mark as Done", font=("Helvetica", 10), bg="#786fa6", fg="white", command=self.mark_done)
        self.done_button.grid(row=0, column=3, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear All", font=("Helvetica", 10), bg="#786fa6", fg="white", command=self.clear_tasks)
        self.clear_button.grid(row=0, column=4, padx=5)

        self.exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), bg="#cf6a87", fg="white", command=self.save_and_exit)
        self.exit_button.pack(pady=10)

        # Load tasks from file
        self.load_tasks()

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter a new task:")
        if task:
            self.task_list.insert(tk.END, task)

    def update_task(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            current_task = self.task_list.get(selected_task_index)
            new_task = simpledialog.askstring("Update Task", "Edit the task:", initialvalue=current_task)
            if new_task:
                self.task_list.delete(selected_task_index)
                self.task_list.insert(selected_task_index, new_task)
        else:
            messagebox.showerror("Error", "No task selected to update.")

    def delete_task(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            self.task_list.delete(selected_task_index)
        else:
            messagebox.showerror("Error", "No task selected to delete.")

    def clear_tasks(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all tasks?"):
            self.task_list.delete(0, tk.END)

    def mark_done(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            task = self.task_list.get(selected_task_index)
            self.task_list.delete(selected_task_index)
            self.task_list.insert(tk.END, f"✔️ {task}")
        else:
            messagebox.showerror("Error", "No task selected to mark as done.")

    def search_tasks(self, *args):
        search_term = self.search_var.get().lower()
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            if search_term in task.lower():
                self.task_list.insert(tk.END, task)

    def save_and_exit(self):
        with open("tasks.txt", "w") as file:
            tasks = self.task_list.get(0, tk.END)
            file.write("\n".join(tasks))
        self.root.quit()

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = file.read().splitlines()
                for task in self.tasks:
                    self.task_list.insert(tk.END, task)
        except FileNotFoundError:
            self.tasks = []

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
