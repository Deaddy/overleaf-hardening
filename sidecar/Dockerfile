FROM ubuntu:jammy

# jammy jellyfish
# 22.04 LTS release
#
#                                       ?
#                                     .
#                                    '
#                     _ -- ~~~ -- _      _______
#                 .-~               ~-.{__-----. :
#               /                       \      | |
#              :         O     O         :     | |
#              /\                       /------' j
#             { {/~-.               .-~\~~~~~~~~~
#              \/ /  |~:- .___. -.~\  \ \
#             / /\ \ | | { { \ \  } }  \ \
#            { {   \ \ |  \ \  \ \ /    } }
#             \ \   /\ \   \ \  /\ \   { {
#              } } { { \ \  \ \/ / \ \  \ \
#             / /   } }  \ \ }{ {    \ \ } }
#            / /   { {     \ \{\ \    } { {
#           / /     } }     } }\\ \  / / \ \
#          `-'     { {     `-'\ \`-'/ /   `-'
#                   `-'        `-' `-'

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt -y update && apt -y upgrade

# We install a few more tools for debugging etc.
RUN apt -y install \
# localhost
  wget \
  htop \
  vim \
  pv \
  curl \
  rsync \
# network
  netcat \
  telnet \ 
  qperf \
  traceroute \
# for the sidecar we only need those
  python3-flask \
  gunicorn \
  podman

RUN date > /builddate
ADD "server.py" "/server.py"

#CMD ["/server.py"]
CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:6666", "--access-logfile=-", "--error-logfile=-", "--timeout", "600",  "server:app"]

