import sys
import os

import SimpleITK as sitk
import numpy as np
import json


def mkdir(path):
    """create a single empty directory if it didn't exist

    Parameters:
        path (str) -- a single directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)


def save_itk_new(image, filename, origin, spacing, direction):
    if type(origin) != tuple:
        if type(origin) == list:
            origin = tuple(reversed(origin))
        else:
            origin = tuple(reversed(origin.tolist()))
    if type(spacing) != tuple:
        if type(spacing) == list:
            spacing = tuple(reversed(spacing))
        else:
            spacing = tuple(reversed(spacing.tolist()))
    if type(direction) != tuple:
        if type(direction) == list:
            direction = tuple(reversed(direction))
        else:
            direction = tuple(reversed(direction.tolist()))
    itkimage = sitk.GetImageFromArray(image, isVector=False)
    itkimage.SetSpacing(spacing)
    itkimage.SetOrigin(origin)
    itkimage.SetDirection(direction)
    sitk.WriteImage(itkimage, filename, True)


def load_itk_image_new(filename):
    itkimage = sitk.ReadImage(filename)
    numpyImage = sitk.GetArrayFromImage(itkimage)
    numpyOrigin = list(reversed(itkimage.GetOrigin()))
    numpySpacing = list(reversed(itkimage.GetSpacing()))
    numpyDirection = list(reversed(itkimage.GetDirection()))
    return numpyImage, numpyOrigin, numpySpacing, numpyDirection


def locate_lungbox(image, margin=5):
    xx, yy, zz = np.where(image)
    lung_boundingbox = np.array([[np.min(xx), np.max(xx)], [np.min(yy), np.max(yy)], [np.min(zz), np.max(zz)]])
    lung_boundingbox = np.vstack([np.max([[0, 0, 0], lung_boundingbox[:, 0] - margin], 0),
                                  np.min([np.array(image.shape), lung_boundingbox[:, 1] + margin], axis=0).T]).T
    lung_boundingbox = np.reshape(lung_boundingbox, newshape=(6,))
    return lung_boundingbox
