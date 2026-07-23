# 3D-Medical-Segmentation-Viewer

Introduction

The segmentation of MRI scans is a time-intensive task. This web app is designed to aid clinicians in identifying tumor growth and volume. For example, the standard brain MRI for a glioma patient requires multiple sequences: T1-Weighted, T2-Weighted, FLAIR, and T1 Contrast-Enhanced. Then, a clinician must scross through every axial, sagittal, and coronal slice to calculate the volume of the tumor.

Deep learning segmentation can reduce time it takes to calculate such tumors. By producing an initial segmentation within minutes, clinicians can review these and make corrections if needed.

At the Children's National Hospital, the PAI lab built models for multiple tasks, including adult glioma, pediatric tumors, meningioma, and more. The goal of this web application is for clinicians to upload their patient's MRI scans, select the corresponding tumor type, and receive interactive axial, sagittal, and coronal views of the segmentation along with volumetric measuremtns for each tumor subregion within minutes.

Website Architecture + How to Use

The frontend is built using Gradio, an open-source Python library that allows for building interactive websites with machine learning models. Each docker container contains an AI model that will perform the corresponding task. The backend is designed such that adding a new segmentation task only requires changes in constants.py. To add a new task:

How to Clone Repository

To edit the codebase, you first clone the repository on your local device.

First, download Visual Studio Code. Then, navigate to the repository web page on your browser. Click on the green button that reads "Code" and copy the HTTPS link. Now, in VS Code click "Clone Git Repository".

Screenshot 2026-07-02 at 11 14 25 AM
Copy the HTTPS link into the top search bar and press enter.

Screenshot 2026-07-02 at 11 16 24 AM
Now, you can run the codebase on your local computer. To test the website, run "bash deploy.sh" in your VS Code terminal. This should prompt you to open a site in your browser.

How to Add a Docker Container

Adding a docker container requires a few steps in the constants.py file.

Register the task name inside "class TaskName". Follow the same pattern as the others: newtask = "New Task Display Name"

Screenshot 2026-07-06 at 10 51 26 AM
Inside DOCKER_TASK_DICT, add a line that points to a Docker image, which folder in the container holds the input scans, and whether the folder should be "ro" (read only) or "rw" (writable).

example: TaskName.newtask.value: ("yourdockerimage", "/input/", "ro")

Screenshot 2026-07-06 at 10 54 02 AM
In DOCKER_OUTPUT, add a line that will indicate which folder the container writes its results into ("output_dir" or "input_dir") and what the output file name looks like

example: TaskName.newtask.value: ("output_dir", f"{DUMMY_DIR}.nii.gz"),

Screenshot 2026-07-06 at 10 56 25 AM
In TASK_NAME_MAPPING, add a line that gives a display name. This will be displayed in the dropdown menu in the app.

example: TaskName.newtask.value: "New Task Display Name",

Screenshot 2026-07-06 at 11 06 54 AM
In LABEL_MAPPING_FACTORY, define what the colored regions are. Each number represents a label ID that the container outputs and it is mapped to a region name from RegionName. If the region your container needs isn't listed, add it to RegionName first.

Screenshot 2026-07-06 at 11 08 02 AM
Indicate which scan types your container needs. If it needs all four scan types (FLAIR, T1, T2, T1c) add it to FULL_MODALITY_TASKS. If it doesn't need al lfour, indicate which tasks it needs like this:

TASK_MODALITIES[TaskName.newtask.value] = ["native T1", "post-contrast T1-weighted"]

In DUMMY_FILE_NAMES, indicate what the input filenames look like.

Screenshot 2026-07-06 at 11 14 22 AM
