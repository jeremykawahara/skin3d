import os
import pandas as pd
from PIL import Image
from typing import Optional, List
from skin3d.annotate import (
     lesion_properties_from_annotations,
)


class BodyTexDataset:
    """3DBodyTex dataset with manual annotations.

        Args:
            df: Data-frame summarizing the BodyTex dataset.
            dir_annotate: String indication the directory containing
                the single manual annotations.
            dir_multi_annotate: String indicating the directory
                containing the test manual annotations of multiple annotators.
            dir_textures: Optional string indicating the directory of the
                meshes' texture images.
    """

    def __init__(
            self,
            df: pd.DataFrame,
            dir_annotate: str = '../data/3dbodytex-1.1-highres/annotations/',
            dir_multi_annotate: str = '../data/3dbodytex-1.1-highres/multiple_annotators/',
            dir_textures: Optional[str] = None,
            ):

        self.df = df
        self.dir_annotate = dir_annotate
        self.dir_multi_annotate = dir_multi_annotate
        self.dir_textures = dir_textures

    def annotated_scan_ids(self, partition: str) -> List[str]:
        """Return the annotated scan IDs of the given `partition`."""
        return list(
            self.annotated_samples_in_partition(partition).scan_id.values)

    def scan_row(self, scan_id: str) -> pd.DataFrame:
        """Return the row corresponding to the `scan_id`.

            Raises:
                ValueError: Raises if multiple records correspond
                    to the `scan_id`.
        """
        scan_row = self.df[self.df.scan_id == scan_id]
        if len(scan_row) > 1:
            raise ValueError(
                "Multiple rows returned. `scan_id` should be unique.")

        return scan_row

    def texture_filepath(
            self, scan_id: str, highres: bool = True) -> str:
        """Return the filepath to the texture image for the given `scan_id`.

        Args:
            scan_id (string): A string representing scan identifier
                (i.e., `self.df.scan_id`).
            highres (bool, optional): If True, returns the filepath
                to the high-resolution image.
                Else, returns the filepath to the low-resolution image.
                This assumes you correctly set the `self.dir_textures`
                to the directory containing the low or high-resolution images

        Returns:
            string: Filepath to the texture image.
        """
        scan_row = self.scan_row(scan_id)

        if highres:
            image_name = 'model_highres_0_normalized.png'
        else:
            image_name = 'model_lowres_0_normalized.png'

        folder_filename = os.path.join(
            scan_row.scan_name.values[0], image_name)

        if self.dir_textures is None:
            return folder_filename
        else:
            return os.path.join(self.dir_textures, folder_filename)

    def annotation_filepath(
            self,
            scan_id: int,
            annotator: Optional[str] = None,
            ) -> str:
        """Return the path to the annotation CSV."""

        filepath = scan_id + '.csv'

        if annotator is None:
            filepath = os.path.join(self.dir_annotate, filepath)
        else:
            filepath = os.path.join(
                self.dir_multi_annotate, annotator, filepath)

        return filepath

    def annotation(
            self,
            scan_id: str,
            annotator: Optional[str] = None,
            ) -> pd.DataFrame:
        """Return a dataframe for the annotations of `scan_id`.

            If `annotator` is None, then return
                the annotations in `self.dir_annotate`.
            If `annotator` is not None, then return
                the annotations for `scan_id` for the given `annotator`.
                Specifically, this gets the annotations
                in `self.dir_multi_annotate/` + `annotator`,
                which corresponds to the test set annotations
                done by `annotator`.
        """

        annotated_df = pd.read_csv(
            self.annotation_filepath(scan_id=scan_id, annotator=annotator),
        )
        ann_properties = lesion_properties_from_annotations(
            annotated_df, scan_id)

        return pd.DataFrame(ann_properties)

    def annotations(
            self,
            scan_ids: List[str],
            annotator: Optional[str] = None,
            ) -> pd.DataFrame:
        """Return a dataframe of all annotations for the given `scan_ids`."""
        all_ann_dfs = []
        for scan_id in scan_ids:
            ann = self.annotation(scan_id=scan_id, annotator=annotator)
            all_ann_dfs.append(ann)

        return pd.concat(all_ann_dfs)

    def texture_image(self, scan_id: str) -> Image:
        """Return the texture image corresponding to `scan_id`."""
        img_path = self.texture_filepath(scan_id=scan_id)
        img = Image.open(img_path).convert("RGB")
        return img

    def annotation_ids_in_partition(self, partition: str) -> List[str]:
        partition_ids = self.annotated_samples_in_partition(
            partition=partition).scan_id.values

        return list(partition_ids)

    def annotated_samples_in_partition(self, partition: str) -> pd.DataFrame:
        """Return the selected annotated samples belonging to the `partition`.

        We select a subset of the rows (i.e., scans) to annotate
        and include in our experiments.

        Args:
            partition (string): A string indicating the partition.
                Corresponds to `self.df.partition`.

        Returns:
            DataFrame: The rows assigned to the partition
                that were selected to be studied in the experiment.
        """
        is_partition = (self.df.partition == partition).values
        is_selected = self.df.selected.values
        return self.df[is_partition & is_selected]

    def summary(self):
        """Print summary statistics of the annotations."""
        train_ids = self.annotated_scan_ids('train')
        valid_ids = self.annotated_scan_ids('valid')
        test_ids = self.annotated_scan_ids('test')
        long_ids = self.annotated_scan_ids('long')
        scan_ids = train_ids + valid_ids + test_ids + long_ids

        # Load the single annotator annotations.
        annotations_single = self.annotations(scan_ids)

        # Load the multiple annototators' test annotations.
        a1 = self.annotations(test_ids, annotator='A1')
        a2 = self.annotations(test_ids, annotator='A2')
        a3 = self.annotations(test_ids, annotator='A3')

        # Combine all annotations into a single data-frame to compute stats.
        annotations = annotations_single.append([a1, a2, a3])

        print("Number of scans annotated with lesions: {}".format(
            len(scan_ids)))
        print("Number of annotated training scans: {}".format(len(train_ids)))
        print("Number of annotated validation scans: {}".format(
            len(valid_ids)))
        print("Number of annotated testing scans: {}".format(len(test_ids)))
        print("Number of annotated longitudinal scans: {}".format(
            len(long_ids)))
        print("Total number of lesions annotated: {}".format(
            len(annotations)))
        print("Average annotated lesion width={:.2f}, height={:.2f}".format(
            annotations.width.mean(), annotations.height.mean()))
