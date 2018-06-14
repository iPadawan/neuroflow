#!/bin/bash
docker run --rm kaczmarj/neurodocker:master generate docker \
           --base neurodebian:stretch-non-free \
           --pkg-manager apt \
           --install ants fsl gcc g++ graphviz tree git-annex-standalone less \
           --add-to-entrypoint "source /etc/fsl/fsl.sh" \
           --spm12 version=dev \
           --user=neuro \
           --miniconda miniconda_version="4.5.31" \
             conda_install="python=3.6 pytest jupyter jupyterlab jupyter_contrib_nbextensions traits pandas matplotlib seaborn nbformat nb_conda" \
             pip_install="https://github.com/nipy/nipype/tarball/master
                          https://github.com/INCF/pybids/tarball/master
                          nilearn datalad[full] nipy duecredit nbval" \
             create_env="neuro" \
             activate=True \
           --user=root \
           --run 'mkdir /data && chmod 777 /data && chmod a+s /data' \
           --run 'mkdir /templates && chmod 777 /templates && chmod a+s /templates' \
           --run 'mkdir /output && chmod 777 /output && chmod a+s /output' \
           --user=neuro \
           --copy templates "/templates" \
           --user=root \
           --run 'chown -R neuro /home/neuro' \
           --run 'rm -rf /opt/conda/pkgs/*' \
           --user=neuro \
           --run 'mkdir -p ~/.jupyter && echo c.NotebookApp.ip = \"0.0.0.0\" > ~/.jupyter/jupyter_notebook_config.py' \
           --workdir /home/neuro \
           --cmd "jupyter-notebook" > Dockerfile
