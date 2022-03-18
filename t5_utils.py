# +
from tracemalloc import start
import pandas as pd
import numpy as np
import json, io, os
#from db_setup.process_frames import filter_bboxes
import kso_utils.db_utils as db_utils
from collections import OrderedDict
from IPython.display import HTML, display, update_display, clear_output
import ipywidgets as widgets
from ipywidgets import interact
from ipyfilechooser import FileChooser
import asyncio

import wandb
import paramiko
from paramiko import SSHClient
from scp import SCPClient


# -

def transfer_model(model_name: str, artifact_dir: str, project_name: str, user: str, password: str):
    #api = wandb.Api()
    #collection = [
    #    coll for coll in api.artifact_type(type_name='model', project=project_name).collections()
    #][-1]
    #artifact = api.artifact(f"{project_name}/" + collection.name + ":latest")
    # Download the artifact's contents
    #artifact_dir = artifact.download()
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    ssh.load_system_host_keys()
    ssh.connect(hostname="80.252.221.46", 
                port = 2230,
                username=user,
                password=password)

    # SCPCLient takes a paramiko transport as its only argument
    scp = SCPClient(ssh.get_transport())
    scp.put(f"{artifact_dir}/weights/best.pt", 
            f"/home/koster/model_config/weights/ \
            {os.path.basename(project_name)}_{os.path.basename(os.path.dirname(artifact_dir))}_{model_name}")
    scp.close()


def choose_test_prop():
        
    w = widgets.FloatSlider(
        value=0.2,
        min=0.0,
        max=1.0,
        step=0.1,
        description='Test proportion:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        display='flex',
        flex_flow='column',
        align_items='stretch',
        style= {'description_width': 'initial'}
    )
    
    v = widgets.FloatLogSlider(
        value=3,
        base=2,
        min=0, # max exponent of base
        max=10, # min exponent of base
        step=1, # exponent step
        description='Batch size:'
    )
    
    z = widgets.IntSlider(
        value=10,
        min=0,
        max=1000,
        step=10,
        description='Epochs:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )
    
    z1 = widgets.FloatSlider(
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1,
        description='Confidence threshold:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        display='flex',
        flex_flow='column',
        align_items='stretch',
        style= {'description_width': 'initial'}
    )
    
    box = widgets.HBox([w, v, z, z1])
   
    display(box)
    return w, v, z, z1

