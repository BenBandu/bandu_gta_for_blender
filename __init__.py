import bpy
from . import replay


def register():
	replay.register()


def unregister():
	replay.unregister()


if __name__ == '__main__':
	register()
	# unregister()