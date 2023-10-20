# exec(compile(open("/home/jtremblay/code/handal_annotating/bala.py").read(), "/home/jtremblay/code/handal_annotating/bala.py", 'exec'))

import bpy
import bgl
import blf
import mathutils
from bpy_extras import view3d_utils

class SpherePlacementOperator(bpy.types.Operator):
    bl_idname = "object.sphere_placement"
    bl_label = "Sphere Placement"
    bl_options = {'REGISTER', 'UNDO'}
    
    active = False
    location = None

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            if not SpherePlacementOperator.active:
                SpherePlacementOperator.active = True
                bpy.context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}
            else:
                SpherePlacementOperator.active = False
                return {'FINISHED'}
        return {'CANCELLED'}

    def find_intersection(self,context, event):
        region = context.region
        rv3d = context.region_data
        camera = bpy.context.scene.camera
        # Check if the mouse coordinates are within the viewport
        if event.mouse_region_x < 0 or event.mouse_region_x > region.width or event.mouse_region_y < 0 or event.mouse_region_y > region.height:
            return None
        x,y = event.mouse_region_x,event.mouse_region_y

        normalized_x = event.mouse_x / region.width
        normalized_y = event.mouse_y / region.height

        view_vector = rv3d.view_matrix.inverted() @ mathutils.Vector((normalized_x * 2 - 1, normalized_y * 2 - 1, -1))

        # ray_origin = context.region_data.view_location

        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, (x,y))
        ray_direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, (x,y))

        # print(view_vector,ray_origin)
        # bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=ray_origin)
        # bpy.context.object.data.name = 'ray_origin'

        # bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=view_vector)
        # bpy.context.object.data.name = 'view_vector'

        # ray_direction = (view_vector - ray_origin).normalized()

        # print(ray_direction)
    
        # num_spheres = 100  # You can adjust the number of spheres
        # interval = ray_direction.normalized() * 0.1  # Adjust the spacing between spheres

        # bpy.ops.object.empty_add(location=ray_origin)
        # parent_empty = bpy.context.object
        
        # for i in range(num_spheres):
        #     sphere_location = ray_origin + i * interval
        #     bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, location=sphere_location)
        #     sphere = bpy.context.object
        #     sphere.select_set(True)
        #     bpy.context.view_layer.objects.active = parent_empty
        #     bpy.ops.object.parent_set(type='OBJECT')
        #     sphere.select_set(False)
            # break

        # Intersect the ray with the objects in the scene
        # hit, location, norm, idx, obj, mw = bpy.context.scene.ray_cast(context.view_layer.depsgraph,ray_origin, ray_direction)
        hit, location, norm, idx, obj, mw = bpy.context.scene.ray_cast(context.view_layer.depsgraph,ray_origin, ray_direction)
        
        print(hit,location)
        # return None

        return location if hit else None

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if SpherePlacementOperator.active:
                # Get the 3D cursor location and add a sphere at that location
                location = self.find_intersection(context, event)
                if not location is None: 
                    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=location)
                SpherePlacementOperator.active = False
                return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            if SpherePlacementOperator.active:
                SpherePlacementOperator.active = False
                return {'CANCELLED'}
        return {'RUNNING_MODAL'}


class SpherePlacementPanel(bpy.types.Panel):
    bl_label = "Sphere Placement"
    bl_idname = "OBJECT_PT_SpherePlacementPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.sphere_placement")

def register():
    bpy.utils.register_class(SpherePlacementOperator)
    bpy.utils.register_class(SpherePlacementPanel)

def unregister():
    bpy.utils.unregister_class(SpherePlacementOperator)
    bpy.utils.register_class(SpherePlacementPanel)
    
if __name__ == "__main__":
    register()
