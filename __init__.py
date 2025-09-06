bl_info = {
	"name": "Clear System Console",
	"author": "BolWaffy",
	"version": (1, 0),
	"blender": (2, 82, 0),
	"location": "Toolbar > Windows",
	"description": "Adds a button to clear the system console",
	"warning": "",
	"doc_url": "",
	"tracker_url": "",
	"category": "Development",
}

# --- Imports --- #
import bpy
import os
import platform
import traceback

# --- Constant --- #
version_check = bpy.app.version < (4, 0, 0)


# --- Core Logic --- #
def sys_console_clear(self):
	try:
		system = platform.system()

		# Try the major 3 operating systems
		if system == "Windows":
			os.system("cls")
		elif system in ["Linux", "Darwin"]:
			os.system("clear")

		else: # If none of the major OS are detected, try the commands blindly
			try:
				os.system("clear")
			except Exception:
				try:
					os.system("cls")

				except Exception: # If both blind attempts fail, Fallback for unsupported OS
					self.report({'ERROR'}, "Unsupported OS: Unable to clear the console.")	#Unsupported OS
					return

		# Show a notification if enabled in preferences
		preferences = bpy.context.preferences.addons[__name__].preferences
		if preferences.show_cleared_msg:
			bpy.context.window_manager.popup_menu(
				lambda self, context: self.layout.label(text="Console Cleared", icon='BRUSH_DATA'),
				title="Console has been cleared",
				icon='INFO'
			)

	except Exception:
		# Report any unexpected errors to the user and console
		self.report({'ERROR'}, "An unexpected error occurred.")
		print(f"\n{traceback.format_exc()}")


# --- Blender UI and Operator Classes --- #
def draw_func(self, context): # Appends Button operator to the Window menu
	self.layout.separator()
	self.layout.operator("sys_console.clear", text="Clear Console", icon='BRUSH_DATA')

class CLEAR_SYS_CONSOLE_OT_operator(bpy.types.Operator): # Clear System Console Operator Call
	bl_label = "Clear System Console"
	bl_idname = "sys_console.clear"
	bl_description = "Clear the system console"

	def execute(self, context):
		sys_console_clear(self)
		return {'FINISHED'}

class SYSTEM_CONSOLE_CLEAR_Preferences(bpy.types.AddonPreferences): # == Main PREFERENCES PANEL ==
	bl_idname = __name__

	show_cleared_msg: bpy.props.BoolProperty(
		name="Show Cleared Popup Message",
		description="Toggle on or off if you want to see the popup message after the console has been cleared",
		default=True)

	def draw(self, context):
		layout = self.layout

		if version_check: # Old Blender version compatibility
			layout = layout.box()

		layout.label(text="Clear System Console Addon Preferences:")

		if version_check: # Old Blender version compatibility
			layout.separator(factor=0.15)
		else:
			layout.separator(type='LINE')
		layout.prop(self, "show_cleared_msg")


# --- Registration --- #
def register():
	bpy.utils.register_class(CLEAR_SYS_CONSOLE_OT_operator)
	bpy.utils.register_class(SYSTEM_CONSOLE_CLEAR_Preferences)
	bpy.types.TOPBAR_MT_window.append(draw_func)

def unregister():
	bpy.utils.unregister_class(CLEAR_SYS_CONSOLE_OT_operator)
	bpy.utils.unregister_class(SYSTEM_CONSOLE_CLEAR_Preferences)
	bpy.types.TOPBAR_MT_window.remove(draw_func)

if __name__ == "__main__":
	register()