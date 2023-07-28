import bpy


# noinspection PyPep8Naming
class RM_PT_Vehicle(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Replay Manager"
	bl_idname = "RM_PT_Vehicle"
	bl_parent_id = "RM_PT_Replay"
	bl_label = "Vehicle Data"

	def draw(self, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		vehicle = replay.active_vehicle

		row = self.layout.row()
		row.scale_y = 0.5
		row.alignment = "CENTER"
		row.label(text="Vehicle: " + vehicle.model)

		self.layout.separator()

		row = self.layout.row()
		row.prop(replay.general, "target", text="Location", icon="EMPTY_AXIS")

		self.layout.separator()

		#TODO: Enum?
		row = self.layout.row()
		row.prop(vehicle, property="primary_color", text="Primary")
		row.prop(vehicle, property="secondary_color", text="Secondary")

	@classmethod
	def poll(cls, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		if replay is None:
			return False

		vehicle = replay.active_vehicle
		if vehicle is None:
			return False

		return True
