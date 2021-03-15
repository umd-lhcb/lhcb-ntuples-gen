## Folder permission on `lxplus`
This is needed to grant collogues access to certain files stored on `lxplus`.

### AFS
AFS (mostly) ignores UNIX permissions[^1]. Instead, use `fs setacl` to control
access right:
```
fs setacl <path_to_folder_on_afs> system:anyuser read
```

To check current access permissions of a folder:
```
fs listacl <path_to_folder_on_afs>
```

!!! warning
    Only new subdirectories inherit the parent directory's permissions.

For more info, consult this link[^1].


[^1]: https://information-technology.web.cern.ch/services/fe/afs/howto/configure-afs-access-rights


### EOS
It is unclear on how to share files stored in EOS as naive `chmod` won't work
and sharing via web interface won't work.


### VNC to lxplus
First, run the VNC server on a lxplus node:
```
vncserver :8 -localhost -name Lxplus-Session -geometry 1024x768
```

If it is your first time running `vncserver`, it may prompt you to set a
remote-access password.

Unfortunately, the default `~/.vnc/xstartup` doesn't work out of box. You can
confirm that by trying to kill the newly-launched server:
```
vncserver -kill :8
```
and you may get something like this:
```
Can't find file /afs/cern.ch/user/s/suny/.vnc/lxplus732.cern.ch:8.pid
You'll have to kill the Xvnc process manually
```

Now, we need to configure a working desktop for VNC. Clear your `~/.vnc/xstartup`
and copy the following lines[^1] to that file:

```bash
#!/bin/sh

unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
icewm &
```

[^1]: Courtesy of Will

Re-launch the `vncserver` on lxplus with the same command. If the port `:8`
is taken by someone else, use a different port. Remember the lxplus hostname
(denote as `lxplus_host`) and port name (denote as `port`).

Now we need to map the VNC port to a localhost port, likely due to firewall
issues:
```
ssh -L <port>:localhost:<port> <user>@<lxplus_host>.cern.ch
```

!!! note
    - Here `port` must be in full number. e.g. `:8` -> `5908`.

Finally, we can access our remote lxplus desktop with:
```
vncviewer <port>
```
