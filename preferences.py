import bpy


class Preferences(bpy.types.AddonPreferences):
	bl_idname = "Bandu-Gta"

	replay_manager: bpy.props.BoolProperty(name="Replay Manager", default=True)
