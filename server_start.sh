docker start ollama

docker exec -it ollama ollama run llama3.1 > /dev/null 2>&1 &

poetry shell

flask --app server.py run > /dev/null 2>&1 &

ngrok http --domain=pet-muskox-honestly.ngrok-free.app 5000