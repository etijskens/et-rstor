========
et-rstor
========



Testing GPU programming on Leibniz

Leibniz has two nodes with two NVIDIA Tesla P100 GPUs each, so there is one Gpu per socket (which has 14 cores).

Requesting a gpu on Leibniz::

    >qsub -q gpu -l gpus=1 <jobscript>

or in the jobscript::

    #PBS -q gpu
    #PBS -l gpus=1

Requesting an interactive job::

    qsub -I -l walltime=2:00:00 -l nodes=1:ppn=20

modules needed::

    > ml calcua/2020a
    > ml GCC/9.3.0
    > ml CUDA/11.2.1

