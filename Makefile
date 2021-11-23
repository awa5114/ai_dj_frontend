# ----------------------------------
#  GOOGLE CLOUD PLATFORM - STORAGE
# ----------------------------------
default: pylint

pylint:
	find . -iname "*.py" -not -path "./tests/*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

# path of the file to upload to gcp (the path of the file should be absolute or should match the directory where the make command is run)
LOCAL_PATH=raw_data/audio/

# project id
PROJECT_ID=ai-dj-76527

# bucket name
BUCKET_NAME=ai_dj_batch627_data

# bucket directory in which to store the uploaded file (we choose to name this data as a convention)
BUCKET_FOLDER=data

# name for the uploaded file inside the bucket folder (here we choose to keep the name of the uploaded file)
# BUCKET_FILE_NAME=another_file_name_if_I_so_desire.csv
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

REGION=europe-west4

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

upload_data:
	@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}


# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	@streamlit run app.py

heroku_login:
	@heroku login

heroku_create_app:
	@heroku create ${APP_NAME}

deploy_heroku:
	@git push heroku master
	@heroku ps:scale web=1
