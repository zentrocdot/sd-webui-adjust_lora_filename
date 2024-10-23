# sd-webui-adjust_lora_filename
#### Extension for the AUTOMATIC1111 Web UI

<p align="justify">sd-webui-adjust_lora_filename is an <i>Extension</i> for the <a href="https://github.com/AUTOMATIC1111/stable-diffusion-webui">AUTOMATIC1111</a> web UI. The <i>Extension</i> adjusts the <i>file name</i> to the <i>output name</i> in the metadata.</p>

---

## Preface

<p align="justify">As I have already written at another place, there is a problem if the LoRA file name without extension is different from the output name in the metadata of the LoRA file itself. The name in the LoRa calling expression in a <i>Prompt</i> can be different from the stored file name. This can be irritating while using a LoRA. The task of this <i>Extension</i> is to eliminate the difference or discrepancy between the file names.</p>

## Background

<p align="justify">A <code>.safetensors</code> files consist of a <i>header</i> and a binary part with the tensors. In the <i>header</i> there may be most of the time <i>metadata</i>. One tag of these <i>metadata</i> specifies the output name. If the filename is not changed the output filename is equal to the filename.</p>

## What the Extension Does

<p align="justify">One can select a LoRA file from a dropdown menu. Sorting is possible in alphabetical forward and backward direction. The selected filename without extension is shown in a textbox on the left side. The output filename from the metadata is shown in a textbox on the right side. In parallel the JSON data is shown in textbox underneath. After clicking the Adjust button, the <i>Extension</i> tries to change the metadata tag, which is responsible for the output filename. Afterwards one can check clicking on the Update button, if the operation was successful.</p>

<a target="_blank" href=""><img src="./images/adjust_fn.png" alt="button panel"></a>

## Installation

The installation link is

```
https://github.com/zentrocdot/sd-webui-adjust_lora_filename
```

## Know Problem

<p align="justify">No problems known yet.</p>

# Reference

[1] https://github.com/AUTOMATIC1111/stable-diffusion-webui

[2] https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Extensions

<hr width="100%" size="2">

<p align="justify">There are various ways to support my work. One option is to purchase some of my extraordinary NFTs :smiley:. Some of my great collections can be found here:</p>

* https://opensea.io/collection/fantastic-mushroom-collection
* https://opensea.io/collection/cats-with-hats-collection-1
* https://opensea.io/collection/devil-woman-collection
* https://opensea.io/collection/cup-of-ice-no-1

<hr width="100%" size="2">

<p align="center">I loved the time when you could get also a hamburger :hamburger: for one Euro!</p>

<p align="center">
<a target="_blank" href="https://www.buymeacoffee.com/zentrocdot"><img src="\images\greeen-button.png" alt="Buy Me A Coffee" height="41" width="174"></a>
</p>
<hr width="100%" size="2">

<p align="justify">If you like what I present here, or if it helps you, or if it is useful, you are welcome to donate a small contribution or a cup of coffee. Or as you might say: Every TRON counts! Many thanks in advance! :smiley:</p>

<pre>TQamF8Q3z63sVFWiXgn2pzpWyhkQJhRtW7            (TRON)
DMh7EXf7XbibFFsqaAetdQQ77Zb5TVCXiX            (DOGE)
12JsKesep3yuDpmrcXCxXu7EQJkRaAvsc5            (BITCOIN)
0x31042e2F3AE241093e0387b41C6910B11d94f7ec    (Ethereum)</pre>
