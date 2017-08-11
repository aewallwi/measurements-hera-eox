import numpy as np
import gainData.AntennaMeasurement as AM
import matplotlib.pyplot as plt

hybrid_coupler_A=AM('','hybrid_A_port_A_antenna',
                    'A_','','ANRITSU_CSV',
                    '1','2','3',0.05,0.25)
