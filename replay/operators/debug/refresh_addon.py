import bpy
import os
from shutil import copytree, rmtree


# noinspection PyPep8Naming
class RM_OT_RefreshAddon(bpy.types.Operator):
	bl_idname = "rm_ops.refresh_addon"
	bl_label = "Refresh Addon"
	bl_description = "Copy scripts from source location to blenders add-on location, restart blender and recover last session"

	def execute(self, context):
		# Copy source to blender scripts
		from_path = 'K:\\Dev\\bandu-gta-for-blender\\replay'
		to_path = 'C:\\Users\\Simon\\AppData\\Roaming\\Blender Foundation\\Blender\\3.6\\scripts\\addons\\replay_manager'
		if os.path.exists(to_path):
			rmtree(to_path)

		copytree(from_path, to_path)

		# restart blender, code snippet from https://github.com/LuxCoreRender/BlendLuxCore/blob/d435660c798451c0de3f023d07b0721ddbeccdf5/operators/debug.py#L28
		blender_exe = bpy.app.binary_path
		import subprocess

		execute = """import bpy
bpy.ops.wm.recover_last_session()
		"""

		subprocess.Popen([blender_exe, "-con", "--python-expr", execute.rstrip()])
		bpy.ops.wm.quit_blender()
		return {"FINISHED"}
