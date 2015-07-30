manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/manage.py"
cd "${INSTALLDIR}/${NAME}/"
export DJANGO_SETTINGS_MODULE=ndohyep.settings.production
$manage migrate

# process static files
$manage collectstatic --noinput
$manage compress

# compile i18n strings
$manage compilemessages
