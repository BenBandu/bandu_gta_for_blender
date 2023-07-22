import bpy
from . import lists
from . import properties
from . import operators
from . import panels

bl_info = {
	"name": "Replay Manager",
	"author": "Simon Rofstad",
	"version": (2, 0),
	"blender": (3, 0, 0),
	"location": "View3D > Sidebar > Replay Manager",
	"description": "Manage .rep files from the classic Grand Theft Auto games",
	"category": "bandu-gta"
}

classes = properties.classes + lists.classes + panels.classes + operators.classes
f_register, f_unregister = bpy.utils.register_classes_factory(classes)


def register():
	f_register()

	bpy.types.Scene.replay_manager = bpy.props.PointerProperty(type=properties.Manager)
	bpy.types.TOPBAR_MT_file_import.append(operators.menu_import)
	bpy.types.TOPBAR_MT_file_export.append(operators.menu_export)


def unregister():
	del bpy.types.Scene.replay_manager
	bpy.types.TOPBAR_MT_file_import.remove(operators.menu_import)
	bpy.types.TOPBAR_MT_file_export.remove(operators.menu_export)

	f_unregister()
