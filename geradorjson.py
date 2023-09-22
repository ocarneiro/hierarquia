import csv, json

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

    def to_json(self):
        return json.dumps(self, ensure_ascii=False, default=lambda p: p.__dict__)

def le_origem():

    pessoa_por_id = {}

    with open('origem.csv', encoding='utf-8') as arquivo:
        origem = csv.reader(arquivo, delimiter=';')

        next(origem, None)  # pula o cabecalho
        for linha in origem:
            pessoa_lida = Pessoa(linha[0], linha[1], linha[2])
            pessoa_por_id[pessoa_lida.id] = pessoa_lida
    
    return pessoa_por_id

pessoa_por_id = le_origem()

def get_filhos(lista_ids_pais):
    niveln = []
    for i in pessoa_por_id.values():
        if i.idpai in lista_ids_pais:
            niveln.append(i.id)
            pessoa_por_id[i.idpai].add_filho(i)
    return niveln

pessoas_por_nivel = {}

# nivel0 é quem não tem pai registrado
pessoas_por_nivel[0] = [i.id for i in pessoa_por_id.values() if not i.idpai]

def gera_saida(nivel):
    pais = pessoas_por_nivel[nivel-1]
    if pais:
        pessoas_por_nivel[nivel] = get_filhos(pais)
        nivel = nivel + 1
        return nivel
    else:
        return 0

nivel = 1
while nivel:
    nivel = gera_saida(nivel)

def exibe_por_nivel():
    for i in range(len(pessoas_por_nivel)):
        print("======  Item atual: {}  =====".format(i))
        for num_pessoa in pessoas_por_nivel[i]:
            print(pessoa_por_id[num_pessoa])

    
def exibe_hierarquia(pessoa, nivel_atual = 0):
    """ função recursiva para imprimir filhos, netos, bisnetos, etc de uma pessoa  """
    recuo = "    " * nivel_atual
    print(recuo + str(pessoa))
    for filho in pessoa.filhos:
        exibe_hierarquia(filho, nivel_atual + 1)
