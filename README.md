# Bubble Prompter Extension for Stable Diffusion WebUI

This extension adds a Bubble Prompter functionality to the AUTOMATIC1111 Stable Diffusion web UI.

## Features

- Category-based word selection
- Random word addition
- Text processing utilities (replace spaces, clean commas, remove duplicates)
- Word emphasis and mitigation

## Installation

1. Clone this repository into the `extensions` folder of your Stable Diffusion WebUI installation:

git clone https://github.com/captainzero93/sd-webui-bubble-prompter.git

2. Restart the WebUI.

## Usage

1. Open the WebUI and navigate to the txt2img or img2img tab.
2. Expand the "Bubble Prompter" accordion.
3. Use the dropdowns to select categories and words.
4. Utilize the buttons to manipulate your prompt text.
5. Click "Process" to finalize your prompt.

## Files

- `scripts/bubble_prompter.py`: Main Python script for the extension
- `javascript/bubble_prompter.js`: JavaScript file for client-side functionality
- `styles.css`: CSS styles for the Bubble Prompter UI
- `install.py`: Installation script for required dependencies
- Various CSV files: Data files for categories and words

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements: 
https://huggingface.co/spaces/pols/Bubble_Prompter
