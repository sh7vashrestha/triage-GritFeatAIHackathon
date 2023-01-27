import util
from flask import Flask, request, jsonify
import joblib
from flask import request
import numpy as np

app = Flask(__name__)

# Heart-and-kidney-predit

@app.route("/")
def ValuePredictorHeart(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==7):
        loaded_model = joblib.load(r'.\artifacts\heart_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]

def ValuePredictorKidney(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==7):
        loaded_model = joblib.load(r'.\artifacts\kidney_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/predict_kidney', methods = ["POST"])
def predict_kidney():
    bp = float(request.form['bp']) 
    sg = float(request.form['sg'])
    al = float(request.form['al'])
    su = float(request.form['su'])
    rbc = float(request.form['rbc'])
    pc = float(request.form['pc'])
    pcc = float(request.form['pcc']) 
    if request.method == "POST":
        to_predict_list = [bp,sg,al,su,rbc,pc,pcc]
        print(to_predict_list)
        if(len(to_predict_list)==7):
            result = ValuePredictorKidney(to_predict_list,7)
    
    if(int(result)==1):
        prediction = "Sorry you have chance of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    res = str(result)
    return{'result':prediction, 'val': res}    

@app.route('/predict_heart', methods = ["POST"])
def predict_heart():  
    cp = request.form['cp']
    trestbps = request.form['trestbps']
    chol = request.form['chol']
    fbs = request.form['fbs']
    restecg = request.form['restecg']
    thalach = request.form['thalach']
    exang = request.form['exang'] 
    
    if request.method == "POST":
        to_predict_list = [cp,trestbps,chol,fbs,restecg,thalach,exang]
        if(len(to_predict_list)==7):
            result = ValuePredictorHeart(to_predict_list,7)
    
    if(int(result)==1):
        prediction = "Sorry you have chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    res = str(result)
    return{'result':prediction, 'val': res}



#triage

@app.route('/predict', methods=['POST'])
def predict_triage():
    New_Saturation =  request.form['Saturation']
    Sexm = int(request.form['Sexm'])
    Injuryy = int(request.form['Injuryy'])
    Mental = request.form['Mental']
    Painy = int(request.form['Painy'])
    Error_group = request.form['Error_group']
    New_Age = request.form['New_Age']
    New_SBP = request.form['New_SBP']
    New_DBP = request.form['New_DBP']
    New_HR = request.form['New_HR']
    New_RR = request.form['New_RR']
    New_BT = request.form['New_BT']
    New_NRS_pain = request.form['New_NRS_pain']
    KTAS_expert  = util.get_estimated_Triage(Sexm,Injuryy,Mental,Painy,New_Saturation,Error_group,New_Age,New_SBP,New_DBP,New_HR,New_RR,New_BT,New_NRS_pain)
    Disposition = (util.get_estimated_Disposition(Sexm,Injuryy,Mental,Painy,New_Saturation,KTAS_expert,Error_group,New_Age,New_SBP,New_DBP,New_HR,New_RR,New_BT,New_NRS_pain))
    Length_of_stay_min = (util.get_estimated_New_Length_of_stay_min_expert(Sexm,Injuryy,Mental,Painy,New_Saturation,Disposition,KTAS_expert,Error_group,New_Age,New_SBP,New_DBP,New_HR,New_RR,New_BT,New_NRS_pain))
    
    response = jsonify({
        'estimated_Triage': KTAS_expert ,
        'estimated_Disposition': Disposition ,
        'estimated_Length_of_stay_min': Length_of_stay_min
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Triage Prediction...")
    util.load_saved_artifacts()
    app.run()