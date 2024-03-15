## Build and Run Docker container
Run `docker build -t prompting .`

Run `docker run -p 6969:6969 -v ~/.config/gcloud:/etc/creds/ -d prompting`