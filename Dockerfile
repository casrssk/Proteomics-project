# Dockerfile for proteomics_proj
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Install Tensorflow
RUN pip install --quiet --no-cache-dir \
    'tensorflow==2.2.0' && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN pip install umap-learn==0.3.10
RUN pip install pyteomics==4.1.2	

COPY ./internship.ipynb ./internship.ipynb
COPY ./results_train_mod_mass.csv ./results_train_mod_mass.csv
COPY ./results_valid_mod_mass.csv ./results_valid_mod_mass.csv
COPY ./results_test_mod_mass.csv ./results_test_mod_mass.csv
COPY ./results_yeast_mod_mass_new.csv ./results_yeast_mod_mass_new.csv
COPY ./test_mouse_10k.csv ./test_mouse_10k.csv
COPY ./Human.fasta ./Human.fasta
