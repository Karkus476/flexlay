//  $Id: screen.cxx,v 1.2 2003/09/21 17:34:00 grumbel Exp $
//
//  Pingus - A free Lemmings clone
//  Copyright (C) 2002 Ingo Ruhnke <grumbel@gmx.de>
//
//  This program is free software; you can redistribute it and/or
//  modify it under the terms of the GNU General Public License
//  as published by the Free Software Foundation; either version 2
//  of the License, or (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program; if not, write to the Free Software
//  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

#include "delta_manager.hxx"
#include "screen.hxx"

Screen::Screen()
{
}

void 
Screen::display()
{
  do_pause = false;
  do_quit  = false;

  on_startup();

  DeltaManager delta_manager;
  
  while (!do_quit)
    {
      draw();
      
      float delta = delta_manager.getset ();
      if (!do_pause)
        {
          float step = 10/1000.0f;
          
          while (delta > step)
            {
              update(step);
              delta -= step;
            }
          update(delta);
        }

      CL_System::keep_alive ();
      CL_System::sleep (1);
    }

  on_shutdown();
}

/* EOF */
