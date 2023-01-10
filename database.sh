docker run -d \
	--name postgres_gpuser \
	-p 5432:5432 \
	--env-file=.env \
	-v gpuser:/var/lib/postgresql/data \
	postgres
