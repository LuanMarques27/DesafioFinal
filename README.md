Para realizar o desafio proposto, foi escolhida a classe Scrapy Spider para a raspagem de dados. Todo o código desenvolvido está localizado no caminho desafiofinal/spiders/desafiofinal.py. Os dados extraídos durante a execução foram salvos em formato JSON e podem ser encontrados no arquivo desafiofinal/dados.json.

A biblioteca OS foi utilizada para mapear o caminho da URL na máquina de produção, facilitando assim a criação do banco de dados. O ambiente de desenvolvimento foi containerizado utilizando o Anaconda Prompt, onde foram instaladas todas as bibliotecas necessárias para a execução da aplicação.

O arquivo JSON foi gerado diretamente a partir do VS Code, utilizando o prompt para rodar o comando scrapy crawl imdb -O dados.json. Esse comando executou o script responsável pela raspagem de dados e gerou a saída no formato desejado.
