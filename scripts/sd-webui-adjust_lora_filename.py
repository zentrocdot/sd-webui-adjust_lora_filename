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
from typing import BinaryIO
from pathlib import Path
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

# --------------------
# Function lora_scan()
# --------------------
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

# ------------------------
# Function get_lora_list()
# ------------------------
def get_lora_list() -> list:
    '''Simple function for use with components.'''
    lora_list = []
    lora_scan(LORA_PATH, [".safetensors"])
    lora_list = list(lora_dict.keys())
    lora_list.sort(reverse=_SortDir)
    return lora_list

# ---------------------------
# Function read_header_data()
# ---------------------------
def read_header_data(file: BinaryIO) -> dict:
    '''Read header data from a given file.

    Parameter:
        file:   file to read from as binary
        return: header data as dict from json
    '''
    # Read the header size saved as little endian from first 8 bytes of file.
    header_size_bytes = file.read(8)
    # Convert the read little endian bytes to an integer.
    header_size_integer = int.from_bytes(header_size_bytes, byteorder='little')
    # Read the header data.
    header_data = file.read(header_size_integer)
    # Create the JSON data.
    json_data = json.loads(header_data)
    # Return the JSON data as dict.
    return json_data

# ---------------------------
# Function read_header_data()
# ---------------------------
def read_metadata(file_name: str) -> dict:
    """Read file to extract the metadata.

    Parameter:
        file_name: name of the file to be read
        return:    metadata as dict from json
    """
    def type_json(value):
        '''Return type of JSON substructure.'''
        try:
            return type(json.loads(value))
        except:
            pass
    # Create an empty dict.
    metadata = {}
    # Open binary file for radonly reading.
    with open(file_name, 'rb') as file:
        # Get the header data from the file.
        header_data = read_header_data(file)
    # Extract the metadata from the header.
    for key, value in header_data.get("__metadata__", {}).items():
        # Get value to key from metadata.
        metadata[key] = value
        # Check if value is of type string and if string is dict.
        if isinstance(value, str) and type_json(value) == dict:
            # Try to get the value as JSON data.
            try:
                metadata[key] = json.loads(value)
            except json.JSONDecodeError:
                pass
    # Return the metadata as dict.
    return metadata

# -------------------------
# Function write_metadata()
# -------------------------
def write_metadata(old_file_name: str, new_file_name: str, metadata: dict):
    '''Creates a new .safetensor file from given and modified file content and
    writes it with the modified metadata into a new file.

    Parameter:
        old_file_name: name of the original file
        new_file_name: name of the modified file
        metadata:      metadata as dict
    '''
    # Open a binary file for readonly reading.
    with open(old_file_name, 'rb') as old_file:
        # Extract the header data and the header size from the given file.
        old_header_data = read_header_data(old_file)
        # Overwrite the metadata in the header.
        old_header_data['__metadata__'] = metadata
        # Convert modified header data back to a binary string.
        new_header_data = json.dumps(old_header_data, separators=(',', ':')).encode('utf-8')
        # Open a new file for writing.
        with open(new_file_name, 'wb') as new_file:
            # Calculate the new offset value.
            offset = len(new_header_data)
            # Write the new offset value into the file.
            new_file.write(offset.to_bytes(8, 'little'))
            # Write the new header data into file.
            new_file.write(new_header_data)
            # Calculate chunk size based on buffer size for wrtiting the tensor to file.
            chunk_size = io.DEFAULT_BUFFER_SIZE
            # Read first chunk data for writing.
            chunk = old_file.read(chunk_size)
            # Write chunk data to file as long there is data.
            while chunk:
                # Write chunk data to the file.
                new_file.write(chunk)
                # Read the next new chunk data.
                chunk = old_file.read(chunk_size)

# ---------------------
# Function change_tag()
# ---------------------
def change_tag(old_filename: str, new_filename: str, value: str) -> None:
    '''Main script function.'''
    # Set the keys.
    key0 = "ss_output_name"
    key1 = "ss_tag_frequency"
    # Read the metadata from a given file.
    metadata = read_metadata(old_filename)
    # Update one entry in the metadata.
    metadata.update({key0: value})
    # Get the value for key ss_tag_frequency.
    temp_value = metadata.get(key1)
    #temp_value = json.dumps(temp_value, separators=(',', ':'))
    temp_value = json.dumps(temp_value)
    # Update one entry in the metadata.
    metadata.update({key1:temp_value})
    print(metadata)
    # Write the new file.
    write_metadata(old_filename, new_filename, metadata)
    # Check if both files have the same size.
    print(os.path.getsize(old_filename))
    print(os.path.getsize(new_filename))
    # Return None
    return None

# +++++++++++++++++++++
# Function on_ui_tabs()
# +++++++++++++++++++++
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
                if rb_state == "Forward":
                    _SortDir = False
                elif rb_state == "Backward":
                    _SortDir = True
                return []
            sort_fw_bw.change(change_sort_fw_bw, inputs=[sort_fw_bw], outputs=[])            
        with gr.Row():
            filename = gr.Textbox(value="", lines=1, render=True,
                                  interactive=False, inputs=None, label="",
                                  info="Selected filename without extension")
            outputname = gr.Textbox(value="", lines=1, render=True,
                                    interactive=False, inputs=None, label="",
                                    info="Filename without extension from metadata")
            gr.Button(value="Adjust")
            def get_basename(fn):
                fn = Path(fn).stem
                return fn
            def get_tagname(fn):
                metadata = read_metadata(fn)
                data = metadata.get("ss_output_name")
                return data
            input_file.input(fn=get_basename, inputs=[input_file], outputs=[filename])
            input_file.input(fn=get_tagname, inputs=[input_file], outputs=[outputname])
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

# ++++++++++++++++++++++++
# Function get_lora_path()
# ++++++++++++++++++++++++
def get_lora_path(lora_file: str) -> str:
    '''Get the path to the LoRA file.'''
    if not isinstance(lora_file, str):
        lora_file = ""
    if not os.path.isfile(os.path.join(LORA_PATH, lora_file)):
        return ""
    return os.path.join(LORA_PATH, lora_file)

# +++++++++++++++++++++++++++++
# Function read_lora_metadata()
# +++++++++++++++++++++++++++++
def read_lora_metadata(input_file: str) -> json:
    '''Read the LoRA metadata.'''
    print(get_lora_path(lora_dict.get(input_file)))
    if selected_model := get_lora_path(lora_dict.get(input_file)):
        if metadata := models.read_metadata_from_safetensors(selected_model):
            return json.dumps(metadata, indent=4, ensure_ascii=False)
        return "No metadata"
    return "No model"
