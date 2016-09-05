# Flexlay - A Generic 2D Game Editor
#
# ISC License
# Copyright (C) 2016 Karkus476 <karkus476@yahoo.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR ON SEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

from .file_resource import FileResource
from .text_file_resource import TextFileResource
from .path_resource import PathResource
from .image_resource import ImageResource
from .image_file_resource import ImageFileResource
from .flexlay_resource import FlexlayResource
from .text_resource import TextResource
from .translatable_text_resource import TranslatableTextResource

# We assume that the flexlay data dir is at ../../data
FLEXLAY_DATA_DIR = PathResource(PathResource.split(__file__)[:-3] + ["data"])
__all__ = ["FileResource", "TextFileResource", "PathResource", "ImageResource",
           "ImageFileResource", "FlexlayResource", "TextResource",
           "TranslatableTextResource"]
