import customtkinter as ctk
import tkinter.messagebox as messagebox
import pandas as pd
from model import DementiaPredictionModel

class DementiaPredictionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dementia Prediction System")
        self.root.geometry("1300x750")  # Slightly smaller window for compact layout
        
        # Set dark appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")  # Professional dark blue theme
        
        # Define modern dark mode color palette
        self.colors = {
            'primary': '#1976D2',    # Deep blue for primary elements
            'secondary': '#0288D1',  # Lighter blue for accents
            'accent': '#D81B60',     # Vibrant pink for emphasis
            'background': '#212121', # Dark background
            'text': '#E0E0E0',       # Light grey for text
            'border': '#424242'      # Subtle dark border
        }
        
        # Initialize model
        self.model = DementiaPredictionModel()
        try:
            self.model.train('data.csv')
            print("Model trained successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Model training failed: {str(e)}")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container with minimal padding
        main_frame = ctk.CTkFrame(self.root, fg_color=self.colors['background'])
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable canvas
        canvas = ctk.CTkCanvas(main_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(canvas, fg_color=self.colors['background'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            delta = -1 if event.delta > 0 or event.num == 4 else 1
            canvas.yview_scroll(delta, "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
        canvas.bind_all("<Button-4>", _on_mousewheel)    # Linux (scroll up)
        canvas.bind_all("<Button-5>", _on_mousewheel)    # Linux (scroll down)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Professional Header
        header_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=self.colors['primary'],
            corner_radius=10,
            border_width=2,
            border_color=self.colors['border']
        )
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew", padx=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Dementia Prediction System",
            font=ctk.CTkFont(family="Roboto", size=24, weight="bold"),
            text_color=self.colors['text']
        )
        title_label.pack(pady=(8, 4))
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Precision Healthcare Analytics Platform",
            font=ctk.CTkFont(family="Roboto", size=12),
            text_color=self.colors['text']
        )
        subtitle_label.pack(pady=(0, 8))
        
        # Input sections in two-column layout
        sections = {
            "👤 Patient Demographics": [
                ('Age', None, "Enter Age (18–120 years)"),
                ('Gender', ['Male', 'Female'], "Select Gender (Male, Female)"),
                ('Weight', None, "Enter Weight (30–200 kg)"),
                ('Dominant_Hand', ['Right', 'Left'], "Select Dominant Hand (Right, Left)")
            ],
            "🏥 Medical History": [
                ('Diabetic', ['0', '1'], "Select Diabetic Status (0 = No, 1 = Yes)"),
                ('Family_History', ['Yes', 'No'], "Select Family History (Yes, No)"),
                ('Chronic_Health_Conditions', ['None', 'Heart Disease', 'Diabetes', 'Hypertension'], "Select Condition (None, Heart Disease, Diabetes, Hypertension)"),
                ('APOE_ε4', ['Positive', 'Negative'], "Select APOE ε4 Status (Positive, Negative)")
            ],
            "❤️ Vital Signs": [
                ('HeartRate', None, "Enter Heart Rate (40–200 bpm)"),
                ('BloodOxygenLevel', None, "Enter Blood Oxygen Level (80–100%)"),
                ('BodyTemperature', None, "Enter Body Temperature (35–40°C)")
            ],
            "🌿 Lifestyle Factors": [
                ('AlcoholLevel', None, "Enter Alcohol Level (0–0.08 BAC)"),
                ('Smoking_Status', ['Never Smoked', 'Former Smoker', 'Current Smoker'], "Select Smoking Status (Never Smoked, Former Smoker, Current Smoker)"),
                ('Physical_Activity', ['Sedentary', 'Mild Activity', 'Moderate Activity', 'High Activity'], "Select Activity Level (Sedentary, Mild, Moderate, High)"),
                ('Sleep_Quality', ['Good', 'Fair', 'Poor'], "Select Sleep Quality (Good, Fair, Poor)"),
                ('Nutrition_Diet', ['Balanced Diet', 'Low-Carb Diet', 'Mediterranean Diet', 'Other'], "Select Diet (Balanced, Low-Carb, Mediterranean, Other)")
            ],
            "🧠 Clinical Assessment": [
                ('Cognitive_Test_Scores', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], "Select Cognitive Score (0–10)"),
                ('Depression_Status', ['Yes', 'No'], "Select Depression Status (Yes, No)"),
                ('MRI_Delay', None, "Enter MRI Delay (0–60 minutes)")
            ],
            "💊 Medication": [
                ('Prescription', ['Galantamine', 'Memantine', 'Rivastigmine', 'Donepezil', 'None'], "Select Prescription (Galantamine, Memantine, Rivastigmine, Donepezil, None)"),
                ('Dosage in mg', None, "Enter Dosage (0–100 mg)"),
                ('Medication_History', ['Yes', 'No'], "Select Medication History (Yes, No)")
            ]
        }
        
        self.inputs = {}
        left_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.colors['background'])
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        right_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.colors['background'])
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        self.scrollable_frame.grid_columnconfigure((0, 1), weight=1)
        
        current_row_left = 0
        current_row_right = 0
        section_count = 0
        
        for section_name, fields in sections.items():
            # Distribute sections between left and right columns
            target_frame = left_frame if section_count < 3 else right_frame
            current_row = current_row_left if section_count < 3 else current_row_right
            
            # Section frame with compact styling
            section_frame = ctk.CTkFrame(
                target_frame,
                fg_color="#2D2D2D",
                corner_radius=8,
                border_width=2,
                border_color=self.colors['border']
            )
            section_frame.grid(row=current_row, column=0, padx=5, pady=(0, 5), sticky="ew")
            
            # Section header
            ctk.CTkLabel(
                section_frame,
                text=section_name,
                font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
                text_color=self.colors['text']
            ).pack(pady=(6, 4), padx=8, anchor="w")
            
            # Grid for input fields
            grid_frame = ctk.CTkFrame(section_frame, fg_color="#2D2D2D")
            grid_frame.pack(fill="x", padx=8, pady=(0, 6))
            
            for i, (field, values, tooltip) in enumerate(fields):
                # Field label
                label = ctk.CTkLabel(
                    grid_frame,
                    text=field.replace('_', ' '),
                    font=ctk.CTkFont(family="Roboto", size=11),
                    text_color=self.colors['text']
                )
                label.grid(row=i, column=0, padx=(8, 6), pady=3, sticky="e")
                label.bind("<Enter>", lambda e, t=tooltip: self.show_tooltip(e, t))
                label.bind("<Leave>", lambda e: self.hide_tooltip())
                
                # Input widget
                if values:
                    self.inputs[field] = ctk.CTkComboBox(
                        grid_frame,
                        values=values,
                        width=200,
                        height=28,
                        font=ctk.CTkFont(family="Roboto", size=11),
                        border_width=2,
                        border_color=self.colors['border'],
                        button_color=self.colors['primary'],
                        button_hover_color=self.colors['accent'],
                        dropdown_font=ctk.CTkFont(family="Roboto", size=11),
                        text_color=self.colors['text']
                    )
                else:
                    self.inputs[field] = ctk.CTkEntry(
                        grid_frame,
                        width=200,
                        height=28,
                        font=ctk.CTkFont(family="Roboto", size=11),
                        border_width=2,
                        border_color=self.colors['border'],
                        placeholder_text=tooltip,
                        text_color=self.colors['text']
                    )
                self.inputs[field].grid(row=i, column=1, padx=8, pady=3, sticky="w")
                self.inputs[field].bind("<Enter>", lambda e, t=tooltip: self.show_tooltip(e, t))
                self.inputs[field].bind("<Leave>", lambda e: self.hide_tooltip())
            
            if section_count < 3:
                current_row_left += 1
            else:
                current_row_right += 1
            section_count += 1
        
        # Action buttons frame
        button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.colors['background'])
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 10), padx=10, sticky="ew")
        
        # Predict button (prominently placed)
        predict_button = ctk.CTkButton(
            button_frame,
            text="Generate Prediction",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            height=40,
            width=200,
            corner_radius=15,
            command=self.make_prediction,
            fg_color=self.colors['primary'],
            hover_color=self.colors['accent'],
            border_width=2,
            border_color=self.colors['border']
        )
        predict_button.pack(side="left", padx=10)
        
        # Clear button
        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Inputs",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            height=40,
            width=200,
            corner_radius=15,
            command=self.clear_inputs,
            fg_color=self.colors['secondary'],
            hover_color=self.colors['accent'],
            border_width=2,
            border_color=self.colors['border']
        )
        clear_button.pack(side="left", padx=10)
        
        # Results section
        self.results_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2D2D2D",
            corner_radius=8,
            border_width=2,
            border_color=self.colors['border']
        )
        self.results_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")
        
        results_title = ctk.CTkLabel(
            self.results_frame,
            text="📊 Prediction Results",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            text_color=self.colors['text']
        )
        results_title.pack(pady=(6, 4))
        
        # Results display with accuracies
        self.result_labels = {}
        models_frame = ctk.CTkFrame(self.results_frame, fg_color="#2D2D2D")
        models_frame.pack(fill="x", padx=8, pady=(0, 6))
        
        # Get model accuracies
        accuracies = self.model.get_accuracies()
        
        for i, model_name in enumerate(['Logistic Regression', 'Random Forest', 'XGBoost']):
            model_frame = ctk.CTkFrame(models_frame, fg_color=self.colors['background'], corner_radius=6)
            model_frame.pack(fill="x", padx=8, pady=4)
            
            ctk.CTkLabel(
                model_frame,
                text=f"{model_name} (Accuracy: {accuracies.get(model_name, 0):.2%})",
                font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
                text_color=self.colors['text']
            ).pack(pady=(4, 3))
            
            results_subframe = ctk.CTkFrame(model_frame, fg_color="transparent")
            results_subframe.pack(fill="x", padx=8, pady=(0, 4))
            
            self.result_labels[f"{model_name}_no_dementia"] = ctk.CTkLabel(
                results_subframe,
                text="No Dementia: --",
                font=ctk.CTkFont(family="Roboto", size=11),
                text_color=self.colors['secondary']
            )
            self.result_labels[f"{model_name}_no_dementia"].pack(side="left", padx=8)
            
            self.result_labels[f"{model_name}_dementia"] = ctk.CTkLabel(
                results_subframe,
                text="Dementia: --",
                font=ctk.CTkFont(family="Roboto", size=11),
                text_color=self.colors['accent']
            )
            self.result_labels[f"{model_name}_dementia"].pack(side="right", padx=8)
    
    def show_tooltip(self, event, text):
        """Show tooltip near the widget."""
        x = event.widget.winfo_rootx() + 20
        y = event.widget.winfo_rooty() + 20
        self.tooltip = ctk.CTkToplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(
            self.tooltip,
            text=text,
            fg_color="#424242",
            text_color=self.colors['text'],
            padding=(5, 5),
            corner_radius=5
        )
        label.pack()
    
    def hide_tooltip(self):
        """Hide the tooltip."""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            del self.tooltip
    
    def clear_inputs(self):
        """Clear all input fields."""
        for field, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkComboBox):
                widget.set("")
        for model_name in ['Logistic Regression', 'Random Forest', 'XGBoost']:
            self.result_labels[f"{model_name}_no_dementia"].configure(text="No Dementia: --")
            self.result_labels[f"{model_name}_dementia"].configure(text="Dementia: --")
    
    def make_prediction(self):
        try:
            self.root.config(cursor="wait")
            
            # Gather inputs
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
                    messagebox.showerror("Error", f"Please fill in the {field.replace('_', ' ')} field")
                    self.root.config(cursor="")
                    return
                input_values.append(str(value))
            
            # Make prediction
            input_string = ','.join(input_values)
            predictions = self.model.predict(input_string)
            
            # Update results
            if predictions:
                for model_name, probs in predictions.items():
                    self.result_labels[f"{model_name}_no_dementia"].configure(
                        text=f"No Dementia: {probs[0]:.1%}",
                        font=ctk.CTkFont(family="Roboto", size=11, weight="bold")
                    )
                    self.result_labels[f"{model_name}_dementia"].configure(
                        text=f"Dementia: {probs[1]:.1%}",
                        font=ctk.CTkFont(family="Roboto", size=11, weight="bold")
                    )
            else:
                messagebox.showerror("Error", "Prediction failed. Please check your inputs.")
            
            self.root.config(cursor="")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.root.config(cursor="")

def main():
    root = ctk.CTk()
    app = DementiaPredictionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()