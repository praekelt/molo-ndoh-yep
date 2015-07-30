manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/manage.py"
cd "${INSTALLDIR}/${NAME}/"
$manage migrate --settings=ndohyep.settings.production

# process static files
$manage compress --settings=ndohyep.settings.production
$manage collectstatic --noinput --settings=ndohyep.settings.production

# compile i18n strings
$manage compilemessages --settings=ndohyep.settings.production
