# ClearAir's image. Build it in clearair/ with: docker build -t clearair:0.1.0 .
#
# TODO(task 23): write the image, following uv's Docker guide:
#   - FROM the Python 3.12 slim image in the kit's VERSIONS.md, and uv copied in with COPY --from= the uv image there;
#   - WORKDIR /app, then pyproject.toml and uv.lock copied and the locked libraries installed
#     (uv sync --locked --no-dev --no-install-project) in their own layer, before any code;
#   - then the clearair package and the sql folder, the virtual environment on PATH,
#     ENTRYPOINT python -m clearair.cli and CMD load-api.
# Never copy .env into the image and never set the key with ENV: settings arrive when the container starts.
