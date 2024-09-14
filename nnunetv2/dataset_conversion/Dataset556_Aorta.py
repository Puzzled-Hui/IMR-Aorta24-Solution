# -*- coding: utf-8 -*-

'''
Program :   
Author  :   Minghui Zhang, sjtu
File    :   Dataset556_Aorta.py
Date    :   2024/8/1 14:55
Version :   V1.0
'''
from batchgenerators.utilities.file_and_folder_operations import *
import shutil
from nnunetv2.dataset_conversion.generate_dataset_json import generate_dataset_json
from nnunetv2.paths import nnUNet_raw


if __name__ == '__main__':

    task_name='Aorta24'
    amos_base_dir = "/mnt/data/ZMH/data/nnUNet_raw/nnUNet_raw_data/Task557_Aorta/"
    out_base = "/mnt/data/ZMH/data/nnUNetV2/nnUNet_raw/Dataset558_Aorta24/"

    dataset_json_source = load_json(join(amos_base_dir, 'dataset.json'))
    imagestr = join(out_base, "imagesTr")
    imagests = join(out_base, "imagesTs")
    labelstr = join(out_base, "labelsTr")
    maybe_mkdir_p(imagestr)
    maybe_mkdir_p(imagests)
    maybe_mkdir_p(labelstr)

    training_identifiers = [i['image'].split('/')[-1][:-7] for i in dataset_json_source['training']]
    print(training_identifiers)
    for tr in training_identifiers:
        shutil.copy(join(amos_base_dir, 'imagesTr', tr + '_0000.nii.gz'), join(imagestr, f'{tr}_0000.nii.gz'))
        shutil.copy(join(amos_base_dir, 'labelsTr', tr + '.nii.gz'), join(labelstr, f'{tr}.nii.gz'))

    test_identifiers = [i.split('/')[-1][:-7] for i in dataset_json_source['test']]
    print(test_identifiers)
    for ts in test_identifiers:
        shutil.copy(join(amos_base_dir, 'imagesTs', ts + '_0000.nii.gz'), join(imagests, f'{ts}_0000.nii.gz'))

    generate_dataset_json(out_base, {0: "CTA"},
                          labels={v: int(k) for k, v in dataset_json_source['labels'].items()},
                          num_training_cases=len(training_identifiers), file_ending='.nii.gz',
                          dataset_name=task_name, reference='None',
                          release='None',
                          description="Aorta24")