// Flexlay - A Generic 2D Game Editor
// Copyright (C) 2002 Ingo Ruhnke <grumbel@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#ifndef HEADER_FLEXLAY_CONSOLE_HPP
#define HEADER_FLEXLAY_CONSOLE_HPP

#include <ClanLib/GUI/component.h>
#include <memory>

class CL_Font;
class ConsoleImpl;
class Rect;
class Size;

class Console : public CL_Component
{
protected:
  virtual ~Console();
public:
  Console(/*const CL_Font& font, */const Rect& rect, CL_Component* parent);

  /** Write something to the console */
  void write(const std::string& );
  void clearscr();
private:
  std::shared_ptr<ConsoleImpl> impl;
};

#endif

/* EOF */
