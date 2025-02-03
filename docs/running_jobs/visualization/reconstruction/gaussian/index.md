# Gaussian Splatting on HPC

## Overview


### The Individual Steps

**Processing with COLMAP**

```
module load contrib
module load chrisreidy/baylyd/colmap
start_colmap feature_extractor --database_path database.db --image_path images --ImageReader.camera_model SIMPLE_PINHOLE
start_colmap exhaustive_matcher --database_path database.db
start_glomap mapper --image_path images --database_path database.db --output_path sparse
```
**Resizing for training**

```
module load contrib
module load chrisreidy/baylyd/gaussian_splat
resize_images --skip_matching --resize --skip_undistort -s $PWD
```

**Actual Gaussian Splat Training**

```
singularity shell --nv /contrib/singularity/shared/baylyd/gaussian_splat/splat_colmap.sif
```

```
​​​​​​​/root/miniforge3/bin/mamba init
bash
mamba activate gaussian_splatting
cd /xdisk/chrisreidy/baylyd/gaussian_splat/gaussian-splatting/
python train.py -s ../../dianne_scanner_media/refreshing_memory/

```

