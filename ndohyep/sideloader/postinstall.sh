cd "${INSTALLDIR}/${NAME}/ndohyep/"
manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/ndohyep/manage.py"

$manage migrate --settings=ndohyep.settings.production
$manage compress --settings=ndohyep.settings.production
$manage collectstatic --noinput --settings=ndohyep.settings.production
