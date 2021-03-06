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


import csv
import logging
from collections import OrderedDict

from flexlay import ObjectBrush, Config
from .gameobj import *
from .worldmap_object import *
from .sprite import SuperTuxSprite


def format_sprite_name(name):
    """
    sprite_name -> Sprite Name
    """
    name = name.replace("_", " ")
    name = name.title()
    return name


class SuperTuxGameObjFactory:
    """
    identifier: section in the .stl file, used for load and save, most of the time, also for Drag&drop
    sprite: used in the object selection and/or in the ObjMapSpriteObject
    functor: creates the object

    ObjectBrush(sprite, metadata)

    See editor/supertux-editor/LevelObjects/Objects.cs
    """
    supertux_gui = None

    def __init__(self):
        GameObj.factory = self
        self.objects = OrderedDict()
        # List of (identifier, image, tag)
        self.badguys = []
        self.init_factories()

    def create_gameobj_at(self, identifier, pos):
        data = self.objects.get(identifier)
        if data is None:
            logging.warning("couldn't create: %r at %s" % (identifier, pos))
        else:
            _, constructor = data
            obj = constructor()
            obj.objmap_object.pos = pos
            return obj

    def create_gameobj(self, identifier, sexpr):
        data = self.objects.get(identifier)
        if data is None:
            logging.warning("couldn't create: %r" % identifier)
        else:
            _, constructor = data
            obj = constructor()
            obj.read(sexpr)
            obj.update()
            return obj

    def create_object_brushes(self):
        """Creates Object Brushes for each sprite"""
        # print("Creating object brushes...")
        brushes = []
        for identifier, (sprite, constructor) in self.objects.items():
            if sprite is not None:
                brush = ObjectBrush(SuperTuxSprite.from_file(os.path.join(Config.current.datadir, sprite)).get_sprite(),
                                    identifier)
                brushes.append(brush)
        return brushes

    def add_object(self, gameobj_class):
        self.objects[gameobj_class.identifier] = (gameobj_class.sprite, gameobj_class)

    def add_badguy(self, identifier, sprite, tag=None):
        self.objects[identifier] = (sprite, lambda: BadGuy(identifier, sprite))
        if tag:
            self.badguys.append((identifier, sprite, tag))
        else:
            self.badguys.append((identifier, sprite))

    def add_simple_object(self, identifier, sprite):
        self.objects[identifier] = (sprite, lambda: SimpleObject(identifier, sprite))

    def add_simple_tile(self, identifier, sprite):
        self.objects[identifier] = (sprite, lambda: SimpleTileObject(identifier, sprite))

    def add_particle_system(self, identifier, sprite, kind):
        self.objects[identifier] = (sprite, lambda: ParticleSystem(kind, sprite))

    def init_factories(self):
        self.add_simple_object("point", "images/engine/editor/point.png")
        self.add_simple_object("rock", "images/tiles/blocks/block11.png")
        self.add_simple_object("heavycoin", "images/objects/coin/heavy_coin.png")

        self.add_simple_tile("unstable_tile", "images/objects/unstable_tile/crumbling-1.png")

        self.add_object(AmbientSound)
        self.add_object(Background)
        self.add_object(Camera)
        self.add_object(Decal)
        self.add_object(Dispenser)
        self.add_object(SequenceTrigger)
        self.add_object(ScriptTrigger)

        self.add_object(BonusBlock)
        self.add_object(Candle)
        self.add_object(DartTrap)
        self.add_object(Door)
        self.add_object(GhostFlame)
        self.add_object(Gradient)
        self.add_object(InfoBlock)
        self.add_object(InvisibleWall)
        self.add_object(LevelTime)
        self.add_object(Platform)
        self.add_object(Powerup)
        self.add_object(Pushbutton)
        self.add_object(ResetPoint)
        self.add_object(ScriptedObject)
        self.add_object(SecretArea)
        self.add_object(SpawnPoint)
        self.add_object(Switch)
        self.add_object(Torch)
        self.add_object(Tux)
        self.add_object(Trampoline)
        self.add_object(WeakBlock)
        self.add_object(WilloWisp)
        self.add_object(Wind)

        self.add_object(WorldmapLevel)
        self.add_object(WorldmapSpawnpoint)
        self.add_object(SpecialTile)

        self.add_badguy("pneumatic-platform", "images/engine/editor/pneumaticplatform.png")
        self.add_badguy("bicycle-platform", "images/engine/editor/bicycleplatform.png")
        self.add_badguy("flying-platform", "images/objects/flying_platform/flying_platform.sprite")
        self.add_badguy("hurting_platform", "images/objects/sawblade/sawblade.sprite")

        self.add_particle_system("particles-clouds", "images/engine/editor/clouds.png", "clouds")
        self.add_particle_system("particles-rain", "images/engine/editor/rain.png", "rain")
        self.add_particle_system("particles-snow", "images/engine/editor/snow.png", "snow")

        self.load_CSV()

    def load_CSV(self):
        with open('data/supertux/objects.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                identifier = row[0]
                path = row[1]
                name = format_sprite_name(identifier) if len(row) < 3 else row[2]
                self.add_badguy(identifier, path)


supertux_gameobj_factory = SuperTuxGameObjFactory()


# EOF #
