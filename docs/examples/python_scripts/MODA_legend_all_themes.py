#!/usr/bin/env python
# coding: utf-8

# ## **Displaying a legend with MODA elements for all MOCHADA themes in a single diagram**

# This example shows how to pack a legend (a.k.a colour key) showing all MODA elements, for each MOCHADA theme into a single svg image for easy comparison.

# In[1]:


import glob
import pathlib

import mochada_kit.running as mr


# <br>
# 
# Get the paths to all the MOCHADA themes in `mochada_kit/themes`

# In[2]:


theme_files = glob.glob(str(pathlib.Path("../themes/puml-theme-MOCHADA-*.puml")))
themes = [str(i).split("puml-theme-")[1][:-5] for i in theme_files]


# <br>
# 
# Make sure the theme based on the current working agreement (CWA) comes first in the list, and remove the themes "MOCHADA-plasma_A4w" and "MOCHADA-plasma_wide", if they are present - these themes look the same as "MOCHADA-plasma" in a colour key but have one parameter changed to make CHADA tables fit better onto an A4 page/wide screen.

# In[3]:


themes.remove("MOCHADA-CWA")
themes.insert(0, "MOCHADA-CWA")
for i in ["MOCHADA-plasma_A4w", "MOCHADA-plasma_wide"]:
    try:
        themes.remove(i)
    except ValueError:
        pass


# <br>
# 
# Now we write the same key (an activity element for each of the MODA elements with its corresponding stereotype) for each theme into a different "label" in the puml code file. There appears to be little control of placing the keys in rows and columns but this adjusts automatically as you add more themes.

# In[4]:


with open(pathlib.Path("../gallery/puml_code/legend_moda_all_themes.puml"), "w") as f:
    f.write("@startuml\n")

    for i, j in enumerate(themes):
        f.write(f"label l{i+1} [\n")
        f.write("{{\n")
        chada_blocks_uml  = f"""!theme {j} from ../../themes
title {j}
:User Case Input; <<user_case_input>>
split
  :Model; <<model>>
split again
  :Data Based Model; <<data_based_model>>
end split
:Raw Output; <<raw_output>>
:Processed Output; <<processed_output>>
"""

        f.write(chada_blocks_uml)
        f.write("}}\n]\n")

    f.write("@enduml\n")


# <br>
# 
# Finally we run the puml code to generate the svg diagram

# In[5]:


mr.run_plantuml_code(pathlib.Path("../gallery/puml_code/legend_moda_all_themes.puml"),
                     output_dir=pathlib.Path("../"))


# Here's the diagram:
# 
# <img src=../gallery/legend_moda_all_themes.svg>
