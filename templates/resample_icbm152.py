import sys
from os.path import join as opj
from nibabel import load
from nibabel.spaces import vox2out_vox
from nibabel.processing import resample_from_to

res = float(sys.argv[1])

fpath = 'mni_icbm152_nlin_asym_09c'

for nifti in ['1mm_brain.nii.gz',
              '1mm_mask.nii.gz',
              '1mm_T1.nii.gz',
              '1mm_tpm_csf.nii.gz',
              '1mm_tpm_gm.nii.gz',
              '1mm_tpm_wm.nii.gz']:

    img = load(opj(fpath, nifti))

    new_info = vox2out_vox(img, voxel_sizes=[res, res, res])

    img = resample_from_to(img, new_info)

    img.to_filename(opj(fpath, nifti).replace('1mm', '%smm' % res))
