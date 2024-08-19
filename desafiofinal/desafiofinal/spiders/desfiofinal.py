import os
import scrapy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#configurando o banco
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

#Mapeamento do banco para ficar parecido com a saida em JSON
class Processos(Base):
     __tablename__ = 'Processos'
     
     id = Column(Integer, primary_Key=True)
     Doc = Column(String)
     Nprocesso = Column(String)
     DataAtuacao = Column(String) #usado como string para facilitar adição ao banco e evitar erro de cast
     Partes = Column(String)
     Materia = Column(String)
     URL = Column(String)

#escolha da função scrapy e spider para fazer a raspagem de dados
class processosFraude(scrapy.Spider):
    name = "tceprocessosfraude"
    proxpag = 0

    def start_requests(self):
        #URL de começo com a pesquisa ja implicita em Palvs=fraude+em+escolas
        yield scrapy.Request('https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+escolas&acao=Executa')

    def parse(self, response, **kwargs):
            #traz os retangulos com todas as informações a serem capturadas
            for dados in response.xpath('//tr[@class="borda-superior"]'):
                #teste para ver se é o retangulo de rodapé sem informações relevantes
                if dados.xpath('./td[@colspan=8]'):
                    break
                else:
                    #captura todos os dados para a saida
                    yield{
                        'Doc':dados.xpath('./td[@class="small "]/a[@target="_blank"]/text()').get().strip(),
                        'N processo':dados.xpath('./td[@class="small "][2]/a/text()').get().strip(),
                        'DataAtuacao':dados.xpath('./td[@class="small "][3]/text()').get().strip(),
                        'Partes':dados.xpath('./td[@class="small "][4]/text()').get() + dados.xpath('./td[@class="small "][5]/text()').get().strip(),
                        'Materia':dados.xpath('./td[@class="small "][6]/text()').get().strip(),
                        'URL':dados.xpath('./td[@class="small "]/a[@target="_blank"]/@href').get().strip()
                    }
                    #adicionando capturas no banco
                    novo_processo = Processos(Doc = dados.xpath('//tr[@class="borda-superior"]/td[@class="small "]/a[@target="_blank"]/text()').get().strip(),
                                              Nprocesso = dados.xpath('//tr[@class="borda-superior"]/td[@class="small "][2]/a/text()').get().strip(),
                                              DataAtuacao = dados.xpath('//tr[@class="borda-superior"]/td[@class="small "][3]/text()').get().strip(),
                                              Partes = dados.xpath('//tr[@class="borda-superior"]/td[@class="small "][4]/text()').get() + dados.xpath('//tr[@class="borda-superior"]/td[@class="small "][5]/text()').get().strip(),
                                              Materia = dados.xpath('//tr[@class="borda-superior"]/td[@class="small "][6]/text()').get().strip(),
                                              URL = dados.xpath('//tr[@class="borda-superior"]/td[@class="small "]/a[@target="_blank"]/@href').get().strip())
                    session = Session()
                    session.add(novo_processo)
                    session.commit
            #realiza se existe o botão de próxima página para continuar a captura
            proxima_pagina= response.xpath('//li/a[@class="page-link"]/@href').get()
            if proxima_pagina:
                self.proxpag += 10
                #chama a função recursivamente para a mesma pesquisa, mas com mais 10 novas entradas para captura
                yield scrapy.Request('https://www.tce.sp.gov.br/jurisprudencia/pesquisar?txtTdPalvs=fraude+em+escolas&acao=Executa&offset=' + str(self.proxpag),
                                      callback=self.parse)
    
if __name__ == '__main__':
     #iniciando banco
     Base.metadata.create_all(engine)

     #iniciando spider
     spider = processosFraude()
     spider.start()