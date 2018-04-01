all: run

run:
	docker run -p 9001:9001 -v `pwd`/oxdi/:/app oxdi
