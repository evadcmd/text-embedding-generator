# text embedding generator

```bash
$ brew install uv just git-lfs
```

in project folder

```bash
$ git lfs install
$ git clone https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
```

run server

```bash
$ uv sync
$ just dev
```

test

```bash
$ just test
```

swagger
http://127.0.0.1:8000/docs#/

you could also use docker compose to boot it up

```bash
$ docker compose up -d
```

swagger http://127.0.0.1:5200/docs#/
