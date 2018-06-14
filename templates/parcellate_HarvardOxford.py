import os
import nibabel as nb
import numpy as np
from os.path import join as opj

template_path = '/usr/share/data/harvard-oxford-atlases/HarvardOxford'

output_path = '/media/line/mindhive/Dropbox/research/88_templates'

# Load cortical segmentation
cort_nii = nb.as_closest_canonical(
    nb.load(opj(template_path, 'HarvardOxford-cortl-maxprob-thr0-1mm.nii.gz')))
cort = cort_nii.get_data()

# Load subcortical segmentation
subc_nii = nb.as_closest_canonical(
    nb.load(opj(template_path, 'HarvardOxford-sub-maxprob-thr0-1mm.nii.gz')))
subc = subc_nii.get_data()
subc[subc > 0 ] += 100

# Load labels
with open('HarvardOxford_label.csv', 'r') as f:
    rois = f.readlines()

# Write Binary ROIs into output folder
output_dir = opj(output_path, 'HarvardOxford_Masks')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for r in rois:

    temp = r.split(',')
    roi_id = int(temp[0])
    roi_name = temp[1][:-1]

    if roi_id < 100:
        data = cort==roi_id
        aff = cort_nii.affine
        hdr = cort_nii.header

    else:
        data = subc==roi_id
        aff = subc_nii.affine
        hdr = subc_nii.header

    hdr.set_data_dtype(np.uint8)
    output_filename = opj(output_dir, '%s.nii.gz' % roi_name)
    nb.Nifti1Image(data.astype(np.uint8), aff, hdr).to_filename(output_filename)
