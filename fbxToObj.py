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
#    blender --background --python ./fbxToObj.py --fbx_file path_to_input_fbx_file --out_rest_fbx_file path_to_ouput_fbx_file --add_rest --out_obj_dir path_to_output_obj_folder --frame_idx 100
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import bpy
import sys, os
import argparse
from pathlib import Path

G_debug = False

def select_single_obj(target_obj):
    for obj in bpy.data.objects:
        obj.select = False
    target_obj.select = True
    for c in target_obj.children:
        c.select = True
    bpy.context.scene.objects.active = target_obj
    
        
if not G_debug:    
    ap = argparse.ArgumentParser()
    ap.add_argument("--background",  required=True, action='store_true', help="dummy argument to get around blender")
    ap.add_argument("--python",  required=True, type=str, help="dummy argument to get around blender")
    ap.add_argument("--fbx_file", required=True, type=str, help="input fbx file")
    ap.add_argument("--add_rest",  required=False, action='store_true', help="add this option to insert rest pose and export fbx")
    ap.add_argument("--out_rest_fbx_file", required=False, type=str, default='', help='if add_rest is on, this parameter must specify output fbx path')
    ap.add_argument("--out_obj_dir", required=False, type=str, default='', help='if this option is available, obj file corresponding to each frame will be exported')
    ap.add_argument("--frame_idx", required=False, type=int, default=0, help='frame index to be exported. if it is negative, all frames will be exported')
    args = ap.parse_args()       

    add_rest = args.add_rest
    out_rest_fbx_file = args.out_rest_fbx_file
    out_obj_dir = args.out_obj_dir
    fbx_file = args.fbx_file
    frame_idx = args.frame_idx

    if Path(fbx_file).suffix != '.fbx':
        print('input fbx_file does not end with .fbx pattern')
        sys.exit(0)
        
    if add_rest == True:
        is_valid =  out_rest_fbx_file != '' and Path(out_rest_fbx_file).suffix == '.fbx'
        if not is_valid:
            print('out_rest_fbx_file is not valid. it must be not empty and ends with .fbx pattern')
            sys.exit(0)
    print('\ninput parameters')
    print('\tfbx_file ', fbx_file)
    print('\tadd_rest ', add_rest)
    print('\tout_rest_fbx_file ', out_rest_fbx_file)
    print('\tout_obj_dir ', out_obj_dir)
else:
    fbx_file = '/home/khanhhh/data_1/projects/Oh/data/animation/Idle.fbx'
    out_obj_dir = '/home/khanhhh/data_1/projects/Oh/data/animation/Idle_output.obj'
    out_obj_dir = ''
    out_rest_fbx_file = '/home/khanhhh/data_1/projects/Oh/data/animation/RestPose.fbx'
    add_rest = True
    frame_idx = 0

#
# clear scene
# 
bpy.ops.scene.delete()

#
# import FBX
#
print("\nloading file: " + fbx_file)
bpy.ops.import_scene.fbx(filepath = fbx_file)


armature_obj = None
for obj in bpy.data.objects:
    if isinstance(obj.data, bpy.types.Armature):
        armature_obj = obj
        print('\nfound one Armature object in the fbx file. its name is: ', armature_obj.name)
        break

if armature_obj is None:
    print('\nobj of type Armature is not found in the scene')
    sys.exit(0)    
    
#
# add pose as first frame
#
if (add_rest):
    print('\ninserted the rest frame at frame index 0')
    bpy.ops.object.mode_set(mode='POSE')
    bpy.data.scenes['Scene'].frame_set(0)
    bpy.ops.pose.transforms_clear()
    for bone in armature_obj.pose.bones:
        bone.keyframe_insert("rotation_quaternion",frame=0)
        
    select_single_obj(armature_obj)
    bpy.ops.export_scene.fbx(filepath=out_rest_fbx_file, use_selection=True)

#
#
# save as animation frames
#
if out_obj_dir != '':
    
    os.makedirs(out_obj_dir, exist_ok = True)
    
    if frame_idx  < 0:
        out_name = Path(fbx_file).stem + '.obj'
        print("\nOutputting with prefix: " + out_name)
        out_path = os.path.join(*[out_obj_dir, out_name])
        bpy.ops.export_scene.obj(filepath=out_path, check_existing=False, axis_forward='-Z', axis_up='Y', use_selection=True, use_animation=True, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=False, use_uvs=False, use_materials=False, use_triangles=True, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=True, global_scale=1000.0, path_mode='AUTO')
    
    else:
        bpy.data.scenes['Scene'].frame_set(frame_idx)    
            
        #find the mesh object under Armature for exporting
        mesh_obj = None
        for c in armature_obj.children:
            if isinstance(c.data, bpy.types.Mesh):
                print('\nfound one mesh object for exporting under the Armature object. its name is: ', c.name)
                mesh_obj = c
        if mesh_obj is None:
            print('\nmesh obj is not found under Armature. exitting...')
            sys.exit(0)
        
        #just export that mesh obj
        select_single_obj(mesh_obj)
        
        out_name = Path(fbx_file).stem + '_' + str(frame_idx) + '.obj'    
        print("\nOutputting object: " + out_name)
        out_path = os.path.join(*[out_obj_dir, out_name])
        
        bpy.ops.export_scene.obj(filepath=out_path, check_existing=False, axis_forward='-Z', axis_up='Y', use_selection=True, use_animation=False, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=False, use_uvs=False, use_materials=False, use_triangles=True, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=True, global_scale=1000.0, path_mode='AUTO')
                


# done
print("fbxToObj.py completed, please don't mind the later messages by Blender\n\n\n")
