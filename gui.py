import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from model import DementiaPredictionModel  # Assuming previous model code is saved as model.py

class DementiaPredictionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dementia Prediction System")
        self.root.geometry("800x900")
        
        # Initialize the model
        self.model = DementiaPredictionModel()
        try:
            self.model.train('data.csv')
            print("Model trained successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error training model: {str(e)}")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1)
        
        # Add canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar components
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(self.scrollable_frame, text="Dementia Prediction System", 
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Input fields
        self.inputs = {}
        current_row = 1
        
        # Numerical inputs
        numerical_fields = [
            ('Diabetic', ['0', '1']),
            ('AlcoholLevel', None),
            ('HeartRate', None),
            ('BloodOxygenLevel', None),
            ('BodyTemperature', None),
            ('Weight', None),
            ('MRI_Delay', None),
            ('Dosage in mg', None),
            ('Age', None),
            ('Cognitive_Test_Scores', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        ]
        
        # Categorical inputs
        categorical_fields = [
            ('Prescription', ['Galantamine', 'Memantine', 'Rivastigmine', 'Donepezil', 'None']),
            ('Dominant_Hand', ['Right', 'Left']),
            ('Gender', ['Male', 'Female']),
            ('Family_History', ['Yes', 'No']),
            ('Smoking_Status', ['Never Smoked', 'Former Smoker', 'Current Smoker']),
            ('APOE_ε4', ['Positive', 'Negative']),
            ('Physical_Activity', ['Sedentary', 'Mild Activity', 'Moderate Activity', 'High Activity']),
            ('Depression_Status', ['Yes', 'No']),
            ('Medication_History', ['Yes', 'No']),
            ('Nutrition_Diet', ['Balanced Diet', 'Low-Carb Diet', 'Mediterranean Diet', 'Other']),
            ('Sleep_Quality', ['Good', 'Fair', 'Poor']),
            ('Chronic_Health_Conditions', ['None', 'Heart Disease', 'Diabetes', 'Hypertension'])
        ]
        
        # Add numerical inputs
        for field, values in numerical_fields:
            ttk.Label(self.scrollable_frame, text=field).grid(row=current_row, column=0, padx=5, pady=2)
            if values:
                self.inputs[field] = ttk.Combobox(self.scrollable_frame, values=values)
            else:
                self.inputs[field] = ttk.Entry(self.scrollable_frame)
            self.inputs[field].grid(row=current_row, column=1, padx=5, pady=2)
            current_row += 1
        
        # Add categorical inputs
        for field, values in categorical_fields:
            ttk.Label(self.scrollable_frame, text=field).grid(row=current_row, column=0, padx=5, pady=2)
            self.inputs[field] = ttk.Combobox(self.scrollable_frame, values=values)
            self.inputs[field].grid(row=current_row, column=1, padx=5, pady=2)
            current_row += 1
        
        # Predict button
        ttk.Button(self.scrollable_frame, text="Predict", command=self.make_prediction).grid(
            row=current_row, column=0, columnspan=2, pady=20)
        current_row += 1
        
        # Results section
        self.results_frame = ttk.LabelFrame(self.scrollable_frame, text="Prediction Results")
        self.results_frame.grid(row=current_row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Labels for results
        self.result_labels = {}
        for i, model_name in enumerate(['Logistic Regression', 'Random Forest', 'XGBoost']):
            ttk.Label(self.results_frame, text=f"\n{model_name}:").grid(row=i*2, column=0, columnspan=2, sticky="w")
            self.result_labels[f"{model_name}_no_dementia"] = ttk.Label(self.results_frame, text="")
            self.result_labels[f"{model_name}_dementia"] = ttk.Label(self.results_frame, text="")
            self.result_labels[f"{model_name}_no_dementia"].grid(row=i*2+1, column=0, sticky="w")
            self.result_labels[f"{model_name}_dementia"].grid(row=i*2+1, column=1, sticky="w")
    
    def make_prediction(self):
        try:
            # Gather all inputs
            input_values = []
            for field in [
                'Diabetic', 'AlcoholLevel', 'HeartRate', 'BloodOxygenLevel', 
                'BodyTemperature', 'Weight', 'MRI_Delay', 'Prescription', 
                'Dosage in mg', 'Age', 'Dominant_Hand', 'Gender', 
                'Family_History', 'Smoking_Status', 'APOE_ε4', 
                'Physical_Activity', 'Depression_Status', 'Cognitive_Test_Scores', 
                'Medication_History', 'Nutrition_Diet', 'Sleep_Quality', 
                'Chronic_Health_Conditions'
            ]:
                value = self.inputs[field].get()
                if value == '':
                    messagebox.showerror("Error", f"Please fill in the {field} field")
                    return
                input_values.append(str(value))
            
            # Make prediction
            input_string = ','.join(input_values)
            predictions = self.model.predict(input_string)
            
            # Update results
            if predictions:
                for model_name, probs in predictions.items():
                    self.result_labels[f"{model_name}_no_dementia"].config(
                        text=f"No Dementia: {probs[0]:.4f}")
                    self.result_labels[f"{model_name}_dementia"].config(
                        text=f"Dementia: {probs[1]:.4f}")
            else:
                messagebox.showerror("Error", "Prediction failed. Please check your inputs.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = DementiaPredictionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()