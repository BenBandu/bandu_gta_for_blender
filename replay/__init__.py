import bpy
from . import properties

bl_info = {
	"name": "Bandu-gta",
	"author": "Simon Rofstad",
	"version": (1, 0),
	"blender": (3, 0, 0),
	"location": "View3D > Sidebar > Replay Manager",
	"description": "Manage .rep files from the classic Grand Theft Auto games",
	"category": "bandu-gta"
}

classes = properties.classes


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.replay_manager = bpy.props.PointerProperty(type=properties.Manager)


def unregister():
	del bpy.types.Scene.replay_manager

	for cls in classes:
		bpy.utils.unregister_class(cls)
