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
