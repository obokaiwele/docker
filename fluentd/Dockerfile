# Alpine base image is ideal because it is smaller
# But Debian base image is needed to support fluent-plugin-systemd plugin
FROM fluent/fluentd:v1.4-debian-2

LABEL maintainer="obokaiwele <https://github.com/obokaiwele>"

# Use root account to run apt commands
USER root

# Install plugins: fluent-plugin-systemd, fluentd-ui
RUN buildDeps="make gcc patch" \
  && apt-get update \
  && apt-get install -y --no-install-recommends $buildDeps \
  && apt-get install -y sudo \
  # Trim installed gems: do not install documentation
  && echo "gem: --no-document" >> /etc/gemrc \
  # Install gems as user fluent so gems can use used as user fluent
  && echo "gem: --no-document" >> ~/.gemrc \
  && gem install fluent-plugin-systemd fluentd-ui \
  && fluentd-ui setup \
  # Clear the cache by removing all sources
  # && gem sources --clear-all \
  && SUDO_FORCE_REMOVE=yes \
    apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
                  $buildDeps \
  && rm -rf /var/lib/apt/lists/* \
           /home/fluent/.gem/ruby/2.6.0/cache/*.gem \
  # Allow fluent user to start fluentd-ui
  && mkdir -p /home/fluent \
  && chown fluent:fluent /home/fluent \
  && chown fluent:fluent /usr/local/bundle/gems/fluentd-ui-1.2.1/tmp/ \
  && chown fluent:fluent /usr/local/bundle/gems/fluentd-ui-1.2.1/log
  # && adduser fluent sudo \
  # && echo "fluent     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


COPY fluent.conf /fluentd/etc/
COPY entrypoint.sh /bin/

EXPOSE 9292

# Switch to fluent user
USER fluent