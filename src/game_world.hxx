//  $Id: game_world.hxx,v 1.4 2003/09/12 16:31:21 grumbel Exp $
// 
//  Windstille - A Jump'n Shoot Game
//  Copyright (C) 2000 Ingo Ruhnke <grumbel@gmx.de>
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

#ifndef GAMEWORLD_HXX
#define GAMEWORLD_HXX

#include <list>

class TileMap;
class DiamondMap;
class WaterMap;
class GameObj;
class Player;

class GameWorld
{
private:
  std::list<GameObj*> objects;
  std::list<Player*> player_objects;
  TileMap* tilemap;
  TileMap* background_tilemap;
  float passed_time;
  DiamondMap* diamond_map;
  WaterMap*   water_map;
public:
  GameWorld (const std::string& filename);
  ~GameWorld();
  
  void add (GameObj* obj) { objects.push_back (obj); }
  void remove (GameObj* obj) { objects.remove (obj); }
  
  // FIXME: are add/remove for different game object types a good
  // idea?
  void add_player (Player* obj);
  void remove_player (Player* obj);

  void draw ();
  void update (float delta);

  float get_time () { return passed_time; } 

  int get_width () const;
  int get_height () const;

  std::list<Player*>* get_players () { return &player_objects; }

  TileMap* get_tilemap () const { return tilemap; }
};

#endif

/* EOF */
