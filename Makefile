.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: certs
certs: ## Generate self-signed certificates
	mkdir -p ./configs/ingress/certificates && \
		openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
			-keyout ./configs/ingress/certificates/privkey.pem \
			-out ./configs/ingress/certificates/fullchain.pem -subj "/CN=dashboard"

.PHONY: build
build: ## Build the docker images
	docker compose build

.PHONY: run
run: ## Bring up the compose file
	docker compose up -d

.PHONY: stop
stop: ## Bring down all docker containers
	docker compose down

.PHONY: copy-configs
copy-configs: ## Copy the latest version of the configuration files
	cp apps/dashboard_app/public/config.json configs/dashboard/
	cp apps/dashboard_app/public/i18n.json configs/dashboard/
	cp apps/tablet_app/public/config.json configs/tablet/
	cp apps/tablet_app/public/i18n.json configs/tablet/

.PHONY: get-dotlottie-player
get-dotlottie-player: ## Download dotlottie player WASM
	mkdir -p ./ingress_data/dotlottie/
	curl https://unpkg.com/@lottiefiles/dotlottie-web@0.29.2/dist/dotlottie-player.wasm -o ingress_data/dotlottie/dotlottie-player.wasm
