init:
	git clone --depth=1 https://github.com/hgascon/pulsar.git || true
	git clone --depth=1 https://github.com/tammok/PRISMA.git pulsar/modules/PRISMA || true
	cd pulsar && git checkout . && git apply ../pulsar.patch
	docker build -t pulsar:latest .
