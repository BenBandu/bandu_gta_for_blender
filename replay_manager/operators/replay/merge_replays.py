import bpy


# noinspection PyPep8Naming
class RM_OT_MergeReplays(bpy.types.Operator):
	bl_idname = "replay_manager.merge_replay"
	bl_label = "Merge Replays"

	def update_merger_data(self, context):
		manager = context.scene.replay_manager

		vehicles = []
		for vehicle in manager.active_replay.vehicles:
			if vehicle.target:
				name = str(vehicle.index)
				vehicles.append((name, name, vehicle.model, "", 1 << len(vehicles)))

		RM_OT_MergeReplays._merger_vehicle_items = tuple(vehicles)

		peds = []
		for ped in manager.active_replay.peds:
			if ped.target:
				name = str(ped.index)
				peds.append((name, name, ped.model, "", 1 << len(peds)))

		RM_OT_MergeReplays._merger_ped_items = tuple(peds)

	def get_mergee_options(self, context):
		manager = context.scene.replay_manager
		replays = [("-1", "Select Replay...", "")]
		for i, replay in enumerate(manager.replays):
			if i == manager.index or replay.version != manager.active_replay.version:
				continue

			replays.append((str(i), replay.name, "", "", i))

		return tuple(replays)

	def update_mergee_data(self, context):
		if self.mergee == "-1":
			return ()

		manager = context.scene.replay_manager

		vehicles = []
		for vehicle in manager.replays[int(self.mergee)].vehicles:
			if vehicle.target:
				name = str(vehicle.index)
				vehicles.append((name, name, vehicle.model, "", 1 << len(vehicles)))

		RM_OT_MergeReplays._mergee_vehicle_items = tuple(vehicles)

		peds = []
		for ped in manager.replays[int(self.mergee)].peds:
			if ped.target:
				name = str(ped.index)
				peds.append((name, name, ped.model, "", 1 << len(peds)))

		RM_OT_MergeReplays._mergee_ped_items = tuple(peds)

	get_merger_vehicle_items = lambda self, context: RM_OT_MergeReplays._merger_vehicle_items
	get_merger_ped_items     = lambda self, context: RM_OT_MergeReplays._merger_ped_items
	get_mergee_vehicle_items = lambda self, context: RM_OT_MergeReplays._mergee_vehicle_items
	get_mergee_ped_items     = lambda self, context: RM_OT_MergeReplays._mergee_ped_items

	_merger_vehicle_items = ()
	_merger_ped_items     = ()
	_mergee_vehicle_items = ()
	_mergee_ped_items     = ()

	mergee: bpy.props.EnumProperty(
		items=get_mergee_options,
		name="Replays",
		description="Replay to merge with",
		update=update_mergee_data,
	)

	merger_vehicles: bpy.props.EnumProperty(
		items=get_merger_vehicle_items,
		name="Vehicles",
		description="Vehicles from Merger",
		options={"ENUM_FLAG"}
	)

	merger_peds: bpy.props.EnumProperty(
		items=get_merger_ped_items,
		name="Peds",
		description="Peds from Merger",
		options={"ENUM_FLAG"}
	)

	mergee_vehicles: bpy.props.EnumProperty(
		items=get_mergee_vehicle_items,
		name="Vehicles",
		description="Vehicles from Mergee",
		options={"ENUM_FLAG"}
	)

	mergee_peds: bpy.props.EnumProperty(
		items=get_mergee_ped_items,
		name="Peds",
		description="Peds from Mergee",
		options={"ENUM_FLAG"}
	)

	def invoke(self, context, event):
		self.update_merger_data(context)
		self.update_mergee_data(context)

		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def execute(self, context):
		scene = context.scene
		replay = scene.replay_manager.active_replay

		if self.mergee == "-1":
			self.reset()
			return {"FINISHED"}

		self.reset()
		return {"FINISHED"}

	def cancel(self, context):
		self.reset()

	def reset(self):
		self.mergee = "-1"
		self.__class__._merger_vehicle_items = ()
		self.__class__._mergee_vehicle_items = ()
		self.__class__._merger_ped_items = ()
		self.__class__._mergee_ped_items = ()

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
		row.label(text="Merger:")

		row = self.layout.row()
		row.scale_y = 0.5
		row.label(text="Vehicles")
		row.label(text="Peds")

		row = self.layout.row()
		split = row.split(factor=0.5)
		grid = split.column().grid_flow(columns=5, even_columns=True, align=True)
		for flag in self._merger_vehicle_items:
			grid.prop_enum(self, "merger_vehicles", flag[0])

		grid = split.column().grid_flow(columns=5, even_columns=True, align=True)
		for flag in self._merger_ped_items:
			grid.prop_enum(self, "merger_peds", flag[0])

		if self.mergee != "-1":
			self.layout.separator()

			row = self.layout.row()
			row.label(text="Mergee:")

			row = self.layout.row()
			row.scale_y = 0.5
			row.label(text="Vehicles")
			row.label(text="Peds")

			row = self.layout.row()
			split = row.split(factor=0.5)
			grid = split.column().grid_flow(columns=5, even_columns=True, align=True)
			for flag in self._mergee_vehicle_items:
				grid.prop_enum(self, "mergee_vehicles", flag[0])

			grid = split.column().grid_flow(columns=5, even_columns=True, align=True, )
			for flag in self._mergee_ped_items:
				grid.prop_enum(self, "mergee_peds", flag[0])

		#TODO: Handle potential re-assign model ids?
		#TODO: Settings...

		self.layout.separator()
