FROM ghcr.io/prefix-dev/pixi:latest

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install package and its dependencies.
RUN pixi install -e app --locked

CMD pixi r -e app serve
