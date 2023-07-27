import bpy


# noinspection PyPep8Naming
class RM_UL_VEHICLE_LIST(bpy.types.UIList):
	bl_idname = "RM_UL_VEHICLE_LIST"

	def filter_items(self, context, data, property):
		items = getattr(data, property)

		filtered = [self.bitflag_filter_item] * len(items)
		ordered = []
		unused = []
		for i, vehicle in enumerate(items):
			if not vehicle.enabled:
				filtered[i] &= ~self.bitflag_filter_item
				unused.append(i)
			else:
				ordered.append(i)

		return filtered, ordered + unused

	def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
		custom_icon = "EMPTY_AXIS"
		vehicle = item

		if self.layout_type in {"DEFAULT", "COMPACT"}:
			layout.label(text=vehicle.model, icon=custom_icon)
		elif self.layout_type in {"GRID"}:
			layout.alignment = "CENTER"
			layout.label(text="", icon=custom_icon)
