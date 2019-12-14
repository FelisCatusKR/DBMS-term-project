# postgis docker 띄우는 명령어

`docker run -d -p 5432:5432 --env-file app.env --name psql -it --rm -v pgdata:/var/lib/postgresql/data mdillon/postgis:11-alpine`
