import random

class OfficeLayout:
    def __init__(self, building_name):
        self.building_name = building_name
        self.floors = {}
        self.furniture = {}
        self.employees = {}
        self.xrefs = []

    def add_floor(self, floor_number, width, depth):
        self.floors[floor_number] = {
            'width': width,
            'depth': depth,
            'rooms': [],
            'furniture': []
        }
        print(f"Floor {floor_number} added: {width}m x {depth}m")

    def add_room(self, floor_number, room_name, x, y, w, h):
        if floor_number in self.floors:
            room = {
                'name': room_name,
                'x': x,
                'y': y,
                'width': w,
                'height': h
            }
            self.floors[floor_number]['rooms'].append(room)
            print(f"Room '{room_name}' added to Floor {floor_number}")
        else:
            print(f"Floor {floor_number} not found")

    def add_furniture(self, category, name, width, height, dynamic=False):
        if category not in self.furniture:
            self.furniture[category] = []
        
        item = {
            'name': name,
            'width': width,
            'height': height,
            'dynamic': dynamic
        }
        self.furniture[category].append(item)
        print(f"Furniture '{name}' added to {category}")

    def add_dynamic_block(self, category, name, base_width, base_height, stretch_params):
        if category not in self.furniture:
            self.furniture[category] = []
        
        block = {
            'name': name,
            'base_width': base_width,
            'base_height': base_height,
            'stretch_params': stretch_params,
            'dynamic': True
        }
        self.furniture[category].append(block)
        print(f"Dynamic Block '{name}' added to {category}")

    def place_furniture(self, floor_number, category, furniture_name, x, y, scale=1.0):
        if floor_number not in self.floors:
            print(f"Floor {floor_number} not found")
            return
        
        if category not in self.furniture:
            print(f"Category '{category}' not found")
            return
        
        found = None
        for item in self.furniture[category]:
            if item['name'] == furniture_name:
                found = item
                break
        
        if found:
            placement = {
                'name': furniture_name,
                'x': x,
                'y': y,
                'scale': scale,
                'dynamic': found.get('dynamic', False),
                'stretch_params': found.get('stretch_params', {})
            }
            self.floors[floor_number]['furniture'].append(placement)
            print(f"Placed '{furniture_name}' at ({x}, {y}) on Floor {floor_number}")
        else:
            print(f"Furniture '{furniture_name}' not found")

    def link_xref(self, external_file, layer, insert_point, scale=1):
        xref = {
            'file': external_file,
            'layer': layer,
            'insert_point': insert_point,
            'scale': scale
        }
        self.xrefs.append(xref)
        print(f"XREF linked: {external_file} at {insert_point}")

    def generate_bom(self):
        print("\n" + "=" * 60)
        print("   BILL OF MATERIALS (BOM)")
        print("=" * 60)
        
        bom = {}
        for floor_num, floor in self.floors.items():
            for item in floor['furniture']:
                name = item['name']
                if name not in bom:
                    bom[name] = 0
                bom[name] += 1
        
        print("\nItem Name           Quantity")
        print("-" * 40)
        for item, qty in bom.items():
            print(f"{item:<20} {qty}")
        
        print("=" * 60)

    def display_layout(self):
        print("\n" + "=" * 60)
        print(f"   OFFICE LAYOUT: {self.building_name}")
        print("=" * 60)
        
        for floor_num, floor in self.floors.items():
            print(f"\nFloor {floor_num}: {floor['width']}m x {floor['depth']}m")
            
            print("  Rooms:")
            for room in floor['rooms']:
                print(f"    - {room['name']}: ({room['x']}, {room['y']}) {room['width']}x{room['height']}m")
            
            print("  Furniture:")
            for item in floor['furniture']:
                dynamic = " (Dynamic)" if item.get('dynamic') else ""
                print(f"    - {item['name']} at ({item['x']}, {item['y']}){dynamic}")

def main():
    print("\n" + "=" * 60)
    print("   COMMERCIAL OFFICE SPACE LAYOUT")
    print("=" * 60)

    office = OfficeLayout("DecodeLabs Tower")

    print("\n[1] Adding Floors:")
    print("-" * 40)
    office.add_floor(1, 40, 30)
    office.add_floor(2, 40, 30)

    print("\n[2] Adding Rooms:")
    print("-" * 40)
    office.add_room(1, "Reception", 0, 0, 10, 8)
    office.add_room(1, "Open Workspace", 0, 10, 25, 15)
    office.add_room(1, "Meeting Room", 27, 10, 10, 8)
    office.add_room(1, "Break Room", 0, 27, 8, 3)
    office.add_room(2, "Executive Office 1", 0, 0, 10, 8)
    office.add_room(2, "Executive Office 2", 12, 0, 10, 8)
    office.add_room(2, "Conference Room", 0, 15, 20, 10)

    print("\n[3] Adding Standard Furniture:")
    print("-" * 40)
    office.add_furniture("desk", "Standard Desk", 1.5, 0.8)
    office.add_furniture("chair", "Office Chair", 0.6, 0.6)
    office.add_furniture("table", "Meeting Table", 3.0, 1.5)

    print("\n[4] Creating Dynamic Blocks:")
    print("-" * 40)
    office.add_dynamic_block("desk", "Stretchable Desk", 1.5, 0.8, {'stretch_x': True, 'stretch_y': False})
    office.add_dynamic_block("table", "Expandable Table", 2.0, 1.2, {'stretch_x': True, 'stretch_y': True})

    print("\n[5] Placing Furniture:")
    print("-" * 40)
    office.place_furniture(1, "desk", "Stretchable Desk", 5, 12, scale=1.5)
    office.place_furniture(1, "chair", "Office Chair", 5, 14)
    office.place_furniture(1, "chair", "Office Chair", 6, 14)
    office.place_furniture(1, "table", "Meeting Table", 30, 12)
    office.place_furniture(2, "desk", "Standard Desk", 2, 2)
    office.place_furniture(2, "desk", "Standard Desk", 14, 2)
    office.place_furniture(2, "table", "Expandable Table", 5, 18, scale=1.5)

    print("\n[6] External References (XREFs):")
    print("-" * 40)
    office.link_xref("architectural_shell.dwg", "shell", (0, 0))
    office.link_xref("electrical_plan.dwg", "electrical", (0, 0))

    print("\n[7] Full Layout Display:")
    office.display_layout()

    print("\n[8] Bill of Materials (BOM):")
    office.generate_bom()

    print("\n" + "=" * 60)
    print("   OFFICE LAYOUT DESIGN COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()