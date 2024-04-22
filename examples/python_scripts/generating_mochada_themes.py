#!/usr/bin/env python
# coding: utf-8

# # **Generating bespoke MOCHADA themes for MODA and/or CHADA diagrams and tables**

# - This example shows how to generate several bespoke plantuml MOCHADA themes (i.e. for MODA and/or CHADA) with 4 or 5 different colours from various colormaps available in matplotlib.
# - These are all the MOCHADA themes in the `mochada_kit/themes`folder

# First, we import the necessary modules:

# In[1]:


import pathlib

import numpy as np
import matplotlib as mpl


# <br>
# 
# #### **1. How many colours do we need?**

# For **CHADA**, there are 5 different types of elements, for which we need a stereotype:
# 
# 1. User Case
# 2. Experiment
# 3. Raw Data
# 4. Data Processing
# 5. Final Data
# 
# For **MODA**, there are 4 different types of elements, for which we need an individual stereotype but which match closely to the CHADA elements, meaning that the same colours can be used:
# 1. User Case Input
# 2. Model
# 3. Raw Output
# 4. Processed Output
# 
# and a fifth one, which does not have an equivalent in CHADA and needs an independent colour - in the [current working agreement](https://emmc.eu/moda/) it is yellow, but as this colour appears in some of the colormaps, we will use a colour gradient between two of the other colours to distinguish this element:
# 
# 5. Data Based Model

# <br>
# 
# We will produce themes with two different options for the colours:
# 
# - themes with four different colours for CHADA elements 1-4. Element 5 will have the same colour as 4 but with an additional blue line around it. MODA elements 1-4 will have the same colours as the corresponding CHADA elements. MODA element 5 will have a colour gradient between two of the other colours.
# - themes with five different colours for CHADA elements 1-5 (element 5 will not have a blue line around it). MODA elements 1-4 will have the same colours as the corresponding CHADA elements. MODA element 5 will have a colour gradient between two of the other colours.

# <br>
# 
# #### **2. Selecting and sampling different colormaps**

# Now we need to select some colormaps and extract four or five different colours from them.
# 
# Here, I have chosen some perceptually uniform colormaps (viridis, plasma and cividis), which also have the advantage that they do not contain both red and green colours, meaning that they should be clearly visible to a wider range of people. I have also chosen a number of other colormaps which I thought may be applicable to MODA/CHADA diagrams. You can see all the colormaps available in matplotlib [here](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
# 
# Another option is to simply choose 4 or 5 colours and apply those.

# In[2]:


colormaps = ['viridis', 'plasma', 'cividis', 'PiYG', 'RdBu',
             'coolwarm', 'bwr', 'seismic', 'Set1', 'Set2',
             'jet', 'rainbow']


# Now we select colours from the colormaps by sampling them at intervals between 0 and 1:

# In[3]:


theme_colors = {}

for cm in colormaps:
    cm_c = mpl.colormaps[cm]
    theme_colors[cm] = [mpl.colors.to_hex(cm_c(i)) for i in np.linspace(0.0, 1.0, 4)]
    theme_colors[cm + "_5"] = [mpl.colors.to_hex(cm_c(i)) for i in np.linspace(0.0, 1.0, 5)]

# there are five different stereotypes, so for the themes with four colors
# we need to repeat the last color once
for k, v in theme_colors.items():
    if not k[-2:] == "_5":
        v.append(v[-1])


# <br>
# 
# #### **3. Read the template on which all the themes are based**

# Now we read theme template, which was created manually and is based on the colours in the [current working agreement](http://characterisation.eu/publications-output/)
# 
# You can inspect this file in a text editor to see it's structure. There are also some comment lines in the file giving further explanations.

# In[4]:


with open(pathlib.Path("../themes/puml-theme-MOCHADA-CWA.puml"), "r") as f:
    d = f.readlines()


# Get the lines that don't change

# In[5]:


mid = list(d[25:34])
end = list(d[58:])


# If we have 5 colours, we don't apply a blue line to the final CHADA element

# In[6]:


end_5 = list(end)
end_5.remove('  LineColor $FINAL_DATA_LINECOLOR\n')
end_5.remove('  LineThickness $FINAL_DATA_LINETHICKNESS\n',)


# <br>
# 
# #### **4. Define some necessary parameters**

# Define basic headers

# In[7]:


h4 = ["''\n",
      "'' Theme for MODA and CHADA diagrams, based on four colors from the plasma\n",
      "'' colormap in matplotlib.\n",
      "'' The colormap was evaluated at 0, 0.333, 0.667 and 1 to obtain the colours.\n",
      "''\n"]

h5 = ["''\n",
      "'' Theme for MODA and CHADA diagrams, based on five colors from the plasma\n",
      "'' colormap in matplotlib.\n",
      "'' The colormap was evaluated at 0, 0.25, 0.5, 0.75 and 1 to obtain the colours.\n",
      "''\n"]

hpu = ["'' This is a perceptually uniform colormap which does not contain\n",
       "'' both red and green colours and should therefore be suitable for\n",
       "'' people who have difficulty distinguishing those colours\n",
       "''\n"]


