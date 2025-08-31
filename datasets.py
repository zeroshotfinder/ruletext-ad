from pathlib import Path
from box import Box
import json

def load_mvtec_loco_anomaly(path="./datasets/mvtec_loco_anomaly_detection"):
    dataset = Box(default_box=True)
    root_path = Path(path)
    train_good_dirs = list(root_path.glob("*/train/good"))

    for folder in train_good_dirs:
        object_name = folder.parents[1].stem
        for img_path in sorted(folder.glob("*.png"), key=lambda x: int(x.stem)):
            if not dataset.train[object_name]:
                dataset.train[object_name] = [img_path]
            else:
                dataset.train[object_name].append(img_path)

    test_dirs = list(root_path.glob("*/test/*"))

    for folder in test_dirs:
        anomaly_type = folder.stem
        object_name = folder.parents[1].stem

        for img_path in sorted(folder.glob("*.png"), key=lambda x: int(x.stem)):
            if not dataset.test[object_name][anomaly_type]:
                dataset.test[object_name][anomaly_type] = [img_path]
            else:
                dataset.test[object_name][anomaly_type].append(img_path)

    defects_files = list(root_path.glob("**/*.json"))

    for defect_file in defects_files:
        with open(defect_file, 'r') as f:
            defects = json.load(f)
            object_name = defect_file.parent.stem
            dataset.defects[object_name] = [" ".join(defect['defect_name'].split('_')) for defect in defects]

    return dataset