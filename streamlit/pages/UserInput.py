import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import yaml
import pandas as pd
import numpy as np
import time
import base64
from PIL import Image
import os
import requests
#import pymysql
import time
from datetime import datetime
import json
import glob

#st.session_state


def getCurrentTimeStr():
 
    currentSecond= datetime.now().second
    currentMinute = datetime.now().minute
    currentHour = datetime.now().hour
 
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    #run_id=manual__2022-07-30T08:27:12.766120+00:00

    run_id = 'run_id=manual__' + str(currentYear) + '-' + str(currentMonth) + '-' + str(currentDay) + 'T' + str(currentHour+4) + ':' + str(currentMinute) + ':' + str(currentSecond)

    return run_id


def createSetupFile(user_input,filePath):
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data=user_input, stream=file, allow_unicode=True)


def isSetupFileExists(filePath):
    if os.path.exists(filePath):
        return True
    else:
        return False

def showMain():
    st.header("Data Perf")

    user_input = {}
    user_input["paths"] = {}
    user_input["paths"]["embedding_folder"] = "embeddings/"
    user_input["paths"]["groundtruth_folder"] = "data/"
    user_input["paths"]["submission_folder"] =  "submissions/"
    user_input["paths"]["results_folder"] = "results/"

    model = st.selectbox(
        'What kind of model you want to choose?',
        ('01g317', '04hgtk', '04rky','09j2d'))

    isflipped = st.checkbox('flipped')

    data_id = ""
    if isflipped == True:
        data_id = model + "-flipped"
    else:
        data_id = model


    task_details = {}
    task_details["data_id"] = data_id
    task_details["train_size"] = 300 # train_size
    task_details["noise_level"] = 0.3 # noise_level
    task_details["test_size"] = 500 # test_size
    task_details["val_size"] = 100 # val_size
    user_input["tasks"] = [task_details]

    user_input["baselines"] = [{"name": "neighbor_shapley (datascope)"},{"name": "random"}]

    isClick = st.button("RUN")

    if isClick == True:
        abs_path = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))
        filePath = abs_path+"/dataperf/task_setup.yml"
        st.write()
        createSetupFile(user_input,filePath)
        
        if isSetupFileExists(filePath) == True:
            st.success("task_setup.yml created successfully!")  

            run_id= st.session_state["name"] + '-' + getCurrentTimeStr()

                
            
            
            # deployment_url = "http://204.15.72.120:8080"
            # dag_id = "my_dag"
            

            # res = requests.post(
            #     url=f"{deployment_url}/api/experimental/dags/{dag_id}/dagRuns",
            #     headers={"Content-Type": "application/json"},
            #     data={"run_id": "meihuqin","state": "queued","conf": '{}'}
            # )
            # st.write(res.text) 
            #st.write(res.json())


            # url = 'http://localhost:8080/api/experimental/dags/my_dag/dag_runs'

            # headers = {'Content-Type': 'application/json', 'Cache-Control': 'no-cache'}
            # data = {}
            # data["run_id"] = run_id
            # data["state"] = "queued"
            # data["conf"] = {}
            
            
            # res = requests.post(url=url,data=data,headers=headers)

            # st.write(res.text)     





            
            # os.system(command)
            imageFileName = data_id + "_evaluation.png"
            jsonFileName = data_id + "_evaluation.json"
            imagePath = abs_path + "/dataperf/results/" + imageFileName
            jsonPath = abs_path + "/dataperf/results/" + jsonFileName
            #st.write(imagePath)
            #flag = true

            template_command = """
                airflow dags trigger my_dag
            """

            os.system(template_command)

            
            my_bar = st.progress(0)

            st.info("Pleasr Wait... It taks about 35+ mins")
            for percent_complete in range(100):
                time.sleep(24)
                my_bar.progress(percent_complete + 1)


            if os.path.exists(imagePath):
                st.image(imagePath)
                os.remove(imagePath)
                os.remove(jsonPath)

                # st.write(run_id)
                # #run_id=manual__2022-07-30T08:27:12.766120+00:00
                # with st.expander("See explanation"):
                #     log_path = "/root/airflow/logs/dag_id=my_dag"
                #     check_file = run_id + '*'
                #     adirs=glob.glob(os.path.join(log_path,check_file)) 
                #     for adir in adirs:
                #         file_name=os.path.split(adirs)[-1]


            else:
                st.error("image DOES NOT EXIST!")
            
            


            
        else:
            st.error("task_setup.yml does not exist!")
            st.warning("Contact us ASAP!")



with open('./streamlit_config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


with st.sidebar:
    if(st.session_state.authentication_status == True):
        st.info("User: ***%s***" % st.session_state.username)
        authenticator.logout('Logout')
    
if(st.session_state.authentication_status == None or st.session_state.authentication_status == False):
    st.header("Please go to ***Home Page and login***!")
    st.session_state.token = ''

if(st.session_state.authentication_status == True):
    showMain()
    
