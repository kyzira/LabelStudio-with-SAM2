# Setting Up Label Studio with SAM2

This guide will walk you through setting up Label Studio on Ubuntu using WSL and SAM2 with Label Studio ML Backend on Windows.
My User is called k3000, just replace it with your User.

## Install Label Studio

1. **Install WSL and Ubuntu.**

2. **Install Label Studio** using the following commands:

    ```bash
    python3 -m venv env
    source env/bin/activate
    sudo apt install python3.9-dev
    python3 -m pip install label-studio
    ```

3. **Edit the bash profile to set environment variables when starting Ubuntu:**

    ```bash
    sudo nano ~/.bash_profile
    ```

4. **Copy the following lines into the file, save with `CTRL + S`, and exit with `CTRL + X`:**
    For Local Storage:

    ```bash
    export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
    export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/home/k3000
    export PATH="$PATH:/home/k3000/.local/bin/"
    ```

    For minIO Storage:

    ```bash
    export LABEL_STUDIO_HOST=http://`<your ip adress>`:8080
    ```

5. **Close the Terminal and reopen Ubuntu.**

6. **Add your images to your Ubuntu home directory.** It should be a subfolder, e.g., `/home/k3000/testingdata1`.

7. **Run Label Studio with the following command:**

    ```bash
    label-studio start
    ```

8. **In Label Studio, add a new project:**
    - Go into the settings and then into **Cloud Storage**.
    - Add **Source Storage** and select **Local Files** as the Storage Type.
    - The absolute path should be, e.g., `/home/k3000/testingdata1`.
    - Remember to check "Treat every bucket object as a source file".
    - You can now add your storage. Click on **Sync Storage** to add your images to your project.

## Prepare Label Studio ML Backend with SAM2

1. **Follow this [tutorial](https://github.com/HumanSignal/label-studio-ml-backend?tab=readme-ov-file) to run from source.**

2. **When the model is running, you can add it to Label Studio:**
    - Go into the **Settings** again, but this time into **Model**.
    - Add a Model. For the Name, you can choose anything (e.g., SAM2).
    - The Backend URL should be `http://<your_ip_address>:9090`. (e.g. `http://192.168.200.92:9090`)
    - Don’t forget to toggle **Interactive Preannotations** to activate the model.

3. **Set environment values**
    - Go into the environment value settings.
    - Set two new variables:
        - `LABEL_STUDIO_URL` and the value is the ip adress (e.g. `http://192.168.200.92:8080`)
        - `LABEL_STUDIO_API_KEY` and the value is the api key (e.g. `4b42c2ae658b7507e3e81ecbfb7af58c82816369`)
            - You can get the key when you load into Label Studio, click on your profile picture on the top right, then into `account&settings` and the key should be displayed on the right hand side.


4. **Finally, you can add your Labeling interface. You can use this template:**

    ```xml
    <View>
        <Image name="image" value="$image" zoom="true"/>
        <Header value="Brush Labels"/>
        <BrushLabels name="tag" toName="image">
            <Label value="Connections" background="#FF0000"/>
            <Label value="Cracks" background="#0d14d3"/>
            <Label value="Roots" background="#FFA39E"/>
        </BrushLabels>
        <Header value="Keypoint Labels"/>
        <KeyPointLabels name="tag2" toName="image" smart="true">
            <Label value="Connections" smart="true" background="#000000" showInline="true"/>
            <Label value="Cracks" smart="true" background="#000000" showInline="true"/>
            <Label value="Roots" smart="true" background="#000000" showInline="true"/>
        </KeyPointLabels>
        <Header value="Rectangle Labels"/>
        <RectangleLabels name="tag3" toName="image" smart="true">
            <Label value="Connections" background="#000000" showInline="true"/>
            <Label value="Cracks" background="#000000" showInline="true"/>
            <Label value="Roots" background="#000000" showInline="true"/>
        </RectangleLabels>
    </View>
    ```




# **Additional Info**


**Storage Option: If you want to use it in Docker**
- Edit following line in the docker-compose.yml and add your ip adress, so the images are hostet correct:
    `LABEL_STUDIO_HOST=${LABEL_STUDIO_HOST:-}`





# **Cant export SAM segments to coco format yet**

Label Studio cant export segments created with SAM to the YOLO or COCO format yet. 


This folder `Conversion` contains the scripts needed for processing images and training models:

- **Conversion Scripts:**
  - **`convert_image_names.py`:** Renames source images to the required format.
  - **`convert_mask_to_coco.py`:** Converts Label Studio masks into COCO JSON format.
  - **`convert_coco_to_yolo.py`:** Converts COCO JSON to YOLO format.

  **Workflow:**
  > **Disclaimer:** Ensure you specify the correct folder paths in the scripts before running them.
  1. Copy source images into a separate folder.
  2. Export labels from Label Studio in two formats:
     - PNG for masks.
     - JSON-min for annotations.
  3. Run `convert_image_names.py` to rename images.
  4. Run `convert_mask_to_coco.py` to convert masks to COCO JSON.
  5. Run `convert_coco_to_yolo.py` to convert COCO JSON to YOLO format.
