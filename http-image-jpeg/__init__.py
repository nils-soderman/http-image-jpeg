''' Paste licence here '''


bl_info = {
    "name": "http://image.jpeg",
    "description": "Download and load images directly into Blender by entering an image adress/URL",
    "author": "Nils Soderman",
    "version": (0, 0, 3),
    "blender": (2, 78, 0),
    "location": "UV/Image Editor & Spacebar menu",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "http://www.rymdnisse.net/contact/",
    "category": "Import-Export"
}



# Import Libraries
import bpy
import os
import urllib.request


# Addon updater by Patrick W. Crawford
# https://github.com/CGCookie/blender-addon-updater
from .addon_updater import Updater as updater
from . import addon_updater_ops
updater.user = "rymdnisse"
updater.repo = "http-image.jpeg"
updater.current_version = bl_info["version"]


# User Preferences
class DemoPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	# addon updater preferences

	auto_check_update = bpy.props.BoolProperty(
		name = "Auto-check for Update",
		description = "If enabled, auto-check for updates using an interval",
		default = False,
		)

	updater_intrval_months = bpy.props.IntProperty(
		name='Months',
		description = "Number of months between checking for updates",
		default=0,
		min=0
		)
	updater_intrval_days = bpy.props.IntProperty(
		name='Days',
		description = "Number of days between checking for updates",
		default=7,
		min=0,
		)
	updater_intrval_hours = bpy.props.IntProperty(
		name='Hours',
		description = "Number of hours between checking for updates",
		default=0,
		min=0,
		max=23
		)
	updater_intrval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description = "Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59
		)
	updater_showhide = bpy.props.BoolProperty(
		name='Show/Hide',
		description = "Show/Hide the updater settings.",
		default=False
		)

	def draw(self, context):

		layout = self.layout

		# Updater draw function
		addon_updater_ops.update_settings_ui(self,context)




# Operator
class Image_Download(bpy.types.Operator):
    """Download & open an image from an image adress/URL"""
    bl_idname = "image.download_image_url"
    bl_label = "Open Image from URL - (http://image.jpeg)"
    url = bpy.props.StringProperty(name="Image URL",description="URL to the image you want to open, e.g. http://google.com/icon.png", default="http://")
    def execute(self, context):

        # ---------------------------------------------------------------------
        # Preperations
        # ---------------------------------------------------------------------


        # Remove extra info from url after a "?"
        url = self.url
        if "?" in url:
            url = url.split("?")[0]

        # Construct nessisary paths
        dirpath = os.path.dirname(__file__)
        filename = os.path.split(url)[1]
        temp_path = os.path.join(dirpath, "temp")
        path = os.path.join(temp_path, filename)
        ext = filename.split(".")[1]

        # Create temp folder if it doesn't exist
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)


        # ---------------------------------------------------------------------
        #  Download Image
        # ---------------------------------------------------------------------

        try:
            urllib.request.urlretrieve(self.url, path)
        except:
             self.report({'ERROR'}, "Something went wrong, could not dowload image.")




        # ---------------------------------------------------------------------
        #       Convert SVG to PNG by rendering an OpenGL version of it.
        # ---------------------------------------------------------------------


        if ext == "svg":

            print("Converting SVG to PNG...")

            # Save previous settings
            area = bpy.context.area.type
            bpy.context.area.type = "VIEW_3D"
            only_render = context.space_data.show_only_render

            # Get all objects + selected once
            objlist = []
            selected_obj = []
            for obj in bpy.data.objects:
                objlist.append(obj.name)
                if obj.select:
                    selected_obj.append(obj.name)


            # Import SVG as mesh
            bpy.ops.import_curve.svg(filepath=path)

            # Get the new imported SVG objects
            svgobj = []
            for obj in bpy.data.objects:
                obj.select = False
                if obj.name not in objlist:
                    svgobj.append(obj.name)


            # Set new render setttings + camera rot/location
            context.space_data.show_only_render = True
            for ob in svgobj:
                bpy.data.objects[ob].select = True
            bpy.ops.view3d.localview()
            bpy.ops.view3d.viewnumpad(type="TOP", align_active=True)
            bpy.ops.view3d.viewnumpad(type="TOP", align_active=True)
            if area == "VIEW_3D":
                # This will cause Blender to crash incase it wasn't a 3D view by default.
                bpy.ops.view3d.zoom(delta=1)
                bpy.ops.view3d.zoom(delta=1)


            # remove SVG file & create a new path
            os.remove(path)
            path = path.replace(".svg", ".png")

            # Render openGL image
            bpy.ops.render.opengl()
            bpy.data.images['Render Result'].save_render(path)

            # Delete SVG
            for ob in svgobj:
                bpy.data.objects.remove(bpy.data.objects[ob], do_unlink=True)

            # Set previous settings
            for obj in selected_obj:
                bpy.data.objects[obj].select = True
            bpy.ops.view3d.localview()
            context.space_data.show_only_render = only_render
            bpy.context.area.type = area



        # ---------------------------------------------------------------------
        #   Open image in Blender
        # ---------------------------------------------------------------------

        # Load image
        image = bpy.data.images.load(path)
        image.name = filename
        image.pack()


        # Open image in the context to where the function is called.

        # Image Editor
        if bpy.context.area.type == "IMAGE_EDITOR":
            # Set as active image
            context.area.spaces.active.image = image
            print("Image loaded into Blender - " + filename)

        # 3D View
        elif bpy.context.area.type == "VIEW_3D":
            # Set as background image
            context.space_data.show_background_images = True
            context.space_data.background_images.new()
            i = len(context.space_data.background_images.items())
            context.space_data.background_images[i-1].image = image
            print("Image added as a background image - " + filename)

        # Node Editor
        elif bpy.context.area.type == "NODE_EDITOR":
            # Get current context
            if context.space_data.tree_type == "ShaderNodeTree":
                tree_type = context.space_data.tree_type.replace('Tree', 'TexImage')
            else:
                tree_type = context.space_data.tree_type.replace('Tree', 'Image')

            try:
                # Create a new node at mouse cursor
                bpy.ops.node.add_node(type=tree_type, use_transform=True)


                # Apply image to node
                i = len(context.space_data.node_tree.nodes)-1
                context.space_data.node_tree.nodes[i].image = image
                print("Image added as a node - " + filename)
            except:
                # Active node tree is not "activated"
                print("Image loaded into Blender - " + filename)
                pass
        else:
            print("Image loaded into Blender - " + filename)



        # Delete temp image
        os.remove(path)

        return {'FINISHED'}



    def invoke(self, context, event):
        # Paste clipboard into the url field when calling the function.
        self.url = bpy.context.window_manager.clipboard
        return context.window_manager.invoke_props_dialog(self)


# Draw operator in menu in the Image Editor
def menu_func(self, context):
    self.layout.operator("image.download_image_url", text="Open Image from URL")



# ------------------------------------------------------------------------
# register and unregister functions
# ------------------------------------------------------------------------

def register():
    # Addon updater
    addon_updater_ops.register(bl_info)

    # All other (In this case only the operator)
    bpy.utils.register_module(__name__)

    # Append the function to the menu in the image editor
    bpy.types.IMAGE_MT_image.append(menu_func)


def unregister():
    bpy.types.IMAGE_MT_image.remove(menu_func)
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
