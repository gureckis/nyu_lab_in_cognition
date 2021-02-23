import numpy.random as npr
import numpy as np
import pandas as pd

# little code to generate the data... not required to run this as data has been stored in a file already
npr.seed(10)
b_0=-9
b_1=4
x = npr.uniform(0, 4, size=(40,))
e=np.exp(b_0+b_1*x)
p = e/(1.0+e)
nyu_df=pd.DataFrame({'student':range(40), 'gpa': x, 'admit': npr.binomial(1, p)})
nyu_df.to_csv('nyu_admission_fake.csv', index=False)