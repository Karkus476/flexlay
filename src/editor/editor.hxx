//  $Id: editor.hxx,v 1.2 2003/09/10 10:58:29 grumbel Exp $
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

#ifndef HEADER_EDITOR_HXX
#define HEADER_EDITOR_HXX

#include <ClanLib/gui.h>

/** */
class Editor
{
private:
  CL_GUIManager*   manager;
  CL_Component*    component;
  CL_StyleManager* style;
  CL_ResourceManager* resources;
  CL_SlotContainer* slot_container;

  CL_PopupMenu* popupmenu;
  CL_MenuData*  menu_data;

  static Editor* current_;
public:
  static Editor* current() { return current_; }

  Editor();
  ~Editor();

  CL_Component* get_component() { return component; }
  void set_component(CL_Component* m) { component = m; }

  CL_SlotContainer* get_slot_container() { return slot_container; }

  void run();
  
  void popup_menu();
private:
  Editor (const Editor&);
  Editor& operator= (const Editor&);
};

#endif

/* EOF */