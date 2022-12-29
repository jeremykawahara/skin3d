# Skin3D

![Skin3D Graphical Abstract](https://ars.els-cdn.com/content/image/1-s2.0-S1361841521003741-ga1_lrg.jpg "Graphical Abstract of our contributions")


<! --[![Skin3d](https://i.imgur.com/sFnqEME.png)](https://www.youtube.com/watch?v=8iErLS0bzY4 "Skin3d")
-->

 [Paper](https://www.sciencedirect.com/science/article/pii/S1361841521003741) | [Arxiv](https://arxiv.org/pdf/2105.00374.pdf) | [DOI](https://doi.org/10.1016/j.media.2021.102329) | [Video](https://www.youtube.com/watch?v=8iErLS0bzY4) 
:---:|:---:|:-----:

This is the official code repository for our paper, "[Skin3D: Detection and Longitudinal Tracking of Pigmented Skin Lesions in 3D Total-Body Textured Meshes](https://www.sciencedirect.com/science/article/pii/S1361841521003741)", published in Medical Imaging Analysis, 2021.

In this work, we propose an automated approach to detect and longitudinally track skin lesions on the skin surface of 3D total-body scans.
As there currently is no other large-scale publicly available dataset of 3D total-body skin lesions, we publicly release over `25,000` 3DBodyTex manual annotations, which we hope will further encourage research on total-body skin lesion analysis.

This repo provides the data for 3DBodyTex bounding boxes annotations, and shows how to visualize and use the code in your project.

If you use the data or any part of the code, please consider citing our work, and the original 3DBodyTex dataset.

```tex
@article{zhao2022skin3d,
  title={Skin3D: Detection and longitudinal tracking of pigmented skin lesions in 3D total-body textured meshes},
  author={Zhao, Mengliu and Kawahara, Jeremy and Abhishek, Kumar and Shamanian, Sajjad and Hamarneh, Ghassan},
  journal={Medical Image Analysis},
  volume={77},
  pages={102329},
  year={2022},
  publisher={Elsevier}
}
```
> Mengliu Zhao, Jeremy Kawahara, Kumar Abhishek, Sajjad Shamanian, Ghassan Hamarneh. "Skin3D: Detection and Longitudinal Tracking of Pigmented Skin Lesions in 3D Total-Body Textured Meshes," Medical Image Analysis. 2021. [[pdf](https://arxiv.org/abs/2105.00374)][[doi](https://doi.org/10.1016/j.media.2021.102329)][[video](https://www.youtube.com/watch?v=8iErLS0bzY4)]

## Download the Meshes

https://cvi2.uni.lu/datasets/

`3DBodyTex.v1` contains the meshes and can be downloaded from the external site linked above. 

The bounding boxes provided by `skin3d` correspond to the <b>high</b> resolution meshes.

## Installation Instructions

To use `skin3d`:

1. Fill out the form to request and download [3DBodyTex.v1](https://cvi2.uni.lu/datasets/)
2. Clone this repository: `git clone https://github.com/jeremykawahara/skin3d.git`
3. Navigate to the repository: `cd skin3d`
4. Create a new environment using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands): `conda create -n skin3d python=3.7`
5. Activate the environment: `conda activate skin3d`
6. Install the requirements: `pip install -r requirements.txt`

## Examples

We provide example notebooks to help explain the format of the data.

- [bodytex_annotations_data](https://github.com/jeremykawahara/skin3d/blob/master/notebooks/bodytex_annotations_data.ipynb) shows the format of the train, valid, and multiple annotator test data
- [bodytex_longitudinal_data](https://github.com/jeremykawahara/skin3d/blob/master/notebooks/bodytex_longitudinal_data.ipynb) shows the format of the IDs used to track the same lesion across scans
- [bodytex_annotations_visual](https://github.com/jeremykawahara/skin3d/blob/master/notebooks/bodytex_annotations_visual.ipynb) illustrates how to visualize multiple annotators on a texture image 

## Structure

This repository is structured as follows:

- [data/](https://github.com/jeremykawahara/skin3d/tree/master/data) contains the 25,000+ manual lesion annotations for 3DBodyTex
- [notebooks/](https://github.com/jeremykawahara/skin3d/tree/master/notebooks) contains example notebooks that load and process the annotations
- [skin3d/](https://github.com/jeremykawahara/skin3d/tree/master/skin3d) contains the Python package to load and process the annotations

## Related Publications
If you use this data or code, please cite the following works:

Description of the annotated bounding boxes:
> Mengliu Zhao, Jeremy Kawahara, Kumar Abhishek, Sajjad Shamanian, Ghassan Hamarneh. "Skin3D: Detection and Longitudinal Tracking of Pigmented Skin Lesions in 3D Total-Body Textured Meshes," Medical Image Analysis. 2021. [[pdf](https://arxiv.org/abs/2105.00374)][[doi](https://doi.org/10.1016/j.media.2021.102329)]

Description of the meshes:
> Saint, A., Ahmed, E., Shabayek, A. E. R., Cherenkova, K., Gusev, G., Aouada, D., & Ottersten, B. (2018). "3DBodyTex: Textured 3D body dataset". International Conference on 3D Vision, 495–504. [[doi]](https://doi.org/10.1109/3DV.2018.00063) [[pdf]](https://core.ac.uk/download/pdf/162022926.pdf)
