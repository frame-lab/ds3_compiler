FROM movesrwth/stormpy:travis
COPY . /app
RUN bash -c "source /opt/venv/bin/activate && pip install lark-parser"