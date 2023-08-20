import bpy


# noinspection PyPep8Naming
class RM_PT_Vehicle(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Replay Manager"
	bl_idname = "RM_PT_Vehicle"
	bl_parent_id = "RM_PT_Replay"
	bl_label = "Vehicles"
	bl_options = {"DEFAULT_CLOSED"}

	def draw(self, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		vehicle = replay.active_vehicle

		self.layout.template_list("RM_UL_VEHICLE_LIST", "vehicle_list", replay, "vehicles", replay, "vehicle_index", rows=2)

		if vehicle is None:
			return

		row = self.layout.row()
		row.scale_y = 0.5
		row.alignment = "CENTER"
		row.label(text="Vehicle: " + vehicle.model)

		self.layout.separator()

		row = self.layout.row()
		row.prop(vehicle, "target", text="Location", icon="EMPTY_AXIS")

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

		for vehicle in replay.vehicles:
			if vehicle.enabled:
				return True

		return False
