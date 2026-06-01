import streamlit as st
import pandas as pd

# Assuming the functions collect_patient_data, collect_symptom_data,
# collect_contact_history, and calculate_risk_level are defined in the environment

st.title("Pediatric Patient Susceptibility Assessment")

st.header("Patient Information")
patient_name = st.text_input("Enter patient's name:")
patient_age = st.number_input("Enter patient's age:", min_value=0, max_value=18, step=1)
patient_region = st.text_input("Enter patient's region:")
patient_temperature = st.number_input("Enter patient's temperature:", format="%0.2f")


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
    # Assuming calculate_risk_level function is available and symptom_to_weight is globally accessible
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
