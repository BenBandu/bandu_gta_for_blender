import bpy


# noinspection PyPep8Naming
class RM_OT_MergeReplays(bpy.types.Operator):
	bl_idname = "replay_manager.merge_replay"
	bl_label = "Merge Replays"

	def get_mergee_items(self, context):
		manager = context.scene.replay_manager
		replays = [("-1", "Select Replay...", "")]
		for i, replay in enumerate(manager.replays):
			if i == manager.index or replay.version != manager.active_replay.version:
				continue

			replays.append((str(i), replay.name, "", "", i))

		return tuple(replays)

	def set_merger_vehicles(self, context):
		manager = context.scene.replay_manager

		vehicles = []
		for vehicle in manager.active_replay.vehicles:
			if vehicle.target:
				name = str(vehicle.index)
				vehicles.append((name, name, vehicle.model, "", 1 << len(vehicles)))

		RM_OT_MergeReplays._merger_vehicles_items = tuple(vehicles)

	def set_mergee_vehicles(self, context):
		if self.mergee == "-1":
			return ()

		manager = context.scene.replay_manager

		vehicles = []
		for vehicle in manager.replays[int(self.mergee)].vehicles:
			if vehicle.target:
				name = str(vehicle.index)
				vehicles.append((name, name, vehicle.model, "", 1 << len(vehicles)))

		RM_OT_MergeReplays._mergee_vehicles_items = tuple(vehicles)

	def get_merger_vehicles_items(self, context):
		return RM_OT_MergeReplays._merger_vehicles_items

	def get_mergee_vehicles_items(self, context):
		return RM_OT_MergeReplays._mergee_vehicles_items

	mergee: bpy.props.EnumProperty(
		items=get_mergee_items,
		name="Replays",
		description="Replay to merge with",
		update=set_mergee_vehicles,
	)

	_merger_vehicles_items = ()
	merger_vehicles: bpy.props.EnumProperty(
		items=get_merger_vehicles_items,
		name="Vehicles",
		description="Vehicles from Merger",
		options={"ENUM_FLAG"}
	)

	_mergee_vehicles_items = ()
	mergee_vehicles: bpy.props.EnumProperty(
		items=get_mergee_vehicles_items,
		name="Vehicles",
		description="Vehicles from Mergee",
		options={"ENUM_FLAG"}
	)

	def invoke(self, context, event):
		self.set_merger_vehicles(context)
		self.set_mergee_vehicles(context)

		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def execute(self, context):
		scene = context.scene
		replay = scene.replay_manager.active_replay

		if self.mergee == "-1":
			self.reset()
			return

		self.reset()
		return {"FINISHED"}

	def cancel(self, context):
		self.reset()

	def reset(self):
		self.mergee = "-1"
		self.__class__._merger_vehicles_items = ()
		self.__class__._mergee_vehicles_items = ()

	def draw(self, context):
		manager = context.scene.replay_manager

		row = self.layout.row()
		split = row.split(factor=0.25)

		row = split.column()
		row.label(text="Merger: ")
		row = split.column()
		row.label(text=manager.active_replay.name)

		row = self.layout.row()
		row.alert = self.mergee == "-1"
		row.prop(self, "mergee", text="Mergee", )

		self.layout.separator()

		row = self.layout.row()
		row.label(text="Merger Vehicles:")

		grid = self.layout.grid_flow(columns=5, even_columns=True, align=True)
		for flag in self._merger_vehicles_items:
			grid.prop_enum(self, "merger_vehicles", flag[0])

		if self.mergee != "-1":
			row = self.layout.row()
			row.label(text="Mergee Vehicles:")

			grid = self.layout.grid_flow(columns=5, even_columns=True, align=True)
			for flag in self._mergee_vehicles_items:
				grid.prop_enum(self, "mergee_vehicles", flag[0])

		#TODO: Ped flags
		#TODO: Handle potential re-assign model ids?
		#TODO: Settings...

		self.layout.separator()
