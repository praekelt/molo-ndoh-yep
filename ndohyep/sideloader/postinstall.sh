cd "${INSTALLDIR}/${NAME}/ndohyep/"
manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/ndohyep/manage.py"

$manage migrate
$manage compress
$manage collectstatic --noinput
