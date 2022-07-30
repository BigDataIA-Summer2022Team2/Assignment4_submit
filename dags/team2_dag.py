import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.bash import BashOperator
doc_md = """
### DAG
#### Purpose

"""

def function():
    print('hi there!')

template_command = """

cd /opt/dataperf

python3 -m venv .test
source .test/bin/activate
pip install datascope

python3 create_baselines.py && python3 main.py && python3 plotter.py
"""

"""

"""

# source .dataperf/bin/activate.sh
# source .venv/bin/activate
# python3 create_baselines.py && python3 main.py && python3 plotter.py


with DAG("my_dag",start_date=datetime(2022, 1, 1),schedule_interval="@daily",catchup=False,) as dag:

        #change_venv = BashOperator(task_id='venv',bash_command='source /home/lemon/main/Assignment4/dataperf-vision-debugging/.venv/bin/activate')
        run_dataperf = BashOperator(task_id='dataperf',bash_command=template_command)
        #my_dag = PythonOperator(task_id='dag', python_callable=function)

        #run_dataperf >> my_dag 