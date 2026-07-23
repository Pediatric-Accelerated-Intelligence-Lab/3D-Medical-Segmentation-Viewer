from enum import Enum
import os
# python 3.11 only supports StrEnum natively
# so we define our own for compatibility with 3.8+
class StrEnum(str, Enum):
    pass

class RegionName(StrEnum):
    NETC = "NON-ENHANCING TUMOR CORE (NETC)"
    ET = "ENHANCING TUMOR (ET)"
    CC = "CYSTIC COMPONENT (CC)"
    NET = "NON-ENHANCING TUMOR (NET)"
    ED = "EDEMA (ED)"
    GTV = "GROSS TUMOR VOLUME (GTV)"
    SNFH = "SURROUNDING NON-ENHANCING FLAIR HYPERINTENSITY (SNFH)"
    RC = "RESECTION CAVITY (RC)"
    RON = "RIGHT OPTIC NERVE (RON)"
    LON = "LEFT OPTIC NERVE (LON)"
    CHI = "CHIASM (CHI)"

class TaskName(StrEnum):
    gli = "Pre- and Post-Treatment Adult Glioma  (BraTS-GLI)"
    men = "Pre-Treatment  Meningioma (BraTS-MEN)"
    menrt = "Pre-Radiotherapy Meningioma (BraTS-MEN-RT)"
    met = " Pre- and Post-Treatment Metastasis (BraTS-MET)"
    ssa = "Sub-Saharan Africa Adult Glioma (BraTS-SSA)"
    peds = "Pre-Treatment Pediatric Glioma (BraTS-PED)"
    nf1 = "NF1 Anterior Visual Pathway (NF1-AVP)"


DUMMY_DIR = "BraTS-PED-00019-000"

#DOCKER_TASK_DICT = {task.value: f"aparida12/brats2025:{task.name}" for task in TaskName}
DOCKER_TASK_DICT = {
    TaskName.gli.value:    ("aparida12/brats2025:gli",            "/input/", "ro"),
    TaskName.men.value:    ("aparida12/brats2025:men",            "/input/", "ro"),
    TaskName.menrt.value: ("aparida12/brats2025:menrt",          "/input/", "ro"),
    TaskName.met.value:    ("aparida12/brats2025:met",            "/input/", "ro"),
    TaskName.ssa.value:    ("aparida12/brats2025:ssa",            "/input/", "ro"),
    TaskName.peds.value:    ("aparida12/brats2025:peds",           "/input/", "ro"),
    TaskName.nf1.value:      ("aparida12/cavs-segmenter:v20250314", "/data/",  "rw"),
}

DOCKER_OUTPUT = {
    TaskName.gli.value:   ("output_dir", f"{DUMMY_DIR}.nii.gz"),
    TaskName.men.value:   ("output_dir", f"{DUMMY_DIR}.nii.gz"),
    TaskName.menrt.value: ("output_dir", f"{DUMMY_DIR}.nii.gz"),
    TaskName.met.value:   ("output_dir", f"{DUMMY_DIR}.nii.gz"),
    TaskName.ssa.value:   ("output_dir", f"{DUMMY_DIR}.nii.gz"),
    TaskName.peds.value:  ("output_dir", f"{DUMMY_DIR}.nii.gz"),
    TaskName.nf1.value:   ("input_dir",  f"{DUMMY_DIR}_t1_ras_n4_res_seg_avp3.nii.gz"),
}

TASK_NAME_MAPPING = {
    TaskName.peds.value: "Pediatric Tumor Segmentation",
    TaskName.gli.value: "Adult Glioma Segmentation",
    TaskName.ssa.value: "Sub-Saharan Africa Adult Glioma Segmentation",
    TaskName.menrt.value: "Meningioma Segmentation Pre-Radiotherapy",
    TaskName.met.value: "Adult Metastasis Segmentation",
    TaskName.men.value: "Adult Pre-treatment Meningioma Segmentation",
    TaskName.nf1.value: "NF1 AVP Segmentation"
}
LABEL_MAPPING_FACTORY = {
    TaskName.peds.value: {
        1: RegionName.ET.value,
        2: RegionName.NET.value,
        3: RegionName.CC.value,
        4: RegionName.ED.value
    },
    TaskName.gli.value: {
        1: RegionName.NETC.value,
        2: RegionName.SNFH.value,
        3: RegionName.ET.value,
        4: RegionName.RC.value
    },
    TaskName.ssa.value: {
        1: RegionName.NETC.value,
        2: RegionName.ED.value,
        3: RegionName.ET.value
    },
     TaskName.menrt.value: {
         1: RegionName.GTV.value
     },
    TaskName.met.value: {
        1: RegionName.NETC.value,
        2: RegionName.SNFH.value,
        3: RegionName.ET.value,
        4: RegionName.RC.value
    },
    TaskName.men.value: {
        1: RegionName.NETC.value,
        2: RegionName.SNFH.value,
        3: RegionName.ET.value,
    },
    TaskName.nf1.value: {
        3: RegionName.RON.value,
        4: RegionName.LON.value,
        5: RegionName.CHI.value
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
    TaskName.ssa.value,
    TaskName.peds.value,
    TaskName.met.value,
    TaskName.men.value,
)

TASK_MODALITIES = {task: ALL_MODALITIES for task in FULL_MODALITY_TASKS}
TASK_MODALITIES[TaskName.menrt.value] = ["post-contrast T1-weighted"]
TASK_MODALITIES[TaskName.nf1.value] = ["native T1"]


ALL_TASKS = {"t1c": f"{DUMMY_DIR}-t1c.nii.gz", "t2f": f"{DUMMY_DIR}-t2f.nii.gz", "t1n": f"{DUMMY_DIR}-t1n.nii.gz", "t2w": f"{DUMMY_DIR}-t2w.nii.gz"}
DUMMY_FILE_NAMES = {
    TaskName.gli.value:   ALL_TASKS,
    TaskName.men.value:   ALL_TASKS,
    TaskName.met.value:   ALL_TASKS,
    TaskName.ssa.value:   ALL_TASKS,
    TaskName.peds.value:  ALL_TASKS,
    TaskName.menrt.value: {"t1c": f"{DUMMY_DIR}-t1c.nii.gz"},
    TaskName.nf1.value:   {"t1n": f"{DUMMY_DIR}_t1_ras_n4_res.nii.gz"},
}
   
AXIS_MAP = {"axial": 0, "coronal": 1, "sagittal": 2}
EXAMPLE_CASES = [
    (TaskName.gli.value, "BraTS-GLI-00492-000"),
    (TaskName.men.value, "BraTS-MEN-00134-000"),
    (TaskName.met.value, "BraTS-MET-00910-000"),
    (TaskName.peds.value, "BraTS-PED-00019-000"),
    (TaskName.ssa.value, "BraTS-SSA-00163-000"),
    (TaskName.menrt.value, "BraTS-MEN-RT-0308-1"),
    (TaskName.nf1.value, "AVP-KIDS-00001-001")
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
