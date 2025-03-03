import pandas as pd
import joblib
import os

def predict_furnace_temps(width, thickness, gsm_a, hardness):
    model_folder = 'furnace_model'
    rf_model = joblib.load(os.path.join(model_folder, 'rf_model.joblib'))
    xgb_model = joblib.load(os.path.join(model_folder, 'xgb_model.joblib'))
    scaler = joblib.load(os.path.join(model_folder, 'scaler.joblib'))
    features = joblib.load(os.path.join(model_folder, 'features.joblib'))
    targets = joblib.load(os.path.join(model_folder, 'target.joblib'))
    
    input_data = pd.DataFrame([[width, thickness, gsm_a, hardness]], columns=features)
    input_scaled = scaler.transform(input_data)
    
    rf_predictions = rf_model.predict(input_scaled)[0]
    xgb_predictions = xgb_model.predict(input_scaled)[0]
    
    result = {}
    for i, target in enumerate(targets):
        rf_value = rf_predictions[i]
        xgb_value = xgb_predictions[i]
        result[target] = max(rf_value, xgb_value)
    
    # Calculate TPH
    if 'Speed' in result:
        density = 7850  # kg/m³
        width_m = width / 1000  # Convert mm to m
        thickness_m = thickness / 1000  # Convert mm to m
        speed = result['Speed']
        tph = (width_m * thickness_m * speed * density * 60) / 1000  # Result in tons/hour
        result['TPH'] = round(tph, 2)
    
    return result
