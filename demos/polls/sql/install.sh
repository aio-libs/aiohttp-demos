# determine os
unameOut="$(uname -s)"
case "${unameOut}" in
    Darwin*)    pg_cmd="psql -U postgres";;
    *)          pg_cmd="sudo -u postgres psql"
esac

pg_cmd+=" -h $DB_HOST -p $DB_PORT"
echo "pg_cmd is '$pg_cmd'"

${pg_cmd} -c "DROP DATABASE IF EXISTS $DB_NAME"
${pg_cmd} -c "DROP ROLE IF EXISTS $DB_USER"
${pg_cmd} -c "CREATE USER $DB_USER WITH PASSWORD '$DB_USER';"
${pg_cmd} -c "CREATE DATABASE $DB_NAME ENCODING 'UTF8';"
${pg_cmd} -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

cat sql/create_tables.sql | ${pg_cmd} -d $DB_NAME -U $DB_USER -a
cat sql/sample_data.sql | ${pg_cmd} -d $DB_NAME -U $DB_USER -a
