import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf
import json
import sys

try:

    # Read input data from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract inputs
    input_attendance = int(input_data["attendance"])
    input_marks = int(input_data["marks"])

    # Define input ranges
    x_attendance = np.arange(0, 101, 1)
    x_marks = np.arange(0, 101, 1)
    y_risk = np.arange(0, 101, 1)

    # Define membership functions for attendance and marks
    attendance_low = mf.trapmf(x_attendance, [0, 0, 30, 40])
    attendance_mid = mf.trapmf(x_attendance, [30, 40, 60, 70])
    attendance_high = mf.trapmf(x_attendance, [60, 70, 100, 100])

    marks_low = mf.trapmf(x_marks, [0, 0, 30, 40])
    marks_mid = mf.trapmf(x_marks, [30, 40, 60, 70])
    marks_high = mf.trapmf(x_marks, [60, 70, 100, 100])

    # Membership function evaluation
    attendance_fit_low = fuzz.interp_membership(x_attendance, attendance_low, input_attendance)
    attendance_fit_mid = fuzz.interp_membership(x_attendance, attendance_mid, input_attendance)
    attendance_fit_high = fuzz.interp_membership(x_attendance, attendance_high, input_attendance)
    marks_fit_low = fuzz.interp_membership(x_marks, marks_low, input_marks)
    marks_fit_mid = fuzz.interp_membership(x_marks, marks_mid, input_marks)
    marks_fit_high = fuzz.interp_membership(x_marks, marks_high, input_marks)

    # Define output membership functions for risk levels
    risk_not = mf.trapmf(y_risk, [0, 0, 15, 20])
    risk_little = mf.trapmf(y_risk, [15, 20, 35, 40])
    risk_mid = mf.trapmf(y_risk, [35, 40, 55, 60])
    risk_high = mf.trapmf(y_risk, [55, 60, 75, 80])
    risk_veryHigh = mf.trapmf(y_risk, [75, 80, 95, 100])

    # Rule definitions (adjust these as per your specific logic)
    rule1 = np.fmin(np.fmin(attendance_fit_high, marks_fit_high), risk_not)
    rule2 = np.fmin(np.fmin(attendance_fit_high, marks_fit_mid), risk_little)
    rule3 = np.fmin(np.fmin(attendance_fit_high, marks_fit_low), risk_high)
    rule4 = np.fmin(np.fmin(attendance_fit_mid, marks_fit_high), risk_not)
    rule5 = np.fmin(np.fmin(attendance_fit_mid, marks_fit_mid), risk_mid)
    rule6 = np.fmin(np.fmin(attendance_fit_mid, marks_fit_low), risk_high)
    rule7 = np.fmin(np.fmin(attendance_fit_low, marks_fit_high), risk_little)
    rule8 = np.fmin(np.fmin(attendance_fit_low, marks_fit_mid), risk_high)
    rule9 = np.fmin(np.fmin(attendance_fit_low, marks_fit_low), risk_veryHigh)

    # Aggregate all rules
    out_risk = np.fmax.reduce([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

    # Defuzzification
    defuzzified = fuzz.defuzz(y_risk, out_risk, 'centroid')

    #print("Outcome of risk is:", defuzzified)

    # Output the result
    result = {"result": defuzzified}
    print(json.dumps(result))

except Exception as e:
    print(json.dumps({"error": str(e)}))