# Now, specify the font colours for the text on the various elements in each theme. I chose these manually having inspected the output.

# In[8]:


font_colors = {'viridis': ["White", "White", "White", "Black", "Black"],
               'viridis_5': ["White", "White", "White", "Black", "Black"],
               'plasma': ["White", "White", "White", "Black", "Black"],
               'plasma_5': ["White", "White", "White", "Black", "Black"],
               'cividis': ["White", "White", "White", "Black", "Black"],
               'cividis_5': ["White", "White", "White", "Black", "Black"],
               'PiYG': ["White", "Black", "Black", "White", "White"],
               'PiYG_5': ["White", "Black", "Black", "Black", "White"],
               'RdBu': ["White", "Black", "Black", "White", "White"],
               'RdBu_5': ["White", "Black", "Black", "Black", "White"],
               'coolwarm': ["White", "Black", "Black", "White", "White"],
               'coolwarm_5': ["White", "Black", "Black", "Black", "White"],
               'bwr': ["White", "Black", "Black", "White", "White"],
               'bwr_5': ["White", "Black", "Black", "Black", "White"],
               'seismic': ["White", "White", "Black", "White", "White"],
               'seismic_5': ["White", "White", "Black", "Black", "White"],
               'Set1': ["White", "White", "White", "White", "White"],
               'Set1_5': ["White", "White", "White", "White", "White"],
               'Set2': ["White", "White", "White", "White", "White"],
               'Set2_5': ["White", "White", "White", "White", "White"],
               'jet': ["White", "Black", "Black", "White", "White"],
               'jet_5': ["White", "Black", "Black", "White", "White"],
               'rainbow': ["White", "Black", "Black", "White", "White"],
               'rainbow_5': ["White", "Black", "Black", "White", "White"]
               }


# <br>
# 
# #### **5. Compile the themes**

# Now we compile the themes and write them to file in `mochada_kit/themes`. We only need to change the definition block "def_block" in the theme file. The part of the file which contains the css syle block is lower down in the file and the values from the def_block are automatically transferred to the css style block

# In[9]:


for k, v in theme_colors.items():
    if k[-2:] == "_5":
        header = list(h5)
        end_block = end_5
        h1 = f"'' Theme for MODA and CHADA diagrams, based on five colors from the {k}\n"
    else:
        header = list(h4)
        end_block = end
        h1 = f"'' Theme for MODA and CHADA diagrams, based on four colors from the {k}\n"

    header[1] = h1

    if k[:4] in ["viri", "plas", "civi"]:
        header = header[:-1] + hpu


    def_block = [f'!$PUML_THEME = "MOCHADA-{k}"\n',
                 f'!$THEME      = "MOCHADA-{k}"\n',
                 '!$OVERVIEW_BACKGROUNDCOLOR = Gray\n',
                 '!$OVERVIEW_FONTCOLOR = White\n',
                 f'!$USER_CASE_BACKGROUNDCOLOR = "{v[0]}"\n',
                 f'!$USER_CASE_FONTCOLOR = {font_colors[k][0]}\n',
                 f'!$EXPERIMENT_BACKGROUNDCOLOR = "{v[1]}"\n',
                 f'!$EXPERIMENT_FONTCOLOR = {font_colors[k][1]}\n',
                 f'!$RAW_DATA_BACKGROUNDCOLOR = "{v[2]}"\n',
                 f'!$RAW_DATA_FONTCOLOR = {font_colors[k][2]}\n',
                 f'!$DATA_PROCESSING_BACKGROUNDCOLOR = "{v[3]}"\n',
                 f'!$DATA_PROCESSING_FONTCOLOR = {font_colors[k][3]}\n',
                 f'!$USER_CASE_INPUT_BACKGROUNDCOLOR = "{v[0]}"\n',
                 f'!$USER_CASE_INPUT_FONTCOLOR = {font_colors[k][0]}\n',
                 f'!$MODEL_BACKGROUNDCOLOR = "{v[1]}"\n',
                 f'!$MODEL_FONTCOLOR = {font_colors[k][1]}\n',
                 f'!$RAW_OUTPUT_BACKGROUNDCOLOR = "{v[2]}"\n',
                 f'!$RAW_OUTPUT_FONTCOLOR = {font_colors[k][2]}\n',
                 f'!$PROCESSED_OUTPUT_BACKGROUNDCOLOR = "{v[3]}"\n',
                 f'!$PROCESSED_OUTPUT_FONTCOLOR = {font_colors[k][3]}\n',
                 f'!$DATA_BASED_MODEL_BACKGROUNDCOLOR = "{v[4]}-{v[1]}"\n',
                 f'!$DATA_BASED_MODEL_FONTCOLOR = {font_colors[k][0]}\n',
                 f'!$FINAL_DATA_BACKGROUNDCOLOR = "{v[4]}"\n',
                 f'!$FINAL_DATA_FONTCOLOR = {font_colors[k][4]}\n'
                 ]

    theme_str = ''.join(header + mid + def_block + end_block)

    with open(pathlib.Path(f"../themes/puml-theme-MOCHADA-{k}.puml"), "w") as f:
        f.write(theme_str)

