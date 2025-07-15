import streamlit as st
import basis_set_exchange as bse
import os

# Set page config
st.set_page_config(
    page_title='Basis Set Converter',
    layout='wide',
    page_icon="🧊",
    menu_items={
        'About': "# This online tool allows you to enter a basis set (and ECPs) in the form of text input for a variety of Quantum Chemistry softwares, and convert it to another format."
    }
)

# Sidebar stuff
st.sidebar.write('# About')
st.sidebar.write('### *Powered by [Basis Set Exchange](https://github.com/MolSSI-BSE/basis_set_exchange)*')
st.sidebar.write('Basis Set Exchange (BSE) is a repository for quantum chemistry basis sets, which also provides a flexible and powerful API to facilitate reading/writing or converting basis sets.')
st.sidebar.write('[API Documentation for BSE](https://molssi-bse.github.io/basis_set_exchange/index.html)')
st.sidebar.write('The BSE library is available under the [BSD 3-Clause license](https://github.com/MolSSI-BSE/basis_set_exchange/blob/master/LICENSE)')

# Main app
st.write('# Basis Set Format Converter')
st.write('This online tool allows you to enter a basis set in the form of text input for a variety of Quantum Chemistry softwares, and convert it to another format.')

placeholder_cfour_basis = ''# Example Cfour basis set for Hydrogen

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


col1, col2 = st.columns(2)
col1.write('## INPUT')
input_format = col1.selectbox(
    'Select the input basis set format',
    (
        'cfour',
         'molpro'
    ),
    index=0  # Default to cfour
)
input_basis_str = col1.text_area(
    label='Enter your own Basis Set here',
    value=placeholder_cfour_basis,
    placeholder='Put your Cfour-formatted basis set here',
    height=400
)
# Get rid of empty lines
input_basis_str = os.linesep.join([s for s in input_basis_str.splitlines() if s.strip()])

col2.write('## OUTPUT')
output_format = col2.selectbox(
    'Select the output basis set format',
    (
        'molpro',
        'cfour'
    ),
    index=0  # Default to molpro
)

# Only try to convert if there is some input
output_basis_str = ""
basis_dict_bse = None
error_message = ""
if input_basis_str.strip():
    try:
        # Parse and convert
        basis_dict_bse = bse.readers.read.read_formatted_basis_str(
            input_basis_str, basis_fmt=input_format
        )
        output_basis_str = bse.writers.write.write_formatted_basis_str(
            basis_dict_bse, fmt=output_format
        )
    except Exception as e:
        error_message = f"Error during conversion: {e}"

col2.text_area(
    label='Converted basis set in the format selected by you',
    value=(output_basis_str if not error_message else error_message),
    height=400
)


st.write('## Basis Set Exchange JSON Format')
st.write('For debugging')
if basis_dict_bse:
    st.write(basis_dict_bse)
elif error_message:
    st.write(error_message)
