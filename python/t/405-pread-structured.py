# libnbd Python bindings
# Copyright (C) 2010-2019 Red Hat Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import nbd
import errno

h = nbd.NBD ()
h.connect_command (["nbdkit", "-s", "--exit-with-parent", "-v",
                    "pattern", "size=512"])

expected = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00(\x00\x00\x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00H\x00\x00\x00\x00\x00\x00\x00P\x00\x00\x00\x00\x00\x00\x00X\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x00\x00\x00\x00h\x00\x00\x00\x00\x00\x00\x00p\x00\x00\x00\x00\x00\x00\x00x\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x88\x00\x00\x00\x00\x00\x00\x00\x90\x00\x00\x00\x00\x00\x00\x00\x98\x00\x00\x00\x00\x00\x00\x00\xa0\x00\x00\x00\x00\x00\x00\x00\xa8\x00\x00\x00\x00\x00\x00\x00\xb0\x00\x00\x00\x00\x00\x00\x00\xb8\x00\x00\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00\x00\xc8\x00\x00\x00\x00\x00\x00\x00\xd0\x00\x00\x00\x00\x00\x00\x00\xd8\x00\x00\x00\x00\x00\x00\x00\xe0\x00\x00\x00\x00\x00\x00\x00\xe8\x00\x00\x00\x00\x00\x00\x00\xf0\x00\x00\x00\x00\x00\x00\x00\xf8\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x08\x00\x00\x00\x00\x00\x00\x01\x10\x00\x00\x00\x00\x00\x00\x01\x18\x00\x00\x00\x00\x00\x00\x01 \x00\x00\x00\x00\x00\x00\x01(\x00\x00\x00\x00\x00\x00\x010\x00\x00\x00\x00\x00\x00\x018\x00\x00\x00\x00\x00\x00\x01@\x00\x00\x00\x00\x00\x00\x01H\x00\x00\x00\x00\x00\x00\x01P\x00\x00\x00\x00\x00\x00\x01X\x00\x00\x00\x00\x00\x00\x01`\x00\x00\x00\x00\x00\x00\x01h\x00\x00\x00\x00\x00\x00\x01p\x00\x00\x00\x00\x00\x00\x01x\x00\x00\x00\x00\x00\x00\x01\x80\x00\x00\x00\x00\x00\x00\x01\x88\x00\x00\x00\x00\x00\x00\x01\x90\x00\x00\x00\x00\x00\x00\x01\x98\x00\x00\x00\x00\x00\x00\x01\xa0\x00\x00\x00\x00\x00\x00\x01\xa8\x00\x00\x00\x00\x00\x00\x01\xb0\x00\x00\x00\x00\x00\x00\x01\xb8\x00\x00\x00\x00\x00\x00\x01\xc0\x00\x00\x00\x00\x00\x00\x01\xc8\x00\x00\x00\x00\x00\x00\x01\xd0\x00\x00\x00\x00\x00\x00\x01\xd8\x00\x00\x00\x00\x00\x00\x01\xe0\x00\x00\x00\x00\x00\x00\x01\xe8\x00\x00\x00\x00\x00\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x01\xf8'

def f (user_data, buf2, offset, s, err):
    assert err.value == 0
    err.value = errno.EPROTO
    if user_data != 42:
        raise ValueError('unexpected user_data')
    assert buf2 == expected
    assert offset == 0
    assert s == nbd.READ_DATA

buf = h.pread_structured (512, 0, lambda *args: f (42, *args))

print ("%r" % buf)

assert buf == expected

buf = h.pread_structured (512, 0, lambda *args: f (42, *args),
                          nbd.CMD_FLAG_DF)

print ("%r" % buf)

assert buf == expected

try:
    buf = h.pread_structured (512, 0, lambda *args: f (43, *args),
                              nbd.CMD_FLAG_DF)
    assert False
except nbd.Error as ex:
    assert ex.errnum == errno.EPROTO
