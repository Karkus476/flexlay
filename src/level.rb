class Level
  version = 2
  filename = nil
  
  name   = "no name"
  author = "no author"
  theme = "antarctica"
  time = 999
  music = "Mortimers_chipdisko.mod"
  
  objects = nil
  camera  = nil
  
  sectors = nil
  current_sector = nil

  attr_reader :version, :filename, :name, :author, :theme, :time, :music, :objects, :camera, :sectors, :current_sector
  attr_writer :version, :filename, :name, :author, :theme, :time, :music, :objects, :camera, :sectors, :current_sector
  
  def initialize(*params)
    if params.length() == 2 then
      # New Level
      (width, height) = params
      
      @name   = "No Name"
      @author = "No Author"
      
      @width  = width
      @height = height
      
      @current_sector = Sector.new(self)
      @current_sector.new_from_size(width, height)
      @sectors = []
      @sectors.push(@current_sector)
      
    elsif params.length() == 1 then
      # Load Level from file
      (@filename,) = params
      
      tree = sexpr_read_from_file(@filename)
      if tree == nil
        raise("Couldn't load level: ", filename)
      end
      
      data = tree[1..-1]
      
      @version = get_value_from_tree(["version", "_"], data, 0)
      
      print "VERSION: ", @version, "\n"
      
      if (@version == 1) then
        parse_v1(data)
      else
        parse_v2(data)
      end
    else
      raise "Wrong arguments for SuperTux::___init__"
    end
  end
  
  def parse_v2(data)
    @name    = get_value_from_tree(["name", "_"], data, "no name")
    @author  = get_value_from_tree(["author", "_"], data, "no author")
    @time    = get_value_from_tree(["time", "_"], data, 999)
    
    @current_sector = nil
    @sectors = []
    for sec in sexpr_filter("sector", data)
      sector = Sector.new(self)
      print("DATA: ", sec, "\n")
      sector.load_v2(sec)
      @sectors.push(sector)
      if sector.name == "main"
        @current_sector = sector
      end
    end
    
    if @current_sector == nil
      print "Error: No main sector defined: ", sectors, "\n"
      @current_sector = @sectors[0]
    end
  end

  def parse_v1(data)
    sector = Sector.new(self)
    sector.load_v1(data)
    
    @sectors = []
    @sectors.push(sector)
    @current_sector = sector
    
    @name    = get_value_from_tree(["name", "_"], data, "no name")
    @author  = get_value_from_tree(["author", "_"], data, "no author")
    @time    = get_value_from_tree(["time", "_"], data, 999)
  end
  
  def save(filename)
    save_v2(filename)
  end
  
  def save_v2(filename)
    f = File.new(filename, "w")
    f.write(";; Generated by Flexlay Editor\n" +
                                                "(supertux-level\n")
    f.write("  (version 2)\n")
    f.write("  (name   \"%s\")\n" % @name)
    f.write("  (author \"%s\")\n" % @author)
    f.write("  (time   \"%s\")\n" % @time)   
    
    for sector in @sectors
      f.write("  (sector\n")
      sector.save(f)
      f.write("   )\n")
    end

    f.write(" )\n\n;; EOF ;;\n")
  end
  
  def save_v1(filename)
    f = File.new(filename, "w")
    f.write(";; Generated by Flexlay Editor\n" +
                                                "(supertux-level\n")
    f.write("  (version 1)\n")
    f.write("  (name   \"%s\")\n" % @name)
    f.write("  (author \"%s\")\n" % @author)
    f.write("  (width  %s)\n"  % @width)
    f.write("  (height  %s)\n" % @height)
    
    f.write("  (music  \"%s\")\n" % @music)
    f.write("  (time   \"%s\")\n" % @time)
    
    f.write("  (gravity %d)\n" % @gravity)
    
    f.write("  (theme \"%s\")\n" % @theme)
    
    f.write("  (interactive-tm\n")
    for i in @interactive.get_data()
      f.write("%d " % i)
    end
    f.write("  )\n\n")

    f.write("  (background-tm\n")
    for i in @background.get_data()
      f.write("%d " % i)
    end
    f.write("  )\n\n")

    f.write("  (foreground-tm\n")
    for i in @foreground.get_data()
      f.write("%d " % i)
    end
    f.write("  )\n\n")

    f.write("  (camera\n")
    f.write("    (mode \"autoscroll\")\n")
    f.write("    (path\n")
    for obj in @objects.get_objects()
      pathnode = get_python_object(obj.get_metadata())
      if (pathnode.__class__ == PathNode)
        f.write("     (point (x %d) (y %d) (speed 1))\n" % obj.get_pos().x, obj.get_pos().y)
      end
    end
    f.write("  ))\n\n")
    
    f.write("  (objects\n")
    for obj in @objects.get_objects()
      badguy = get_python_object(obj.get_metadata())
      if (badguy.__class__ == BadGuy)
        pos    = obj.get_pos()
        if (badguy.type != "resetpoint")
          f.write("     (%s (x %d) (y %d))\n" % badguy.type, int(pos.x), int(pos.y))
        end
      end
    end
    f.write("  )\n\n")
    
    f.write("  (reset-points\n")
    for obj in @objects.get_objects()
      badguy = get_python_object(obj.get_metadata())
      if (badguy.__class__ == BadGuy)
        pos    = obj.get_pos()
        if (badguy.type == "resetpoint")
          f.write("     (point (x %d) (y %d))\n" % (pos.x.to_i), pos.y.to_i)
        end
      end
    end
    f.write("  )\n\n")
    
    f.write(" )\n\n;; EOF ;;\n")
  end

  def activate_sector(sector, workspace)
    for sec in @sectors
      if sec.name == sector
        sec.activate(workspace)
        break
      end
    end
  end

  def add_sector(sector)
    @sectors.push(sector)
  end

  def get_sectors()
    return @sectors.map {|sec| sec.name}
  end

  def activate(workspace)
    @current_sector.activate(workspace)
  end
end

# EOF #
