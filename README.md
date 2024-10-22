# sd-webui-adjust_lora_filename
#### Extension for the AUTOMATIC1111 Web UI

<p align="justify">sd-webui-adjust_lora_filename is an <i>Extension</i> for the <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui">AUTOMATIC1111</a> web UI. The <i>Extension</i> adjusts file name to output name in the metadata.</p>

---

## Preface

<p align="justify">As I have already written at another place, there is a problem if the LoRA file name without extension is different from the output name in the LoRA file itself. The name in the expression in a Prompt can be different from the stored file name. That can be irritating. The task of this <i>Extension</i> is to eliminate the difference.</p>

## Background

<p align="justify">A .safetensors files consist of a header and a binary part with the tensors. In the header there may be most of the time metadata. One tag of these metadata specifies the output filename. If the filename is not changed the output filename is equal to the filename.</p>

## What the Extension Does

<p align="justify">One can select a LoRA file from a dropdown menu. Sorting is possible in alphabetical forward and backward direction. The selected filename without extension is shown in a textbox on the left side. The output filename from the metadata is shown in a textbox on the right side. In parallel the JSON data is shown in textbox underneath. After clicking the Adjust button, the <i>Extension</i> tries to change the metadata tag, which is responsible for the output filename. Afterwards one can check clicking on the Update button, if the operation was successful.</p>

<a target="_blank" href=""><img src="./images/adjust_fn.png" alt="button panel"></a>

## Installation

The installation link is

```
https://github.com/zentrocdot/sd-webui-adjust_lora_filename
```

## Know Problem

<p align="justify">If a LoRA model is renamed on the harddisk, while AUTOMATIC1111 is running, old a new filename in the drop-down list. This has to be checked and corrected.</p>

# Reference

[1] https://github.com/AUTOMATIC1111/stable-diffusion-webui

[2] https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Extensions
