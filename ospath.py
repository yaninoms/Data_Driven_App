import os

map_file = "map.html"
full_path = os.path.abspath(map_file)
print(f"Map file saved at: {full_path}")  # Debugging
if os.path.exists(full_path):
    self.map_frame.load_url(f"file://{full_path}")
else:
    print("Error: Map file not found!")
