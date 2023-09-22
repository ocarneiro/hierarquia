import csv

class Pessoa:
    """Uma pessoa que pode ter um pai registrado. Ou não."""
    def __init__(self, id, nome, idpai):
        self.id = id
        self.nome = nome
        self.idpai = idpai
        self.filhos = []

    def __repr__(self):
        return "{}: {}, filho de {}".format(self.id, self.nome, self.idpai if self.idpai else "ninguém")
    
    def add_filho(self, filho):
        self.filhos.append(filho)

def le_origem():

    dict_origem = {}

    with open('origem.csv', encoding='utf-8') as arquivo:
        origem = csv.reader(arquivo, delimiter=';')

        next(origem, None)  # pula o cabecalho
        for linha in origem:
            pessoa_lida = Pessoa(linha[0], linha[1], linha[2])
            dict_origem[pessoa_lida.id] = pessoa_lida
    
    return dict_origem

dict_origem = le_origem()

def get_filhos(lista_ids_pais):
    niveln = []
    for i in dict_origem.values():
        if i.idpai in lista_ids_pais:
            niveln.append(i.id)
            dict_origem[i.idpai].add_filho(i)
    return niveln

saida = {}

# nivel0 é quem não tem pai registrado
saida[0] = [i.id for i in dict_origem.values() if not i.idpai]

def gera_saida(nivel):
    pais = saida[nivel-1]
    if pais:
        saida[nivel] = get_filhos(pais)
        nivel = nivel + 1
        return nivel
    else:
        return 0

nivel = 1
while nivel:
    nivel = gera_saida(nivel)

def exibe_por_nivel():
    for i in range(len(saida)):
        print("======  Item atual: {}  =====".format(i))
        for num_pessoa in saida[i]:
            print(dict_origem[num_pessoa])

