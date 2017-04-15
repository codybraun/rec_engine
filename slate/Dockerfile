FROM ruby:2.2.6-onbuild
EXPOSE 8002
VOLUME /usr/src/app/source
RUN apt-get update && apt-get install -y nodejs \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["bundle", "exec", "middleman", "server", "--watcher-force-polling"]
