# -*- coding: utf-8 -*-
# Copyright (c) 2011 Ionuț Arțăriși <iartarisi@suse.cz>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from popcorn.configs import rdb

ARCHES = ['i586', 'x86_64']

class System(object):
    """A System is a user machine that we want to track.

    A system is identified by a smolt hw_uuid (generated by smolt and
    typically stored in /etc/smolt/hw-uuid). Ids are stored in the set
    'distro:%(distro)s:systems' and incremented in 'global:nextSystemId'.

    A hash is stored in 'system:%(hw_uuid)s' containing:
     - arch - the architecture of the system

    """
    @classmethod
    def get_all_ids(cls):
        """Return a set of the ids of all the System objects"""
        return rdb.smembers('systems')

    # XXX think about memoizing the objects in this class, so they don't
    # get created every time we need to look for one
    def __init__(self, hw_uuid, arch):
        """Check if the system is in our database and create it if it isn't

        :arg hw-uuid: smolt hw-uuid to uniquely indentify each system

        """
        self.hw_uuid = hw_uuid

        key = 'system:%s' % hw_uuid
        try:
            self.id = rdb[key]
        except KeyError:
            self.id = str(rdb.incr('global:nextSystemId'))

            # TODO - distros
            rdb.sadd('systems', hw_uuid)
            rdb[key] = self.id

            # XXX see if this constraint can go in the database,
            # otherwise just make it prettier
            assert arch in ARCHES
            rdb.hset('system:%s' % self.id, 'arch', arch)

    def __repr__(self):
        return self.id
