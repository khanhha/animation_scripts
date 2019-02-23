#!/usr/bin/python
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# The Oh Zone, Inc ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2019- The Oh Zone, inc. All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains the
# property of COMPANY. The intellectual and technical concepts
# contained herein are proprietary to COMPANY and may be covered
# by U.S. and Foreign Patents, patents in process, and are protected
# by trade secret or copyright law. Dissemination of this information
# or reproduction of this material is strictly forbidden unless prior
# written permission is obtained from COMPANY. Access to the source code
# contained herein is hereby forbidden to anyone except Alertcurrent COMPANY
# employees, managers or contractors who have executed Confidentiality
# and Non-disclosure agreements explicitly covering such access.
#
# The copyright notice above does not evidence any actual or intended
# publication or disclosure  of  this source code, which includes
# information that is confidential and/or proprietary, and is a trade
# secret of COMPANY. ANY REPRODUCTION, MODIFICATION, DISTRIBUTION,
# PUBLIC PERFORMANCE, OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS
# SOURCE CODE WITHOUT THE EXPRESS WRITTEN CONSENT OF COMPANY IS STRICTLY
# PROHIBITED, AND IN VIOLATION OF APPLICABLE LAWS AND INTERNATIONAL
# TREATIES. THE RECEIPT OR POSSESSION OF THIS SOURCE CODE AND/OR
# RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS TO REPRODUCE,
# DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE, USE, OR SELL
# ANYTHING THAT IT  MAY DESCRIBE, IN WHOLE OR IN PART.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# fbxToObj.py
#
# convert fbx to individual obj frames
#
# usage:
#    blender --background --python fbxToObj.py -- <fbx input> <output prefix>
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import bpy
import sys, os
import argparse
from pathlib import Path

G_debug = False

def Usage():
    print("Usage: blender --background --python fbxToObj.py -- <fbx input> {-add_rest} <output folder>")
    sys.exit(0)
    
if not G_debug:    
    ap = argparse.ArgumentParser()
    ap.add_argument("--background",  required=True, action='store_true', help="dummy argument to get around blender")
    ap.add_argument("--python",  required=True, type=str, help="dummy argument to get around blender")
    ap.add_argument("-fbx_file", required=True, type=str, help="input fbx file")
    ap.add_argument("--add_rest",  required=False, action='store_true', help="add this option to insert rest pose and export fbx")
    ap.add_argument("--out_rest_fbx_file", required=False, type=str, default='', help='if add_rest is on, this parameter must specify output fbx path')
    ap.add_argument("--out_obj_dir", required=False, type=str, default='', help='if this option is available, obj file corresponding to each frame will be exported')
    args = ap.parse_args()       

    add_rest = args.add_rest
    out_rest_fbx_file = args.out_rest_fbx_file
    out_obj_dir = args.out_obj_dir
    fbx_file = args.fbx_file

    if Path(fbx_file).suffix != '.fbx':
        print('input fbx_file does not end with .fbx pattern')
        sys.exit(0)
        
    if add_rest == True:
        is_valid =  out_rest_fbx_file != '' and Path(out_rest_fbx_file).suffix == '.fbx'
        if not is_valid:
            print('out_rest_fbx_file is not valid. it must be not empty and ends with .fbx pattern')
            sys.exit(0)
    print('input parameters')
    print('fbx_file ', fbx_file)
    print('add_rest ', add_rest)
    print('out_rest_fbx_file ', out_rest_fbx_file)
    print('out_obj_dir ', out_obj_dir)
else:
    fbx_file = '/home/khanhhh/data_1/projects/Oh/data/animation/Idle.fbx'
    out_obj_dir = '/home/khanhhh/data_1/projects/Oh/data/animation/Idle_output.obj'
    out_obj_dir = ''
    out_rest_fbx_file = '/home/khanhhh/data_1/projects/Oh/data/animation/RestPose.fbx'
    add_rest = True
    

#
# clear scene
# 
bpy.ops.scene.delete()

#
# import FBX
#
print("loading file: " + fbx_file)
bpy.ops.import_scene.fbx(filepath = fbx_file)


#
# add pose as first frame
#
if (add_rest):
    bpy.ops.object.mode_set(mode='POSE')
    bpy.data.scenes['Scene'].frame_current=0
    bpy.ops.pose.transforms_clear()
    obj = bpy.context.object
    for bone in obj.pose.bones:
        bone.keyframe_insert("rotation_quaternion",frame=0)
    bpy.ops.export_scene.fbx(filepath=out_rest_fbx_file)

#
#
# save as animation frames
#
if out_obj_dir != '':
    
    os.makedirs(out_obj_dir, exist_ok = True)
    
    out_name = Path(fbx_file).stem + '.obj'
    print("Outputting with prefix: " + out_name)
    out_path = os.path.join(*[out_obj_dir, out_name])
    
    bpy.ops.export_scene.obj(filepath=out_path, check_existing=False, axis_forward='-Z', axis_up='Y', use_selection=False, use_animation=True, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=False, use_uvs=False, use_materials=False, use_triangles=True, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=True, global_scale=1000.0, path_mode='AUTO')

# done
print("fbxToObj.py completed")
