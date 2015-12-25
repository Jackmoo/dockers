# Use phusion/baseimage as base image. To make your builds
# reproducible, make sure you lock down to a specific version, not
# to `latest`! See
# https://github.com/phusion/baseimage-docker/blob/master/Changelog.md
# for a list of version numbers.

# -p 18888:18888 for port mapping/expose

FROM phusion/baseimage:0.9.18

MAINTAINER jiok <jiokmoo@gmail.com>

# Set environment variables

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# Usermod setting
#RUN \
#  usermod -u 99 hathuser && \
#  usermod -g 100 hathuser && \
#  usermod -d /home hathuser && \
#  chown -R hathuser:users /home

# Install java
RUN \
  add-apt-repository "deb http://us.archive.ubuntu.com/ubuntu/ trusty universe multiverse" && \
  add-apt-repository "deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates universe multiverse" && \
  apt-get update -q && \
  apt-get install -qy wget default-jre zip && \
  apt-get clean -y && \
  rm -rf /var/lib/apt/lists/*
  
# Get/unzip hath program, WARNING!! no verification on hash
RUN \
  mkdir /home/hath && \
  cd /home/hath && \
  wget http://hentaiathome.net/get/HentaiAtHome_1.2.6.zip && \
  unzip HentaiAtHome_1.2.6.zip

# expose/copy script to hath folder
ADD hath_config.conf /home/hath/
ADD start_hath_pty.py /home/hath/
  
# now, all execution handle in python script
RUN \
  cd /home/hath && \
  python start_hath_pty.py

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*