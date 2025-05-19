#───────────────────────────────────────────────────────────
#  Makefile : docker-compose helper (dev & prod)
#───────────────────────────────────────────────────────────

# 기본값 : make → dev 스택 기동
.DEFAULT_GOAL := dev

# 파일 경로
DEV_COMPOSE  := docker-compose.yml
PROD_COMPOSE := docker-compose.prod.yml
DEV_ENV  := ./backend/.dev.env
PROD_ENV := ./backend/.prod.env

# ──────────────── Dev Stack ────────────────
dev:
	@echo "🚀  Starting DEV stack..."
	docker compose -f $(DEV_COMPOSE) --env-file $(DEV_ENV) up -d --build

dev-clean:
	@echo "🧹  Stopping & removing DEV containers..."
	docker compose -f $(DEV_COMPOSE) --env-file $(DEV_ENV) down

dev-fclean:
	@echo "🔥  FULL clean (DEV containers, volumes, images)..."
	docker compose -f $(DEV_COMPOSE) --env-file $(DEV_ENV) down --rmi local
    # db_data volume은 삭제하지 않음 

dev-re: dev-clean dev    # down → up

# ──────────────── Prod Stack ───────────────
prod:
	@echo "🚀  Starting PROD stack..."
	docker compose -f $(PROD_COMPOSE) --env-file $(PROD_ENV) up -d --build

prod-clean:
	@echo "🧹  Stopping & removing PROD containers..."
	docker compose -f $(PROD_COMPOSE) --env-file $(PROD_ENV) down

prod-fclean:
	@echo "🔥  FULL clean (PROD containers, volumes, images)..."
	docker compose -f $(PROD_COMPOSE) --env-file $(PROD_ENV) down --rmi local
    # db_data volume은 삭제하지 않음

prod-re: prod-clean prod

# ──────────────── 편의 별칭 ────────────────
all: dev
clean:  dev-clean
fclean: dev-fclean
re:     dev-re

.PHONY: dev prod dev-clean prod-clean dev-fclean prod-fclean dev-re prod-re clean fclean re all
