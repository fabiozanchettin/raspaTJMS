
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import random
import time
import clipboard
import chardet
import csv
import re


# some other code here...
driver = webdriver.Chrome() # substitua pelo driver de sua preferência
driver.get("https://esaj.tjms.jus.br/cjsg/consultaCompleta.do")
#driver = webdriver.Chrome(r"C:/Users/Fabio/Downloads/chromedriver_win32/chromedriver.exe")
driver.implicitly_wait(2)

random_time = random.randint(1, 2)
time.sleep(random_time)

ementa = driver.find_element(By.XPATH, "//*[@id='iddados.buscaEmenta']")
texto = "AMBIENTAL"
for c in texto:
    ementa.send_keys(c)
    time.sleep(random.uniform(0.01, 0.1))
    random_time = random.randint(0, 1)
    time.sleep(random_time)

dataJulgamento = driver.find_element(By.XPATH, "//*[@id='iddados.dtJulgamentoInicio']")
texto1 = "01/01/2020"

for c in texto1:
    dataJulgamento.send_keys(c)
    time.sleep(random.uniform(0.01, 0.1))
    random_time = random.randint(0, 1)
    time.sleep(random_time)

dataFinal = driver.find_element(By.XPATH, "//*[@id='iddados.dtJulgamentoFim']")
texto2 = "31/01/2020"
for c in texto2:
    dataFinal.send_keys(c)
    time.sleep(random.uniform(0.01, 0.1))
    random_time = random.randint(0, 1)
    time.sleep(random_time)

pesquisar = driver.find_element(By.XPATH, "//*[@id='pbSubmit']")
pesquisar.click()

random_time = random.randint(0, 1)
time.sleep(random_time)

pesquisar = driver.find_element(By.XPATH, "//*[@id='pbSubmit']")
pesquisar.click()

# Abra o arquivo em modo append

numero_linha = 1
with open('teste.txt', 'a') as f:
    numero_linha = 1
    pagina_atual = 1
    while True:
        # Encontre todos os botões de visualização de ementa e itere sobre eles
        botoes_ementa = driver.find_elements(By.XPATH, '//*[@id="divDadosResultado-A"]//a[3]/img')
        for botao in botoes_ementa:
            botao.click()
            time.sleep(1)
            a = ActionChains(driver)
            a.key_down(Keys.CONTROL).send_keys('C').key_up(Keys.CONTROL).perform()
            texto = clipboard.paste()
            # Escreva o conteúdo em uma nova linha do arquivo
            f.write(f'{numero_linha} - {texto}\n')
            numero_linha += 1
            # Feche o modal
            botao_fechar = driver.find_element(By.XPATH, '//*[@id="popupModalBotaoFechar"]')
            botao_fechar.click()
        # Verifique se há uma próxima página
        try:
            proxima_pagina = driver.find_element(By.XPATH,
                                                 '//*[@id="paginacaoSuperior-A"]/table/tbody/tr[1]/td[2]/div/a[@name="A%d"]' % (
                                                             pagina_atual + 1))
            proxima_pagina.click()
            pagina_atual += 1
            time.sleep(1)
        except NoSuchElementException:
            print("Não há mais páginas.")
            break

# Feche o driver do Selenium
driver.quit()

with open('teste.txt', 'rb') as dados:
    resultado = chardet.detect(dados.read())
    #print(resultado)

with open('teste.txt', 'r', encoding=resultado['encoding']) as dados:
    dadosIniciais = dados.read()
    lista = dadosIniciais.splitlines()
    nova_lista = [item for item in lista if item != '']
    #pprint.pprint(nova_lista)

    #print('\n'.join(nova_lista))
    #print('a lista tem: ' + str(len(nova_lista)))
    #for item in nova_lista:
        #print(item, end='\n')
        #print('----------------')
nova_lista3 = []
for i in range(1, len(nova_lista),2):
    match = re.findall(r'\(TJMS\.\s*(.*?) n\.\s*(.{25})', nova_lista[i])

    if match:
        # Encontra as posições das cinco primeiras vírgulas na string
        posicao_virgula_1 = nova_lista[i].find(',')
        posicao_virgula_2 = nova_lista[i].find(',', posicao_virgula_1 + 1)
        posicao_virgula_3 = nova_lista[i].find(',', posicao_virgula_2 + 1)
        posicao_virgula_4 = nova_lista[i].find(',', posicao_virgula_3 + 1)
        posicao_virgula_5 = nova_lista[i].find(',', posicao_virgula_4 + 1)

        # Extrai o conteúdo entre as vírgulas e adiciona à lista match[0]
        conteudo_entre_virgulas_1 = nova_lista[i][posicao_virgula_1 + 1:posicao_virgula_2]
        conteudo_entre_virgulas_2 = nova_lista[i][posicao_virgula_2 + 1:posicao_virgula_3]
        conteudo_entre_virgulas_3 = nova_lista[i][posicao_virgula_3 + 1:posicao_virgula_4]
        conteudo_entre_virgulas_4 = nova_lista[i][posicao_virgula_4 + 1:posicao_virgula_5]
        conteudo_entre_virgulas_5 = nova_lista[i][posicao_virgula_5 + 1:].strip()

        match = list(match[0])
        match.append(conteudo_entre_virgulas_1)
        match.append(conteudo_entre_virgulas_2)
        match.append(conteudo_entre_virgulas_3)
        match.append(conteudo_entre_virgulas_4)
        match.append(conteudo_entre_virgulas_5)

        # Cria a nova lista
        nova_lista1 = [nova_lista[0], match]

        nova_lista2 = []
        nova_lista2.extend(nova_lista1[1])
        nova_lista2.append(nova_lista1[0])
        #print(nova_lista2)
        for i in range(len(nova_lista2)):
            nova_lista2[i]=nova_lista2[i].strip()



    else:
        print("Não foi possível encontrar as informações do processo.")

    for j in range(4, 7): # seleção do 4º, 5º e 6º elemento (os índices começam em 0)
        nova_lista2[j] = nova_lista2[j].split(':')[1].strip() # divide a string pelo caractere ':' e seleciona a parte desejada (índice 1), removendo espaços em branco
        #print(nova_lista2)

    for k in range(6,7):

        nova_lista2[6] = nova_lista2[6][:-1]
        nova_lista2[7] = nova_lista2[7][4:]


        #print(nova_lista2)
        nova_lista3.append(nova_lista2)


with open('teste.csv', 'w', newline='', encoding='cp1252') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Tipo', 'Número', 'Comarca', 'Câmara', 'Relator', 'Data de julgamento', 'Data de publicação', 'Ementa'])
    for item in nova_lista3:
        writer.writerow(item)
print('Fim!!!')


