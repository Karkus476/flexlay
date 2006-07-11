#!/usr/bin/ruby
##  $Id$
##
##  Flexlay - A Generic 2D Game Editor
##  Copyright (C) 2004 Ingo Ruhnke <grumbel@gmx.de>
##
##  This program is free software; you can redistribute it and/or
##  modify it under the terms of the GNU General Public License
##  as published by the Free Software Foundation; either version 2
##  of the License, or (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program; if not, write to the Free Software
##  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

$config_file = File.expand_path("~/.flexlay/supertux.rb")

def find_supertux_datadir()
  # try to automatically detect the supertux datadir
  possible_locations = [
    "~/cvs/supertux/supertux/data/",
    "~/cvs/supertux/data/",
    "/usr/share/games/supertux/",
    "/usr/local/share/games/supertux/",
    "/opt/supertux/data/",
    "~/projects/supertux/data/",
    "~/projects/supertux/svn/trunk/supertux/data/",
  ]
  # `which supertux`
end

# Config file loading hack
if File.exist?($config_file) then
  require $config_file
end

BACKGROUND_LAYER  = 1
INTERACTIVE_LAYER = 2
FOREGROUND_LAYER  = 3

require "flexlay_wrap"
include Flexlay_wrap

require "flexlay.rb"
require "gameobj.rb"
require "sexpr.rb"

flexlay = Flexlay.new()
width = 1024
height = 768
flexlay.init("SuperTux Editor", width, height)

# Tools
$tilemap_paint_tool  = TileMapPaintTool.new()
$tilemap_select_tool = TileMapSelectTool.new()
$zoom_tool           = ZoomTool.new()
$zoom2_tool          = Zoom2Tool.new()
$workspace_move_tool = WorkspaceMoveTool.new()
$objmap_select_tool  = ObjMapSelectTool.new()
# $sketch_stroke_tool  = SketchStrokeTool.new()

$mysprite = make_sprite("../data/images/icons16/stock_paste-16.png")

# $console = Console.new(CL_Rect.new(CL_Point.new(50, 100), CL_Size.new(400, 200)),
#                        $gui.get_component())
# $console.write("Hello World\n");
# $console.write("blabl\n");
# $console.write("blabl\naoeuau\naeouau");

require "gui.rb"

class Config
  attr_accessor :datadir, :recent_files

  def initialize()
    @recent_files = []
  end

  def save(filename)
    dir = File.expand_path("~/.flexlay/")
    if not File.exists?(dir) then
      Dir.mkdir(dir)
    end
    f = File.new(filename, "w")
    f.write("# Autogenerated Script, don't edit by hand!\n\n")
    f.write("$datadir      = " + $datadir.inspect() + "\n")
    f.write("$recent_files = " + $recent_files.inspect() + "\n")
    f.write("\n# EOF #\n")
  end
end

$config  = Config.new()
if !$datadir then
  $datadir = File.expand_path("~/projects/supertux/trunk/supertux/data/")+"/"
end

require "data.rb"
require "WorldMap.rb"
require "WorldMapObject.rb"
require "TileMap.rb"
require "LispWriter.rb"
require "tileset.rb"
require "level.rb"
require "sector.rb"
require "sprite.rb"
require "util.rb"

$tileset = Tileset.new(32)
$tileset.load($datadir + "images/tiles.strf")
$tileset.create_ungrouped_tiles_group()

$gui = SuperTuxGUI.new(width, height)

if !$recent_files then
  $recent_files = []
end

$recent_files.each do |filename|
  $gui.recent_files_menu.add_item($mysprite, filename, proc{ supertux_load_level(filename) })
end

if ARGV == []
  Level.new(100, 50).activate($gui.workspace)
else
  supertux_load_level(ARGV[0])
end

# Init the GUI, so that button state is in sync with internal state
$gui.gui_toggle_minimap()
$gui.gui_toggle_minimap()
$gui.gui_show_interactive()
$gui.gui_show_current()
$gui.set_tilemap_paint_tool()

if not File.exist?($datadir) then
  dialog = GenericDialog.new("Specify the SuperTux data directory and restart", $gui.gui.get_component())
  dialog.add_label("You need to specify the datadir where SuperTux is located")
  dialog.add_string("Datadir:", $datadir)
  
  dialog.set_block { |datadir|
    $datadir = datadir 
  }
end

$gui.run()

$config.save($config_file)

# FIXME: Can't deinit flexlay, since we would crash then
at_exit{flexlay.deinit()}
# puts "And now we crash"

# EOF #
