import os
import sys
import subprocess

BLENDER_EXE = 'C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe'
PROJECT_PATH = 'D:\\Sonstiges\\Programmierung\\Blender\\Scripts\\Batch Render\\test.blend'
SCENE_NAME = 'Scene'
OUTPUT_FILE_PATH = 'D:\\Desktop\\blender test\\output\\####'
PYTHON_BATCH_RENDER_FILE = "D:\\Sonstiges\\Programmierung\\Blender\\Scripts\\Batch Render\\batch_renderer.py"

try:
# check to throw any errors that occur
    command = [
        BLENDER_EXE,
        PROJECT_PATH,
        '--background',
        '--python', PYTHON_BATCH_RENDER_FILE
    ]
    # command = [
    #     BLENDER_EXE,
    #     PROJECT_PATH,
    #     '--background',
    #     '--scene', SCENE_NAME,
    #     '--frame-start', "0",
    #     '--frame-end', "10",
    #     '--render-output', OUTPUT_FILE_PATH,
    #     '--engine', 'CYCLES',
    #     # '--cycles-device', 'CPU',
    #     '--render-format', 'PNG',
    #     '--use-extension', "true",

    #     '--render-anim'

    # ]
    # command = [BLENDER_EXE, "--scene", SCENE_PATH]
    subprocess.run(command, check=True)
except subprocess.CalledProcessError:
    print('ERROR!')
    sys.exit(0)