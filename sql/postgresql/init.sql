REVOKE ALL ON schema public FROM public;

CREATE ROLE s1 WITH LOGIN PASSWORD 'students@mysql@DB3' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION VALID UNTIL 'infinity';

CREATE ROLE teacher WITH LOGIN PASSWORD 'Oj4dblcui_' NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION VALID UNTIL 'infinity';
GRANT ALL ON schema public TO teacher;
ALTER USER teacher CREATEDB;
ALTER USER teacher with superuser;
