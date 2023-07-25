import bpy
from . import replay_manager
from .preferences import Preferences

bl_info = {
	"name": "Bandu-Gta",
	"author": "Simon Rofstad",
	"version": (2, 0),
	"blender": (3, 0, 0),
	"description": "Tools for handling multiple files from the classic Grand Theft Auto games",
	"category": "bandu-gta"
}


def register():
	bpy.utils.register_class(Preferences)
	replay_manager.register()


def unregister():
	bpy.utils.unregister_class(Preferences)
	replay_manager.unregister()


if __name__ == '__main__':
	register()
	# unregister()
