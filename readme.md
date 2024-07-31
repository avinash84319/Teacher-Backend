## Project Structure

---

## Tech stack used:

The tech stack used here is,

- langchain
- LLM ollama llamma3.1

---


## Project setup instructions:
	
To install the dependencies use:

```
poetry install

```

you can use requirmenets.txt file to install the dependencies also , although we recommend using poetry for the same.

Please install and setup docker before running the next steps.

To run LLM with gpu use:

Ensure you have nvidia container toolkit installed (check ollama image docs) and run the following commands:
```
docker pull ollama/ollama
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama run llama3.1

```

Reminder above commands are first time setup, for subsequent runs you can use the following command:
```

docker start ollama
docker exec -it ollama ollama run llama3.1

```



