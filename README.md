# Using Deep learning for alignment-free and error-tolerant identification of peptide sequences across different species. 


The implementation of the architectures and all steps needed for preprocessing the data, training, prediction and evaluation of the resulting models can be achived through these steps. 
Step 1: DeepNovo (ver:0.0.1) can be cloned from https://github.com/nh2tran/DeepNovo. The prerequisites for working this tool are (Python 2.7, TensorFlow 1.2 and Cython 0.22, Pyteomics ). 

Step 2: The command used to build Deepnovo_cython_setup taken from DeepNovo,
 python deepnovo_cython_setup.py build_ext –inplace

Step 3: A pre-trained model (yeast.low.coon_2013) was obtained from the link and tested. https://drive.google.com/open?id=0By9IxqHK5MdWalJLSGliWW1RY2c.
python deepnovo_main.py –-train_dir train.example –search_denovo

Step 4: After getting familiarised with the software, I used the modified forked version of DeepNovo provided by Tom Altenburgh, RKI (https://github.com/tondre/DeepNovo.git) and followed step 2 and step 3.

Step 5: Results from Deepnovo were compiled using data_preprocessing.py. This python code looks into the modifications and replaces I/L with all L in the predicted sequences. Secondly, it changes all Cmod to C, and all Qmod, Nmodand Mmod to Q, M, N respectively.

Step 6: For running the model, you need all the files named in docker file in the working directory and then you can build the docker image (docker build -f Dockerfile . -t proteomics_proj). Run docker image docker run -p 8888:8888 proteomics_proj:latest. 
