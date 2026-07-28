from enum import Enum
import os
# python 3.11 only supports StrEnum natively
# so we define our own for compatibility with 3.8+
class StrEnum(str, Enum):
    pass

class RegionName(StrEnum):
    NETC = "NON-ENHANCING TUMOR CORE (NETC)"
    ET = "ENHANCING TUMOR (ET)"
    SNFH = "SURROUNDING NON-ENHANCING FLAIR HYPERINTENSITY (SNFH)"
    GTV = "GROSS TUMOR VOLUME (GTV)"
    NET = "NON-ENHANCING TUMOR (NET)"
    ED = "EDEMA (ED)"
    RC = "RESECTION CAVITY (RC)"
    

class TaskName(StrEnum):
      gli = "Pre- and Post-Treatment Adult Glioma"
      menrt = "Pre-Radiotherapy Meningioma (BraTS-MEN-RT)"
      peds = "Pre-Treatment Pediatric Glioma (BraTS-PED)"

    
DUMMY_DIR = "BraTS-PED-00019-000"

#DOCKER_TASK_DICT = {task.value: f"aparida12/brats2025:{task.name}" for task in TaskName}

DOCKER_TASK_DICT = {
    TaskName.gli.value:    ("aparida12/brats2025:gli",            "/input/", "ro"),
    TaskName.menrt.value: ("aparida12/brats2025:menrt",          "/input/", "ro"),
    TaskName.peds.value:    ("aparida12/brats2025:peds",           "/input/", "ro")
}

DOCKER_OUTPUT = {
    TaskName.gli.value:   ("output_dir", f"{DUMMY_DIR}.nii.gz"),
    TaskName.menrt.value:   ("output_dir", f"{DUMMY_DIR}.nii.gz"),
    TaskName.peds.value:  ("output_dir", f"{DUMMY_DIR}.nii.gz"),
}

TASK_NAME_MAPPING = {
    TaskName.gli.value: "Adult Glioma Segmentation",
    TaskName.menrt.value: "Meningioma Segmentation Pre-Radiotherapy",
    TaskName.peds.value: "Pediatric Tumor Segmentation"

}

   LABEL_MAPPING_FACTORY = {
    TaskName.gli.value: {
        1: RegionName.NETC.value,
        2: RegionName.SNFH.value,
        3: RegionName.ET.value,
        4: RegionName.RC.value
    },
    TaskName.menrt.value: {
         1: RegionName.GTV.value
     },
    TaskName.peds.value: {
            1: RegionName.ET.value,
            2: RegionName.NET.value,
            3: RegionName.CC.value,
            4: RegionName.ED.value
     }
   }

SUFFIX = {
    "T2 FLAIR": "t2f",
    "native T1": "t1n",
    "post-contrast T1-weighted": "t1c",
    "T2 weighted": "t2w",
}

ALL_MODALITIES = list(SUFFIX)
IMAGE_ORDER_LIST = [
    SUFFIX["post-contrast T1-weighted"],
    SUFFIX["T2 FLAIR"],
    SUFFIX["native T1"],
    SUFFIX["T2 weighted"],
]

FULL_MODALITY_TASKS = (
    TaskName.gli.value,
    TaskName.peds.value

TASK_MODALITIES = {task: ALL_MODALITIES for task in FULL_MODALITY_TASKS}
TASK_MODALITIES[TaskName.menrt.value] = ["post-contrast T1-weighted"]



ALL_TASKS = {"t1c": f"{DUMMY_DIR}-t1c.nii.gz", "t2f": f"{DUMMY_DIR}-t2f.nii.gz", "t1n": f"{DUMMY_DIR}-t1n.nii.gz", "t2w": f"{DUMMY_DIR}-t2w.nii.gz"}

DUMMY_FILE_NAMES = {
    TaskName.gli.value:   ALL_TASKS,
    TaskName.menrt.value: {"t1c": f"{DUMMY_DIR}-t1c.nii.gz"},
    TaskName.peds.value:  ALL_TASKS,
}
   
AXIS_MAP = {"axial": 0, "coronal": 1, "sagittal": 2}
EXAMPLE_CASES = [
    (TaskName.gli.value, "BraTS-GLI-00492-000"),
]
EXAMPLE_OUTPUTS = {folder: f"example_outs/{folder}.nii.gz" for _, folder in EXAMPLE_CASES}

# Examples Setup
EXAMPLE_DIR = "./examples"

TASK_SUFFIXES = {
    task: {SUFFIX[modality] for modality in modalities}
    for task, modalities in TASK_MODALITIES.items()
}

EXAMPLES_FULL_DIR = []

for task, folder in EXAMPLE_CASES:
    folder_path = os.path.join(EXAMPLE_DIR, folder)
    valid_suffixes = TASK_SUFFIXES[task]

    files = [
        os.path.join(folder_path, f"{folder}-{suffix}.nii.gz") if suffix in valid_suffixes else None
        for suffix in IMAGE_ORDER_LIST
    ]

    EXAMPLES_FULL_DIR.append([task, *files])
