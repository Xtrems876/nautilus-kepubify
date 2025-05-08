import subprocess
import os


def run_kepubify(paths: list[str]):
    # Run kepubify for each file in the list
    for path in paths:
        output_dir = os.path.dirname(path)  # Get the directory of the input file
        subprocess.Popen(["kepubify", "--output", output_dir, path])


import gi

gi.require_version("Nautilus", "4.0")
from gi.repository import GObject, Nautilus


class KepubifyMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files: list[Nautilus.FileInfo]):
        # Only create a menu item if valid .epub files are explicitly selected
        selected_paths = [
            file.get_location().get_path()
            for file in files
            if file.get_uri_scheme() == "file"  # Check if it's a regular file
            and file.get_location()
            .get_path()
            .endswith(".epub")  # Check for .epub extension
            and not file.get_location()
            .get_path()
            .endswith(".kepub.epub")  # Exclude .kepub.epub
        ]
        if selected_paths:
            return [self.menu_item_for(selected_paths)]
        return []

    def menu_item_for(self, paths: list[str]) -> Nautilus.MenuItem:
        convert_to_kepub_item = Nautilus.MenuItem(
            name="KepubifyMenuProvider::ConvertToKepub",
            label="Convert to Kepub",
        )
        convert_to_kepub_item.connect("activate", self.menu_item_activated, paths)
        return convert_to_kepub_item

    def menu_item_activated(self, menu, user_data):
        run_kepubify(user_data)
