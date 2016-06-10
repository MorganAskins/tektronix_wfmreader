Software for Tektronic Oscilloscope
===================================

wfmread.py: Read binary wfm003 files for data analysis
- has the option to write to npz

To write to an npz file:

$ python wfmread.py file.wfm  
This will output a new file called file.npz  
This file can be read in through python and plotted with matplotlib as so:  

$ python  
```python
>>> import numpy as np
>>> import matplotlib.pyplot as plt
>>> data = np.load('file.npz')
>>> data.files
  ['voltage', 'timescale']
>>> waveforms = data['voltage']
>>> time = data['timescale']
## data['voltage'] is a list of all waveforms, you can read a single waveform
## by calling its element data['voltage'][0] (first waveform)
>>> plt.plot(time, waveforms[0])
>>> plt.show()
```

time_resolution.ipynb: Example analysis code using wfmread
