# overleaf-hardening

Concepts of hardening one's overleaf installation to alleviate the issue that
compiles otherwise run in the context of the webserver and could access all
data in overleaf (which can be totally fine for SOHO-setups).

None of these require modifying overleaf in any way but work by swapping out
the `latexmk` binary.
This should work for pretty much any overleaf release from 2.x.x to 5.x.x.

## Overview of this repo

- `latexmk-noop.py` proof of concept python file which you put in place of
  `latexmk` (renaming the old `latexmk` to `latexmkoriginal`), which can serve
  as a template for your own approaches.
- `sidecar/` sidecar solution which uses a second privileged container running
  podman which also mounts the overleaf data directory, running a podman
  container mounting only the files for the current project for each compile

## See also

Oliver Cordes'
[sharelatex-isolation](https://github.com/ocordes/sharelatex-isolation)
provides isolation via `LD_PRELOAD`, allowing one to harden `latexmk` without
needing to use chroots or containers or different build hosts.

## Acknowledgements

Special thanks go out to Torben Gotowik from Uni Paderborn and Benedikt
Bieringer from Uni Muenster for raising the issue and helping me understand
the application side of things.
Also thanks to @vincentscode for prodividing convincing exploits.
