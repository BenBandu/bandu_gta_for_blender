import bpy
from . import blocks


class Frame(bpy.types.PropertyGroup):

	general: bpy.props.PointerProperty(type=blocks.General, name="Camera")
	clock:   bpy.props.PointerProperty(type=blocks.Clock,   name="Clock")
	weather: bpy.props.PointerProperty(type=blocks.Weather, name="Weather")

	peds: bpy.props.CollectionProperty(type=blocks.Ped, name="Ped")
	ped_index: bpy.props.IntProperty(name="Ped Index", description="Current Ped", default=-1)

	vehicles: bpy.props.CollectionProperty(type=blocks.Vehicle, name="Vehicle")
	vehicle_index: bpy.props.IntProperty(name="Vehicle Index", description="Current Vehicle", default=-1)

	@property
	def active_ped(self):
		if len(self.peds) == 0:
			return None

		ped = self.peds[self.ped_index]
		if not ped.enabled:
			return None

		return ped

	@property
	def active_vehicle(self):
		if len(self.vehicles) == 0:
			return None

		vehicle = self.vehicles[self.vehicle_index]
		if not vehicle.enabled:
			return None

		return vehicle

