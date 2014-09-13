# Flexlay - A Generic 2D Game Editor
# Copyright (C) 2014 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Sector:
  self.parent    = None
  self.name      = None
  self.music     = None
  self.gravity   = 10.0
  
  self.width  = None
  self.height = None
  
  self.background  = None
  self.interactive = None
  self.foreground  = None
  
  self.objects	  = None
#  sketch    = None
  self.editormap = None

  self.cameramode = "normal"

  attr_reader   :objects, :background, :interactive, :foreground, :parent, :width, :height
  attr_accessor :name, :music, :gravity
  
  def __init__(self, parent):
    self.parent = parent
    self.cameramode = "normal"
  end

  def get_level(self):
    return self.parent
  end

  def resize(self, size, pos):
    self.width  = size.width
    self.height = size.height
    self.background.resize(size, pos)
    self.interactive.resize(size, pos)
    self.foreground.resize(size, pos)
  end

  def new_from_size(self, name, width, height):
    self.name  = name
    self.music = ""
    self.gravity = 10.0
    
    self.width  = width
    self.height = height
    
    self.foreground  = TilemapLayer($tileset, self.width, self.height)
    self.interactive = TilemapLayer($tileset, self.width, self.height)
    self.background  = TilemapLayer($tileset, self.width, self.height)       
    self.objects	 = ObjectLayer()
    # self.sketch  = SketchLayer()

    self.editormap = EditorMap(True)
#    self.editormap.set_background_color(Color(255, 255, 255))
    self.editormap.add_layer(self.background.to_layer())
    self.editormap.add_layer(self.interactive.to_layer())
    self.editormap.add_layer(self.objects.to_layer())
    self.editormap.add_layer(self.foreground.to_layer())
#    self.editormap.add_layer(self.sketch.to_layer())
    # FIXME: Data might not get freed since its 'recursively' refcounted
    self.editormap.set_metadata(self)
    return self
  end

  def load_v1(self, data):
    self.name = "main"
    self.music = get_value_from_tree(["music", "_"], data, "")
    self.gravity = get_value_from_tree(["gravity", "_"], data, 10.0)
    
    self.width  = get_value_from_tree(["width", "_"], data, 20)
    self.height = get_value_from_tree(["height", "_"], data, 15)
    
    self.foreground  = TilemapLayer($tileset, self.width, self.height)
    self.foreground.set_data(get_value_from_tree(["foreground-tm"], data, []))
    
    self.interactive = TilemapLayer($tileset, self.width, self.height)
    self.interactive.set_data(get_value_from_tree(["interactive-tm"], data, []))
    
    self.background  = TilemapLayer($tileset, self.width, self.height)
    self.background.set_data(get_value_from_tree(["background-tm"], data, []))

    self.cameramode = "normal"

    self.editormap = EditorMap(True)

    self.objects = ObjectLayer()

    for i in get_value_from_tree(["objects"], data, [])
      (name, odata) = i[0], i[1..-1]
      # fix some old object names
      if(name == :money)
        name = :jumpy
      end
      if(name == :laptop)
        name = :mriceblock
      end
      create_gameobject_from_data(self.editormap, self.objects, name, odata)
    end

    start_pos_x = get_value_from_tree(["start_pos_x", "_"], data, 0)
    start_pos_y = get_value_from_tree(["start_pos_y", "_"], data, 0)
    sexpr = [["name", "main"], ["x", start_pos_x], ["y", start_pos_y]]
    create_gameobject_from_data(self.editormap, self.objects, "spawnpoint", sexpr)

    background = get_value_from_tree(["background", "_"], data, "")
    if(background != "")
      sexpr = [["image", background], ["speed", 0.5]]
      create_gameobject_from_data(self.editormap, self.objects, :background, sexpr)
    else:
      sexpr = [["top_color",
        get_value_from_tree(["bkgd_red_top", "_"], data, 0),
        get_value_from_tree(["bkgd_green_top", "_"], data, 0),
        get_value_from_tree(["bkgd_blue_top", "_"], data, 0)],
                ["bottom_color",
        get_value_from_tree(["bkgd_red_bottom", "_"], data, 0),
        get_value_from_tree(["bkgd_green_bottom", "_"], data, 0),
        get_value_from_tree(["bkgd_blue_bottom", "_"], data, 0)],
              ["speed", 0.5]]
      create_gameobject_from_data(self.editormap, self.objects, :background, sexpr)
    end

    partsys = get_value_from_tree(["particle_system", "_"], data, "")
    if(partsys == "snow")
      sexpr = []
      create_gameobject_from_data(self.editormap, self.objects, :'particles-snow', sexpr)
    elif(partsys == "rain")
      sexpr = []
      create_gameobject_from_data(self.editormap, self.objects, :'particles-rain', sexpr)
    elif(partsys == "clouds")
      sexpr = []
      create_gameobject_from_data(self.editormap, self.objects, :'particles-clouds', sexpr)
    elif(partsys == "")
    else:
      print "Unknown particle system type '", partsys, "'\n"
    end
	    
    self.editormap.add_layer(self.background.to_layer())
    self.editormap.add_layer(self.interactive.to_layer())
    self.editormap.add_layer(self.objects.to_layer())
    self.editormap.add_layer(self.foreground.to_layer())
    # FIXME: Data might not get freed since its 'recursively' refcounted
    self.editormap.set_metadata(self)
  end
  
  def load_v2(self, data):
    self.name = "<No Name>"
    self.music = ""
    self.init_script = ""
    self.gravity = 10.0
    self.cameramode = "normal"
    
    self.width  = 0
    self.height = 0

    self.background  = None
    self.interactive = None
    self.foreground  = None

    self.editormap = EditorMap(True)
    
    self.objects = ObjectLayer()
