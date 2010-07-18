###
# Copyright (c) 2010, Chris Swingler
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import MaruGet
from random import randint


class MaruBlog(callbacks.Plugin):
    """
    This plugin gets a Maru blog post.
    Simlpy call say "maru postnumber" and the post will
    be returned to the channel. Omitting the postnumber
    will get the most recent post.
    """
    pass
 
    def maru(self, irc, msg, args, channel, num=None):
        """ [<post number>]

        Prints a blog post to the channel.  If no post number is given,
        returns a random entry.
        """
        if(num == None):
            self.log.info("Randomly getting a maru post:")
            latestM = MaruGet.MaruBlog()
            postNum = randint(2,latestM.latestPost())
        else:
            postNum = num
        self.log.info("Getting maru post number: " + str(postNum))
        m = MaruGet.MaruBlog(postNum)
        r = m.ircContent()
        self.log.debug("Maruing %q in %s due to %s.",
                r, channel, msg.prefix)
        self.log.debug("Type: %s ", type(r))
        r = unicode(r).encode("utf-8")
        maruList = list()

        irc.queueMsg(ircmsgs.privmsg(channel, "Maru blog entry #" +\
            str(postNum) +" (" + m.maruUrl + ")" +":"))
        for maruLine in r.split('\n'):
            try:
                maruList.append(unicode(maruLine).encode("ascii"))
            except UnicodeDecodeError:
                pass
        for line in maruList:
            irc.queueMsg(ircmsgs.privmsg(channel, line))
        irc.noReply()
    maru = wrap(maru, ['inChannel', optional('int')])

    def randmaru(self, irc, msg, args, channel):
        """
        Deprecated.  Use maru with no parameters instead.
        """
        irc.queueMsg(ircmsgs.privmsg(channel, "'randmaru' will be " +\
                "abolished. Use the 'maru' with no parameters " +\
                "instead of the circle. Mew."))
        irc.noReply()
    randmaru = wrap(randmaru, ['inChannel'])

    def hug(self, irc, msg, args, channel):
        """
        Huuuuuuuuuuuuuuuugs!
        """
        irc.queueMsg(ircmsgs.privmsg(channel,
        "http://lakupo.com/qu/ghacks/userpics/philippe-hugs.jpg"))
        irc.noReply()
        return
    hug = wrap(hug, ['inChannel'])

Class = MaruBlog

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
