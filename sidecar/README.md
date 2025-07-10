# Sidecar solution

We run a sidecar with podman.

- `Dockerfile` the Dockerfile for the sidecar container
- `latexmk.py` is copied to the overleaf main container, replacing `latexmk`
- `server.py` is run in the sidecar container, serving as endpoint for
  `latexmk.py`
- the sidecar container ideally mounts an Memory emptyDir to
  `/var/lib/containers` (or any other volume) because otherwise podman falls
  back to `vfs` storage driver, which costs like 30s per compile

## Example sidecar

If running the k8s-at-home overleaf helm chart, one needs to patch around the
deployment.
The sidecar container roughly looks like this:

```
      - name: sidecar
        # you need to push the image somewhere where you can get it
        image: podman-sandbox:testing
        imagePullPolicy: Always
        resources: {}
        securityContext:
          readOnlyRootFilesystem: false
          privileged: true
        volumeMounts:
        - mountPath: /var/lib/sharelatex
          name: data
        # this can be an emptyDir
        - mountPath: /var/lib/containers
          name: containers
```

## Known issues

- Variables like TIMEOUT etc. exist but are not fully implemented yet
- first compile after pod restart usually does not finish because we have to
  wait for podman to pull the image
- the container we currently use for latex is not really good, you are
  encouraged to use your own
