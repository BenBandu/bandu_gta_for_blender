import bpy
import os
from shutil import copytree, copyfile, rmtree


# noinspection PyPep8Naming
class RM_OT_RefreshAddon(bpy.types.Operator):
	bl_idname = "replay_manager.refresh_addon"
	bl_label = "Refresh Addon"
	bl_description = "Copy scripts from source location to blenders add-on location, restart blender and recover last session"

	def execute(self, context):
		# Copy source to blender scripts
		self.update_directory()

		# restart blender, code snippet from https://github.com/LuxCoreRender/BlendLuxCore/blob/d435660c798451c0de3f023d07b0721ddbeccdf5/operators/debug.py#L28
		blender_exe = bpy.app.binary_path
		import subprocess

		execute = """import bpy
bpy.ops.wm.recover_last_session()
		"""

		subprocess.Popen([blender_exe, "-con", "--python-expr", execute.rstrip()])
		bpy.ops.wm.quit_blender()
		return {"FINISHED"}

	def update_directory(self):
		to_path = 'F:\\Users\\AppData\\Roaming\\Blender Foundation\\Blender\\3.6\\scripts\\addons\\bandu_gta_for_blender\\'
		from_path = 'K:\\Dev\\bandu-gta-for-blender\\'

		if os.path.exists(to_path):
			rmtree(to_path, ignore_errors=True)
			os.mkdir(to_path)

		copytree(from_path + 'replay_manager', to_path + "replay_manager")
		copytree(from_path + 'bandu_gta', to_path + "bandu_gta")
		for filename in os.listdir(from_path):
			if filename.endswith('.py') and not filename.startswith('update'):
				copyfile(from_path + filename, to_path + filename)
