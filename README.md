# text embedding generator

```
$ brew install rye
```

```
$ brew install git-lfs
```

in project folder

```
$ git lfs install
$ git clone https://huggingface.co/intfloat/multilingual-e5-large
```

note: https://hironsan.hatenablog.com/entry/2023/07/05/073150

run server

```
$ rye sync
$ rye run dev
```

test

```
$ rye run test
```

swagger
http://127.0.0.1:8000/docs#/
