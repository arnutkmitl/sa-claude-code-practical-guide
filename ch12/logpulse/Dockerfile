FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

# Run as an unprivileged user; logpulse only reads files.
RUN useradd --create-home pulse
USER pulse

ENTRYPOINT ["logpulse"]
CMD ["--help"]