#    self.sketch = SketchLayer()

    for i in data
      (name,data) = i[0], i[1..-1]
      if name == :name:
        self.name = data[0]
      elif name == :gravity
        self.gravity = data[0]
      elif name == :music
	self.music = data[0]
      elif name == :"init-script"
        self.init_script = data[0]
      elif name == :tilemap
	layer   = get_value_from_tree(["layer", "_"], data, "interactive")
        width   = get_value_from_tree(["width", "_"],  data, 20)
        height  = get_value_from_tree(["height", "_"], data, 15)
        solid   = get_value_from_tree(["solid", "_"],  data, False)

        tilemap = TilemapLayer($tileset, width, height)
        tilemap.set_data(get_value_from_tree(["tiles"], data, []))
        
        if solid:
          self.interactive = tilemap
          self.width       = width
          self.height      = height
        elif layer == "background"
          self.background = tilemap
        elif layer == "foreground"
	  self.foreground = tilemap
        else:
          print "Flexlay doesn't handle tilemap layer '", layer, "'.\n"
        end
      elif name == :camera
	self.cameramode = "normal"
	# TODO...
      else:
	create_gameobject_from_data(self.editormap, self.objects, name, data)
      end
    end
    
    print "Tileset: ", $tileset, " ", width, " ", height, "\n"

    if(self.interactive == None || self.width == 0 || self.height == 0)
      throw "No interactive tilemap in sector '", self.name , "'.\n"
    end

    if (self.background == None):
      self.background = TilemapLayer($tileset, self.width, self.height)
    end

    if (self.foreground == None):
      self.foreground = TilemapLayer($tileset, self.width, self.height)
    end

    if self.background:
        self.editormap.add_layer(self.background.to_layer()) 
    if self.interactive:
        self.editormap.add_layer(self.interactive.to_layer()) 
    if self.foreground:
        self.editormap.add_layer(self.foreground.to_layer())
    self.editormap.add_layer(self.objects.to_layer())
#    self.editormap.add_layer(self.sketch.to_layer())
    self.editormap.set_metadata(self)
  end

  def activate(self, workspace):
    workspace.set_map(self.editormap)
    TilemapLayer.set_current(self.interactive)
    ObjectLayer.set_current(self.objects)
    connect(self.editormap.sig_change(), proc{$gui.on_map_change()})
  end

  def save_tilemap(self, f, tilemap, name, solid = None):
    f.write("    (tilemap\n")
    f.write("      (layer  \"%s\")\n" % name)
    f.write("      (solid %s)\n" % if solid == :solid then "#t" else "#f" end)
    f.write("      (speed  %f)\n" % 1.0)
    f.write("      (width  %d)\n" % tilemap.get_width())
    f.write("      (height %d)\n" % tilemap.get_height())
    f.write("      (tiles\n")
    f.write("        ")
    x = 0
    for i in tilemap.get_data()
      f.write("%d " % i)
      x += 1
      if x == width:
        f.write("\n        ")
        x = 0
      end
    end
    f.write("))\n")    
  end

  def save(self, f):
    f.write("    (name  \"#{self.name}\")\n"  % self.name)
    if(self.music != "")
      f.write("    (music  \"#{self.music}\")\n" % self.music)
    end
    if(self.init_script != "")
      f.write("    (init-script \"#{self.init_script}\")\n")
    end
    f.write("    (gravity %f)\n" % self.gravity)
    
    save_tilemap(f, self.background,  "background")
    save_tilemap(f, self.interactive, "interactive", :solid)
    save_tilemap(f, self.foreground,  "foreground")
#    save_strokelayer(f, self.sketch)

    f.write("    (camera\n")
    f.write("      (mode \"%s\")\n" % [self.cameramode])
#    f.write("      (path\n")
#    self.objects.get_objects().each {|obj|
#      pathnode = obj.get_data()
#      if (pathnode.is_a?(PathNode))
#        f.write("       (point (x %d) (y %d) (speed 1))\n" % obj.get_pos().x, obj.get_pos().y)
#      end
#    }
#    f.write("      )")
	f.write("    )\n\n")

    for obj in self.objects.get_objects()
      object = obj.get_data()
      object.save(f, obj)
    end
  end
end


# EOF #
