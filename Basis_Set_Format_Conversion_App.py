import streamlit as st
import basis_set_exchange as bse
import os
import logging

# Set up logging for debugging purposes
logging.basicConfig(level=logging.INFO)

# --- Page Configuration ---
st.set_page_config(
    page_title='Basis Set Converter',
    layout='wide',
    page_icon="🧊",
    menu_items={
        'About': "# This online tool allows you to enter a basis set (and ECPs) in the form of text input for a variety of Quantum Chemistry softwares, and convert it to another format."
    }
)

# --- Sidebar Information ---
st.sidebar.write('# About')
st.sidebar.write('### *Powered by [Basis Set Exchange](https://github.com/MolSSI-BSE/basis_set_exchange)*')
st.sidebar.write('Basis Set Exchange (BSE) is a repository for quantum chemistry basis sets, which also provides a flexible and powerful API to facilitate reading/writing or converting basis sets.')
st.sidebar.write('[API Documentation for BSE](https://molssi-bse.github.io/basis_set_exchange/index.html)')
st.sidebar.write('The BSE library is available under the [BSD 3-Clause license](https://github.com/MolSSI-BSE/basis_set_exchange/blob/master/LICENSE)')

# --- Example Placeholders for Supported Formats ---
# Extend these as more formats are supported
placeholder_examples = {
    "cfour": '''# Example Cfour basis set for Hydrogen
H:aug-cc-pV5Z-DK
comment

  5
    0    1    2    3    4
    6    5    4    3    2
    9    5    4    3    2

402.0000000 60.2400000 13.7300000 3.9050000 1.2830000 
0.4655000 0.1811000 0.0727900 0.0207000 

0.0000000 0.0000000 0.0002836 0.0000000 0.0000000 0.00000000 
0.0000000 0.0000000 0.0021692 0.0000000 0.0000000 0.00000000 
0.0000000 0.0000000 0.0112082 0.0000000 0.0000000 0.00000000 
0.0000000 0.0000000 0.0448854 0.0000000 0.0000000 0.00000000 
1.0000000 0.0000000 0.1423120 0.0000000 0.0000000 0.00000000 
0.0000000 1.0000000 0.3309635 0.0000000 0.0000000 0.00000000 
0.0000000 0.0000000 0.4362734 1.0000000 0.0000000 0.00000000 
0.0000000 0.0000000 0.1764335 0.0000000 1.0000000 0.00000000 
0.00000000 0.00000000 0.00000000 0.00000000 0.00000000 1.0000000 

4.5160000 1.7120000 0.6490000 0.2460000 0.0744000 

1.0000000 0.0000000 0.0000000 0.0000000 0.00000000 
0.0000000 1.0000000 0.0000000 0.0000000 0.00000000 
0.0000000 0.0000000 1.0000000 0.0000000 0.00000000 
0.0000000 0.0000000 0.0000000 1.0000000 0.00000000 
0.00000000 0.00000000 0.00000000 0.00000000 1.0000000 

2.9500000 1.2060000 0.4930000 0.1560000 

1.0000000 0.0000000 0.0000000 0.00000000 
0.0000000 1.0000000 0.0000000 0.00000000 
0.0000000 0.0000000 1.0000000 0.00000000 
0.00000000 0.00000000 0.00000000 1.0000000 

2.5060000 0.8750000 0.2740000 

1.0000000 0.0000000 0.00000000 
0.0000000 1.0000000 0.00000000 
0.00000000 0.00000000 1.0000000 

2.3580000 0.5430000 

1.0000000 0.00000000 
0.00000000 1.0000000 
''',
    "molpro": '''! Example Molpro basis set for Hydrogen
spherical
basis={
!
! hydrogen             (9s,5p,4d,3f,2g) -> [6s,5p,4d,3f,2g]
s, H , 402.0000000, 60.2400000, 13.7300000, 3.9050000, 1.2830000, 0.4655000, 0.1811000, 0.0727900, 0.0207000
c, 5.5, 1.0000000
c, 6.6, 1.0000000
c, 1.8, 0.0002836, 0.0021692, 0.0112082, 0.0448854, 0.1423120, 0.3309635, 0.4362734, 0.1764335
c, 7.7, 1.0000000
c, 8.8, 1.0000000
c, 9.9, 1.0000000
p, H , 4.5160000, 1.7120000, 0.6490000, 0.2460000, 0.0744000
c, 1.1, 1.0000000
c, 2.2, 1.0000000
c, 3.3, 1.0000000
c, 4.4, 1.0000000
c, 5.5, 1.0000000
d, H , 2.9500000, 1.2060000, 0.4930000, 0.1560000
c, 1.1, 1.0000000
c, 2.2, 1.0000000
c, 3.3, 1.0000000
c, 4.4, 1.0000000
f, H , 2.5060000, 0.8750000, 0.2740000
c, 1.1, 1.0000000
c, 2.2, 1.0000000
c, 3.3, 1.0000000
g, H , 2.3580000, 0.5430000
c, 1.1, 1.0000000
c, 2.2, 1.0000000
}
'''
}

