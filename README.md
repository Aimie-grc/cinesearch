# Lancer la stack
docker compose up -d

# Vérifier que ES est prêt
curl http://localhost:9200

# Arrêter la stack
docker compose down

# Arrêter et supprimer les volumes
docker compose down -v