# sd-webui-adjust_lora_filename
#### Extension for the AUTOMATIC1111 Web UI

<p align="justify">sd-webui-aspect_ratios-dd is an <i>Extension</i> for the <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui">AUTOMATIC1111</a>.</p>

---

## Preface

As I have already written earlier, there is a problem if the file name without extension is different from the output name in the LoRA file. The name in the expression can be different from the file name. That can be irritating.

## What the Extension Does

One can select a LoRA file from a dropdown menu. Sorting is possible in alphabetical forward and backward direction. The selected filename without extension is shown in a textbox on the left side. The filename from the metadata is shown in a textbox on the right side. in parallel the JSON data is shown in textbox underneath. After clicking the Adjust button, the Extension tries to change the metadata tag, which is responsible for the filename. Afterwards one can check clicking on the Update button, if the operation was successful.

<a target="_blank" href=""><img src="./images/adjust_fn.png" alt="button panel"></a>

## Know Problem

<p align="justify">If a LoRA model is renamed on the harddisk, while AUTOMATIC1111 is running, old a new filename in the drop-down list. This has to be checked and corrected.</p>

# Reference

to-do ...
