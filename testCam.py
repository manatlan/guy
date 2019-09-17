#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import guy,datetime

class Cam(guy.Guy):
    __doc__="""
<video autoplay></video>

<script>
guy.init( function() {
    const constraints = {video: true};
    const video = document.querySelector('video');
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {video.srcObject = stream});
})
</script>"""


if __name__ == "__main__":
    Cam().run()
