.PHONY: up dry test clean

up:
	python upload.py

dry:
	python upload.py --dry-run

test:
	python upload.py --test

clean:
	del upload_log.json 2>nul & python upload.py
