import os.path
import sys
from enum import Enum
import bpy



DELIMITER_KEY = 'DELIMITER'
delimiter = None

EEVEE = 'eevee'
CYCLES = 'cycles'
WORKBENCH = 'workbench'

BATCH_FILE_PATH = 'batch.txt'

"""RenderSettings objects. All render jobs."""
jobs = []


def read_command(line):
    global delimiter
    print('Found command: ' + line)
    line = line.removeprefix('!')
    key, value = line.split('=')
    key = key.strip()
    value = value.strip()
    if key == DELIMITER_KEY:
        if not value:
            message = 'Invalid DELIMITER value ' + value + '!'
            print(message)
            raise Exception(message)
        delimiter = value
        print('Set DELIMITER to ' + delimiter)


def read_batch_file():
    batch_jobs = []
    with open(BATCH_FILE_PATH, 'r') as batch:
        for line in batch.readlines():
            line = line.strip()
            if line == '':
                continue
            if line.startswith('#'):    #ignore comments
                #print('Comment ^^^')
                continue
            elif line.startswith('!'):
                read_command(line)
                continue
            else:
                print(line)
                rset = create_render_settings(line)
                batch_jobs.append(rset)

    return batch_jobs




def main():
    global jobs
    # test_changing_settings()
    jobs = read_batch_file()
    start_jobs()
    # for job in jobs:
        # set_render_settings(job)
        # start_render()


def start_jobs():
    global jobs
    for job in jobs:
        set_render_settings(job)
        if job.open_gl_render:
            render_viewport_animation()
            
        else:
            start_render()


def jobs_contained_open_gl_render():
    for job in jobs:
        if job.open_gl_render:
            return True
        
    return False


def test_changing_settings():
    rset = RenderSettings()
    rset.camera = "Camera"
    rset.start_frame = 100
    rset.end_frame = 200
    rset.engine = RenderEngine.CYCLES
    rset.resolution_x = 100
    rset.resolution_y = 200
    rset.resolution_percentage = 50
    rset.fps = 30
    rset.samples = 111
    rset.file_ext = "mov"
    
    set_render_settings(rset)


def set_active_camera(camera_name):
    print('Setting active camera to ' + camera_name)
    scene = bpy.context.scene
    scene_cam = scene.objects.get(camera_name)
    if scene_cam:
        scene.camera = scene_cam
    else:
        print("Error! Could not find " + camera_name)
        raise Exception("Error! Could not find " + camera_name)



    
def set_render_settings(settings):
    """
    :param: Render settings
        A RenderSettings obj containing the render settings.
    """
    set_active_camera(settings.camera)
    scene = bpy.context.scene
    scene.frame_start = settings.start_frame
    scene.frame_end = settings.end_frame
    render = scene.render    
    render.engine = settings.engine.value
    scene.cycles.device = settings.compute_device
    render.resolution_x = settings.resolution_x
    render.resolution_y = settings.resolution_y
    render.resolution_percentage = settings.resolution_percentage
    render.fps = settings.fps
    set_samples(settings.samples, scene, settings.engine)
    scene.cycles.samples = settings.samples
    render.use_file_extension = settings.use_file_ext
    render.filepath = settings.file_path
    render.use_overwrite = settings.overwrite
    render.image_settings.file_format = settings.file_format
    render.image_settings.compression = settings.compression
    
    

def set_samples(samples, scene, engine):
    if engine == RenderEngine.EEVEE:
        pass
    elif engine == RenderEngine.CYCLES:
        scene.cycles.samples = samples
    elif engine == RenderEngine.WORKBENCH:
        pass    
        


def render_viewport_image():
    bpy.ops.render.opengl(animation=False)
    
def render_viewport_animation():
    # view_context=False causes blender to render using the scene settings instead of the currently 3D view
    bpy.ops.render.opengl(animation=True, view_context=False)

def render_image():
    bpy.ops.render.render(animation=False)

def start_render():
    bpy.ops.render.render(animation=True)




def create_render_settings(line):
    line_values = line.split(delimiter)
    print(line_values)
    rset = RenderSettings()
    i = 0

    rset.ip = line_values[i].strip()
    i = i+1
    rset.camera = line_values[i].strip()
    i = i+1
    rset.start_frame = int(line_values[i].strip())
    i = i+1
    rset.end_frame = int(line_values[i].strip())
    i = i+1
    rset.engine = RenderEngine(line_values[i].strip())
    i = i+1
    rset.compute_device = line_values[i].strip()
    i = i+1
    rset.open_gl_render = parse_int_boolean(line_values[i].strip())
    i = i+1
    rset.resolution_x = int(line_values[i].strip())
    i = i+1
    rset.resolution_y = int(line_values[i].strip())
    i = i+1
    rset.resolution_percentage = int(line_values[i].strip())
    i = i+1
    rset.fps = int(line_values[i].strip())
    i = i+1
    rset.samples = int(line_values[i].strip())
    i = i+1
    rset.use_file_ext = parse_int_boolean(line_values[i].strip())
    i = i+1
    rset.file_path = line_values[i].strip()
    i = i+1
    rset.file_format = line_values[i].strip()
    i = i+1
    rset.overwrite = parse_int_boolean(line_values[i].strip())
    i = i+1
    rset.compression = int(line_values[i].strip())
        
    print(rset)

    return rset


def parse_int_boolean(value):
    """
    Parses 0 to False and 1 to True
    """
    return bool(int(value.strip()))


class RenderEngine(Enum):
    EEVEE = 'BLENDER_EEVEE'
    CYCLES = 'CYCLES'
    WORKBENCH = 'BLENDER_WORKBENCH'


class RenderSettings():
    def __init__(self):
        self.camera = None
        self.start_frame = None
        self.end_frame = None
        self.engine = 'CYCLES'
        self.compute_device = 'CPU'
        self.resolution_x = 1920
        self.resolution_y = 1080
        self.resolution_percentage = 100
        self.fps = 25
        self.samples = 128
        self.use_file_ext = False
        self.file_path = 'blubb'
        self.overwrite = False
        self.file_format = 'PNG'
        self.compression = 15
        self.open_gl_render = False
        self.ip = None
        
    def __str__(self):
        return f"{self.ip} \t {self.camera} \t {self.start_frame} \t {self.end_frame} \t {self.engine} \t {self.compute_device} \t {self.open_gl_render} \t {self.resolution_x} \t {self.resolution_y} \t {self.resolution_percentage} \t {self.fps} \t {self.samples} \t {self.use_file_ext} \t {self.file_path} \t {self.overwrite} \t {self.file_format} \t {self.compression}"




if __name__ == '__main__':
    bpy.app.handlers.load_post.append(main())

    # close Blender if it had been opened for OpenGL viewport renders.
    if jobs_contained_open_gl_render:
        bpy.ops.wm.quit_blender()