# --- Main Application UI ---
st.write('# Basis Set Format Converter')
st.write('This online tool allows you to enter a basis set in the form of text input for a variety of Quantum Chemistry softwares, and convert it to another format.')

col1, col2 = st.columns(2)

# --- INPUT COLUMN ---
col1.write('## INPUT')

input_format = col1.selectbox(
    'Select the input basis set format',
    tuple(placeholder_examples.keys()),
    index=0  # Default to cfour
)

# Dynamic placeholder based on selected input format
input_placeholder = placeholder_examples[input_format]

# File upload option
uploaded_file = col1.file_uploader("Upload your Basis Set file (.txt)", type=["txt"])
if uploaded_file:
    input_basis_str = uploaded_file.read().decode("utf-8")
else:
    input_basis_str = col1.text_area(
        label='Enter your own Basis Set here',
        value=input_placeholder,
        placeholder=f'Put your {input_format}-formatted basis set here',
        height=400
    )

# --- OUTPUT COLUMN ---
col2.write('## OUTPUT')

output_format = col2.selectbox(
    'Select the output basis set format',
    tuple(placeholder_examples.keys()),
    index=0
)

# --- Conversion Logic ---
output_basis_str = ""
basis_dict_bse = None
error_message = ""

if input_basis_str.strip():
    try:
        # Parse the input basis set using BSE
        logging.info(f"Attempting to read basis set in format: {input_format}")
        basis_dict_bse = bse.readers.read.read_formatted_basis_str(
            input_basis_str, basis_fmt=input_format
        )
        # Convert and write to the selected output format
        output_basis_str = bse.writers.write.write_formatted_basis_str(
            basis_dict_bse, fmt=output_format
        )
        logging.info("Conversion successful.")
    except Exception as e:
        error_message = (
            f"Error during conversion: {e}. "
            "Please check your input format, make sure it matches the selected input type, "
            "and consult the [BSE documentation](https://molssi-bse.github.io/basis_set_exchange/formats.html) if needed."
        )
        logging.error(error_message)

col2.text_area(
    label='Converted basis set in the format selected by you',
    value=(output_basis_str if not error_message else error_message),
    height=400
)

# Download button for converted output
if output_basis_str and not error_message:
    col2.download_button(
        label="Download Converted Basis Set",
        data=output_basis_str,
        file_name=f"converted_basis_set.{output_format}.txt",
        mime="text/plain",
    )

# --- Debug Mode Toggle ---
debug_mode = st.sidebar.checkbox("Show Debug Info (BSE JSON)", value=False)

if debug_mode:
    st.write('## Basis Set Exchange JSON Format (Debug)')
    if basis_dict_bse:
        st.write(basis_dict_bse)
    elif error_message:
        st.write(error_message)
