from __future__ import annotations
import os
import json
import pandas as pd
from typing import Optional


def lesion_properties_from_annotations(
        df: pd.DataFrame,
        scan_id: Optional[str] = None,
        ) -> list[dict]:
    """Load specific properties from the annotations."""

    properties = []
    for region_attributes, coords in zip(
            df.region_attributes, df.region_shape_attributes):
        coords = json.loads(coords)
        x = coords['x']
        y = coords['y']
        w = coords['width']
        h = coords['height']

        # Some annotations had `undefined` values,
        # which JSON does not parse well without quotes.
        if 'undefined' in region_attributes:
            region_attributes = region_attributes.replace(
                'undefined', '"undefined"')

        region_attributes = json.loads(region_attributes)
        # If the lesion_id field exists and is set,
        # then set the lesion_id.
        lesion_id = ""
        if 'lesion_id' in region_attributes and \
                region_attributes['lesion_id'] != "":
            lesion_id = int(region_attributes['lesion_id'])

        annotator = ""
        if 'annotator' in region_attributes:
            annotator = region_attributes['annotator']

        properties.append(
            {
                'scan_id': scan_id,
                'x': x, 'y': y,
                'x2': x + w, 'y2': y + h,
                'width': w, 'height': h,
                'annotator': annotator,
                'lesion_id': lesion_id,
            }
        )

    return properties


def load_multiple_annotations(
            dir_multi_annotate: str
        ) -> dict[dict[pd.DataFrame]]:
    """Returns a dictionary of annotations for multiple readers.

        The returned dictionary contains a dictionary of dataframes.
        annotations.keys() -> list of annotaor IDs e.g., ['A1', 'A2']
        annotations['A1'].keys() -> list of scan IDs e.g., ['000', '009']
        annotations['A1']['000'] -> dataframe of annotations
                                    done by 'A1' for scan '000'
    """

    annotators = sorted(os.listdir(dir_multi_annotate))
    annotators = [ann for ann in annotators if not ann.startswith('.')]

    annotations = {}
    for annotator in annotators:
        dir_single_annotator = os.path.join(dir_multi_annotate, annotator)
        user_annotation_csvs = sorted(os.listdir(dir_single_annotator))
        user_annotations = {}
        for csv_name in user_annotation_csvs:
            csv_filepath = os.path.join(dir_single_annotator, csv_name)
            annotate_df = pd.read_csv(csv_filepath)
            lesion_properties = lesion_properties_from_annotations(annotate_df)
            scan_id, _ = csv_name.split('.')
            user_annotations[scan_id] = pd.DataFrame(lesion_properties)

        annotations[annotator] = user_annotations

    return annotations
