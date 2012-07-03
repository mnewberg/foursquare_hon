#!/bin/bash                                                                              
# This is a Django, Project-specific Cron script.                                        
# Separate Projects would need a copy of this script                                     
# with appropriate Settings export statments.                                            

PYTHONPATH="${PYTHONPATH}:/var/www/four_staging/foursquare"
export PYTHONPATH
export DJANGO_SETTINGS_MODULE=settings

git pull origin staging
