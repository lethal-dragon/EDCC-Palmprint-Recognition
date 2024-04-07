# Copyright (c) 2019 leosocy. All rights reserved.
# Use of this source code is governed by a MIT-style license
# that can be found in the LICENSE file.

import os
import edcc
from itertools import combinations

# TEST_PALMPRINT_DATA_DIR = "../../palmprint_data"
# TEST_A_01_PALMPRINT_IMAGE = os.path.join(TEST_PALMPRINT_DATA_DIR, "a_01.bmp")
# TEST_A_02_PALMPRINT_IMAGE = os.path.join(TEST_PALMPRINT_DATA_DIR, "a_02.bmp")
# TEST_B_01_PALMPRINT_IMAGE = os.path.join(TEST_PALMPRINT_DATA_DIR, "b_01.bmp")
# TEST_B_02_PALMPRINT_IMAGE = os.path.join(TEST_PALMPRINT_DATA_DIR, "b_02.bmp")
#
#
# if __name__ == "__main__":
#     config = edcc.EncoderConfig(29, 5, 5, 10)
#     encoder = edcc.create_encoder(config)
#     one_palmprint_code = encoder.encode_using_file(TEST_A_01_PALMPRINT_IMAGE)
#     another_palmprint_code = encoder.encode_using_file(TEST_A_02_PALMPRINT_IMAGE)
#     similarity_score = one_palmprint_code.compare_to(another_palmprint_code)
#     print(
#         "{} <-> {} similarity score:{}".format(
#             TEST_A_01_PALMPRINT_IMAGE, TEST_A_02_PALMPRINT_IMAGE, similarity_score
#         )
#     )

LEFT_HAND_DIR = "/Users/freehk./Documents/GitHub/EDCC-Palmprint-Recognition/IITD Palmprint V1/Segmented/Left"
RIGHT_HAND_DIR = "/Users/freehk./Documents/GitHub/EDCC-Palmprint-Recognition/IITD Palmprint V1/Segmented/Right"
OUTPUT_FILE = "/Users/freehk./Documents/GitHub/EDCC-Palmprint-Recognition/IITD Palmprint V1/similarity_scores.txt"

subjects_left = {}
subjects_right = {}

for filename in os.listdir(LEFT_HAND_DIR):
    if filename.endswith(".bmp"):
        subject_id = filename.split('_')[0]
        if subject_id not in subjects_left:
            subjects_left[subject_id] = []
        subjects_left[subject_id].append(os.path.join(LEFT_HAND_DIR, filename))

for filename in os.listdir(RIGHT_HAND_DIR):
    if filename.endswith(".bmp"):
        subject_id = filename.split('_')[0]
        if subject_id not in subjects_right:
            subjects_right[subject_id] = []
        subjects_right[subject_id].append(os.path.join(RIGHT_HAND_DIR, filename))

if __name__ == "__main__":
    config = edcc.EncoderConfig(29, 5, 5, 10)
    encoder = edcc.create_encoder(config)

    with open(OUTPUT_FILE, "w") as f:
        # For each hand side, write a line to the file to indicate the start of the comparisons for that hand side.
        for hand_dict, hand_name in [(subjects_left, 'Left'), (subjects_right, 'Right')]:
            f.write(f"Now starting {hand_name} hand comparisons:\n")
            for subject_id, images in hand_dict.items():
                for image1, image2 in combinations(images, 2):
                    image1_code = encoder.encode_using_file(image1)
                    image2_code = encoder.encode_using_file(image2)
                    similarity_score = image1_code.compare_to(image2_code)
                    # Write the similarity score to the output file.
                    f.write(
                        "{} <-> {} similarity score:{}\n".format(
                            os.path.relpath(image1, LEFT_HAND_DIR if hand_name == 'Left' else RIGHT_HAND_DIR),
                            os.path.relpath(image2, LEFT_HAND_DIR if hand_name == 'Left' else RIGHT_HAND_DIR),
                            similarity_score
                        ))

