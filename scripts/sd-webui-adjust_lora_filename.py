#!/usr/bin/python3
'''sd-webui-lora_metadata_viewer
Extension for AUTOMATIC1111.

Version 0.0.0.1
'''
# pylint: disable=invalid-name
# pylint: disable=import-error
# pylint: disable=trailing-whitespace
# pylint: disable=line-too-long
# pylint: disable=no-member

# Import the Python modules.
import os
import json
import gradio as gr
import modules.sd_models as models
import modules.shared
from modules.ui import create_refresh_button
from modules import script_callbacks

# Get LoRA path.
LORA_PATH = getattr(modules.shared.cmd_opts, "lora_dir", os.path.join(models.paths.models_path, "Lora"))

# Create dictionary.
lora_dict = {}

# Set private variable.
_SortDir = False

# Function lora_scan().
def lora_scan(lora_dir: str, ext: list) -> (list, list):
    '''File scan for LoRA models.'''
    global lora_dict
    subdirs, files = [], []
    for fn in os.scandir(lora_dir):
        if fn.is_dir():
            subdirs.append(f.path)
        if fn.is_file():
            if os.path.splitext(fn.name)[1].lower() in ext:                
                lora_dict[fn.name] = fn.path
    for dirs in list(subdirs):
        sd, fn = lora_scan(dirs, ext)
        subdirs.extend(sd)
        files.extend(fn)
    return subdirs, files

# Function get_lora_list().
def get_lora_list() -> list:
    '''Simple function for use with components.'''
    lora_list = []
    lora_scan(LORA_PATH, [".safetensors"])
    lora_list = list(lora_dict.keys())
    lora_list.sort(reverse=_SortDir)
    return lora_list

# Function on_ui_tabs().
def on_ui_tabs():
    '''Method on_ui_tabs()'''
    # Create a new block.
    with gr.Blocks(analytics_enabled=False) as ui_component:    
        # Create a new row. 
        with gr.Row():
            input_file = gr.Dropdown(choices=get_lora_list(), label="LoRA File List")
            create_refresh_button(input_file, get_lora_list,
                                  lambda: {"choices": get_lora_list()},
                                  "metadata_utils_refresh_1")
            sort_fw_bw = gr.Radio(choices=["Forward", "Backward"], value="Forward", 
                                  label="Sorting Direction", info="",
                                  scale=2, min_width=50)
            def change_sort_fw_bw(rb_state):
                global _SortDir
                _SortDir = False
                #out_state = "Forward"
                if rb_state == "Forward":
                    _SortDir = False
                    #out_state = "Forward"
                elif rb_state == "Backward":
                    _SortDir = True
                    #out_state = "Backward"
                #return [out_state]
                return []
            sort_fw_bw.change(change_sort_fw_bw, inputs=[sort_fw_bw], outputs=[])
        with gr.Row():
            arvalue = gr.Textbox(value="", lines=1, render=True,
                        interactive=False, inputs=None, label="",
                        info="Selected filename without extension"
                    )
        with gr.Row():
            arvalue = gr.Textbox(value="", lines=1, render=True,
                        interactive=False, inputs=None, label="",
                        info="Filename without extension from metadata"
                    )
        # Create a new row. 
        with gr.Row():
            json_output = gr.Code(lines=10, label="Metadata as JSON", language="json")
            input_file.input(
                fn=read_lora_metadata,
                inputs=[input_file],
                outputs=[json_output]
            )
    return [(ui_component, "Adjust Lora Filename", "adjust_lora_filename_tab")]

# Invoke a callback function. 
script_callbacks.on_ui_tabs(on_ui_tabs)

# Function get_lora_path().
def get_lora_path(lora_file: str) -> str:
    '''Get the path to the LoRA file.'''
    if not isinstance(lora_file, str):
        lora_file = ""
    if not os.path.isfile(os.path.join(LORA_PATH, lora_file)):
        return ""
    return os.path.join(LORA_PATH, lora_file)

# Function read_lora_metadata().
def read_lora_metadata(input_file: str) -> json:
    '''Read the LoRA metadata.'''
    print(get_lora_path(lora_dict.get(input_file)))
    if selected_model := get_lora_path(lora_dict.get(input_file)):
        if metadata := models.read_metadata_from_safetensors(selected_model):
            return json.dumps(metadata, indent=4, ensure_ascii=False)
        return "No metadata"
    return "No model"
