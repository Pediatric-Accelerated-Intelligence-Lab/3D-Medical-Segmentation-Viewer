
**Introduction**

The manual segmentation of MRI scans is a time-intensive task. This web app is designed to facilitate clinicians in identifying tumor growth and volume. For example, the standard brain MRI for a glioma patient requires multiple sequences: T1-Weighted, T2-Weighted, FLAIR, and T1 Contrast-Enhanced. Then, a clinician must scross through every axial, sagittal, and coronal slice to calculate the volume of the tumor. 

Deep learning-based segmentation workflows can reduce time it takes to calculate such tumor volumes. By generating an initial segmentation within minutes, clinicians can review these and make corrections if needed. 

At the Children's National Hospital, the PAI lab built models for multiple tasks, including adult glioma, pediatric tumors, meningioma, and more. The goal of this web application is for clinicians to upload their patient's MRI scans, select the corresponding tumor type, and receive interactive axial, sagittal, and coronal views of the segmentation along with volumetric measurements for each tumor subregion within minutes. 

This app is a segmentation app. You input multiple MRI scans and the app outputs the full 3D segmentation mask and tumor volumes. The frontend is built using Gradio, an open-source Python library that allows for building interactive websites with machine learning models. Each docker container contains an AI model that will perform the corresponding task. The backend is designed using Gradio and Docker, such that adding a new segmentation task only requires changes in constants.py. It also features parallel execution, allowing multiple models to run simultaneously. 



**How to Clone Repository**

To edit the codebase, you first clone the repository on your local device. 

First, download Visual Studio Code using a standard web browser. Then, navigate to the repository web page on your browser. Click on the green button that reads "Code" and copy the HTTPS link. Now, in VS Code click "Clone Git Repository".

<img width="412" height="294" alt="Screenshot 2026-07-02 at 11 14 25 AM" src="https://github.com/user-attachments/assets/f94ffde5-6cb8-4d5e-b735-0805a8b13316" />

Copy the HTTPS link into the top search bar and press enter. 

<img width="662" height="75" alt="Screenshot 2026-07-02 at 11 16 24 AM" src="https://github.com/user-attachments/assets/895266fb-a0f3-419d-b5ed-76c751ade834" />

Now, you can run the codebase on your local computer. To test the website, run "bash deploy.sh" in your VS Code terminal. This should prompt you to open a site in your browser. 

**How to Add a Docker Container**

Adding a docker container requires a few steps in the constants.py file. 

Register the task name inside "class TaskName". Follow the same pattern as the others: newtask = "New Task Display Name"

<img width="297" height="149" alt="Screenshot 2026-07-06 at 10 51 26 AM" src="https://github.com/user-attachments/assets/1229fa1e-6da4-497d-aeaa-a49c68cfba72" />

Inside DOCKER_TASK_DICT, add a line that points to a Docker image, which folder in the container holds the input scans, and whether the folder should be "ro" (read only) or "rw" (writable). 

example: TaskName.newtask.value: ("yourdockerimage", "/input/", "ro")

<img width="639" height="167" alt="Screenshot 2026-07-06 at 10 54 02 AM" src="https://github.com/user-attachments/assets/e7ad9ea7-a263-481e-a441-f848b77bfb10" />

In DOCKER_OUTPUT, add a line that will indicate which folder the container writes its results into ("output_dir" or "input_dir") and what the output file name looks like

example: TaskName.newtask.value: ("output_dir", f"{DUMMY_DIR}.nii.gz"),

<img width="650" height="167" alt="Screenshot 2026-07-06 at 10 56 25 AM" src="https://github.com/user-attachments/assets/db4e38f7-6bf9-433c-ba81-68b7343f956e" />

In TASK_NAME_MAPPING, add a line that gives a display name. This will be displayed in the dropdown menu in the app. 

example: TaskName.newtask.value: "New Task Display Name",

<img width="539" height="169" alt="Screenshot 2026-07-06 at 11 06 54 AM" src="https://github.com/user-attachments/assets/168cb115-1c73-4178-bafc-2ccddf8ce65d" />

In LABEL_MAPPING_FACTORY, define what the colored regions are. Each number represents a label ID that the container outputs and it is mapped to a region name from RegionName. If the region your container needs isn't listed, add it to RegionName first. 

<img width="266" height="690" alt="Screenshot 2026-07-06 at 11 08 02 AM" src="https://github.com/user-attachments/assets/0fca1276-7d15-468c-803e-cfdcedfc1618" />

Indicate which scan types your container needs. If it needs all four scan types (FLAIR, T1, T2, T1c) add it to FULL_MODALITY_TASKS. If it doesn't need all four, indicate which tasks it needs like this: 

TASK_MODALITIES[TaskName.newtask.value] = ["native T1", "post-contrast T1-weighted"]

In DUMMY_FILE_NAMES, indicate what the input filenames look like. 

<img width="527" height="164" alt="Screenshot 2026-07-06 at 11 14 22 AM" src="https://github.com/user-attachments/assets/f2a11f64-86ff-48db-8cd6-fed678b13f13" />
