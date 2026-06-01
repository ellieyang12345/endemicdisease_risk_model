import streamlit as st
import pandas as pd

# --- Data Loading and Preprocessing for Risk Calculation ---
# Load the Symptom-severity dataset
symptom_severity_df = pd.read_csv('/content/Symptom-severity.csv')

# Clean symptom names in symptom_severity_df and create the symptom_to_weight map
symptom_severity_df['Symptom'] = symptom_severity_df['Symptom'].str.lower().str.replace('_', ' ').str.strip()
symptom_to_weight = dict(zip(symptom_severity_df['Symptom'], symptom_severity_df['weight']))

# --- Function Definition for Risk Calculation ---
def calculate_risk_level(symptom_binary_data, contact_history_binary_data, symptom_to_weight_map):
    """Calculates the risk level based on binary symptom and contact history data using symptom weights."""
    total_weighted_score = 0
    total_possible_weight = 0

    # Calculate weighted score for active symptoms
    for symptom_name, is_present in symptom_binary_data.items():
        if is_present == 1:
            cleaned_symptom = symptom_name.lower().replace('_', ' ').strip()
            if cleaned_symptom in symptom_to_weight_map:
                total_weighted_score += symptom_to_weight_map[cleaned_symptom]
            else:
                # Assign a default medium weight if symptom not found in map
                total_weighted_score += 3 # Default weight for unknown symptom
        # Each symptom contributes 5 to the total possible weight (assuming max weight is 5)
        total_possible_weight += 5

    # Incorporate contact history into the weighted score
    if contact_history_binary_data == 1:
        # Assign a significant weight to contact history if present (e.g., similar to a severe symptom)
        total_weighted_score += 4
    # Add max possible weight for contact history to the denominator
    total_possible_weight += 5

    weighted_frequency = total_weighted_score / total_possible_weight if total_possible_weight > 0 else 0

    if weighted_frequency < 0.33:
        risk_level = "Low Risk"
    elif weighted_frequency < 0.66:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    return risk_level, weighted_frequency

# --- Streamlit App Layout ---
st.title("Pediatric Patient Susceptibility Assessment")

st.header("Patient Information")
patient_name = st.text_input("Enter patient's name:")
patient_age = st.number_input("Enter patient's age:", min_value=12, max_value=116, step=1) # Age range updated
patient_region = st.text_input("Enter patient's region:")
patient_temperature = st.number_input("Enter patient's temperature (Celsius):", format="%0.2f") # Celsius added


st.header("Symptom Data")
symptoms_list = [
    "coughing", "chest pain", "breathing problems", "papule appearance",
    "skin pain", "diarrhea", "abdominal pain", "conjunctival congestion",
    "burning eyes", "itchy eyes", "eye secretions", "blisters/ulcers in hand/foot/mouth"
]
symptoms_input = {}
for symptom in symptoms_list:
    symptoms_input[symptom] = st.radio(f"{symptom.replace('_', ' ').capitalize()} (yes/no):", ('no', 'yes'))

st.header("Contact History")
contact_history_input = st.radio("Contact/consumption of infected/sick/dead animals/remains (yes/no):", ('no', 'yes'))

# Convert 'yes'/'no' to 1/0
symptom_binary_streamlit = {symptom: 1 if response == 'yes' else 0 for symptom, response in symptoms_input.items()}
contact_history_binary_streamlit = 1 if contact_history_input == 'yes' else 0

if st.button("Assess Risk"):
    # Call the calculate_risk_level function with the necessary arguments
    risk_level, frequency = calculate_risk_level(symptom_binary_streamlit, contact_history_binary_streamlit, symptom_to_weight)

    st.subheader("Assessment Results")
    st.write(f"Patient Name: {patient_name}")
    st.write(f"Patient Age: {patient_age}")
    st.write(f"Patient Region: {patient_region}")
    st.write(f"Patient Temperature: {patient_temperature}")
    st.write(f"Frequency of 'yes' responses: {frequency:.2f}")
    st.write(f"Calculated Risk Level: {risk_level}")

    # You can add a simple visual indicator for the risk level here
    if risk_level == "Low Risk":
        st.success(risk_level)
    elif risk_level == "Medium Risk":
        st.warning(risk_level)
    else:
        st.error(risk_level)
