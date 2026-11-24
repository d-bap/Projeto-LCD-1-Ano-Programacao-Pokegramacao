import random

class Mensagens:
    ERRO_NIVEL_INVALIDO = "O nível tem de estar entre 1 e 100."
    ERRO_NIVEL_MAX = "O nível máximo é 100."
    ERRO_POKEMON_NAO_ENCONTRADO = "O Pokémon não existe."
    ERRO_EQUIPA_CHEIA = "A equipa está cheia."
    ERRO_EQUIPA_VAZIA = "A equipa está vazia."
    ERRO_POSICAO_INVALIDA = "Posição inválida."
    ERRO_NOME_INVALIDO = "Nome inválido."
    ERRO_NOME_DUPLICADO = "Já existe um treinador com esse nome."
    ERRO_TREINADOR_NAO_ENCONTRADO = "O treinador não existe."
    ERRO_TREINADORES_IGUAIS = "Um treinador não pode batalhar contra si próprio."
    ERRO_SEM_TREINADORES = "Não existem treinadores."
    ERRO_EQUIPAS_VAZIAS = "Todas as equipas estão vazias."

    ERRO_OPCAO_INVALIDA = "Opção inválida."
    ERRO_FICHEIRO_INVALIDO = "Ficheiro inválido."

    PEDIDO_OPCAO = "> "
    PEDIDO_FICHEIRO = "Ficheiro: "
    PEDIDO_NOME = "Nome: "
    PEDIDO_TREINADOR = "Treinador: "
    PEDIDO_FILTRO = "Filtro: "
    PEDIDO_POSICAO = "Posição: "

    REPRESENTACAO_POKEMON = "{nome} (Nível: {nivel})"
    REPRESENTACAO_TREINADOR = "Treinador {nome} (Vitórias: {vitorias})"
    CAPTURA_SUCESSO = "Capturou um {pokemon}!"
    BATALHA_VITORIA = "{vencedor} venceu a batalha!"
    BATALHA_EMPATE = "Empate..."


# Opções dos menus (T7-T10)

OPCOES_PRINCIPAL = (
    "Menu de treinador",
    "Gerir estádio Pokémon",
    "Estatísticas"
)

OPCOES_GESTAO = (
    "Listar treinadores",
    "Adicionar treinador",
    "Carregar treinadores",
    "Gravar treinadores"
)

OPCOES_TREINADOR = (
    "Ver equipa",
    "Capturar Pokémon",
    "Remover da equipa",
    "Batalhar"
)

OPCOES_ESTATISTICAS = (
    "Top 10",
    "Média de vitórias",
    "Equipa mais experiente",
    "Pokémon mais comum",
    "Distribuição de tipos"
)

# Escreva aqui as classes Pokemon, Pokedex, Treinador e EstadioPokemon (T1-T6)

class Pokemon:
    def __init__(self, nome, tipos, nivel):
        if not isinstance(nivel, int) or not 1 <= nivel <= 100:
            raise ValueError(Mensagens.ERRO_NIVEL_INVALIDO)
        self.__nome = nome
        self.__tipos = tuple(tipos)
        self.__nivel = nivel

    def __str__(self):
        return Mensagens.REPRESENTACAO_POKEMON.format(nome=self.__nome, nivel=self.__nivel)

    def __eq__(self, other):
        if not isinstance(other, Pokemon):
            return False
        return self.__nome == other.__nome and self.__nivel == other.__nivel

    @property
    def nome(self):
        return self.__nome

    @property
    def tipos(self):
        return self.__tipos

    @property
    def nivel(self):
        return self.__nivel

    def subir_nivel(self):
        self.__nivel += 1

class Pokedex:
    def __init__(self, ficheiro=None):
        self.__ficheiro = ficheiro

    @property
    def especies(self):
        nomes = []
        f = open(self.__ficheiro, "r", encoding="utf-8")
        for linha in f:
            linha = linha.strip()
            if linha != "":
                nomes.append(linha.split(",")[0].strip())
        f.close()
        return tuple(nomes)

    def carregar_pokemon(self, ficheiro):
        f1 = open(self.__ficheiro, "r", encoding="utf-8")
        f1_1 = open(self.__ficheiro, "a", encoding="utf-8")
        f2 = open(ficheiro, "r", encoding="utf-8")
        linha1 = f1.readline(-1)
        if linha1 != "":
            f1_1.write("\n")
        for linha in f2:
            if linha.strip() != "":
                f1_1.write(linha)
        f1.close()
        f1_1.close()
        f2.close()

    def gerar_pokemon(self, nome, nivel):
        f = open(self.__ficheiro, "r", encoding="utf-8")
        for linha in f:
            pok = []
            for word in linha.strip().split(","):
                pok.append(word.strip())
            if nome.strip() == pok[0]:
                f.close()
                return Pokemon(nome, pok[1:], nivel)
        raise ValueError(Mensagens.ERRO_POKEMON_NAO_ENCONTRADO)

    def gerar_pokemon_aleatorio(self):
        lvl = int(random.random() ** 2 * 100) + 1
        nome = random.choice(self.especies)
        return self.gerar_pokemon(nome, lvl)

class Treinador:
    def __init__(self, nome, vitorias=0):
        self.__nome = nome
        self.vitorias = vitorias
        self.__team = []

    def __str__(self):
        return Mensagens.REPRESENTACAO_TREINADOR.format(nome=self.__nome, vitorias=self.vitorias)

    def __eq__(self, other):
        if not isinstance(other, Treinador):
            return False
        return self.__nome == other.__nome

    @property
    def nome(self):
        return self.__nome

    @property
    def equipa(self):
        return tuple(self.__team)

    @property
    def experiencia_equipa(self):
        total = 0
        for pokemon in self.equipa:
            total += pokemon.nivel
        return total

    def vitorias(self):
        return self.vitorias

    def capturar_pokemon(self, pokemon):
        if len(self.equipa) >= 6:
            raise ValueError(Mensagens.ERRO_EQUIPA_CHEIA)
        self.__team.append(pokemon)

    def remover_da_equipa(self, posicao):
        if not 0 <= posicao <= len(self.equipa) - 1:
            raise ValueError(Mensagens.ERRO_POSICAO_INVALIDA)
        pokemon = self.equipa[posicao]
        del self.__team[posicao]
        return pokemon

    def vencer_batalha(self):
        self.vitorias += 1
        for pokemon in self.equipa:
            if pokemon.nivel < 100:
                pokemon.subir_nivel()

class EstadioPokemon:
    def __init__(self, nome):
        self.__nome = nome
        self.__lst_treinadores = []

    @property
    def nome(self):
        return self.__nome

    @property
    def treinadores(self):
        return tuple(self.__lst_treinadores)

    def adicionar_treinador(self, nome):
        if "," in nome or nome == "":
            raise ValueError(Mensagens.ERRO_NOME_INVALIDO)
        for treinador in self.__lst_treinadores:
            if treinador.nome == nome:
                raise ValueError(Mensagens.ERRO_NOME_DUPLICADO)
        novo = Treinador(nome)
        self.__lst_treinadores.append(novo)
        return novo

    def obter_treinador(self, nome):
        for treinador in self.__lst_treinadores:
            if treinador.nome == nome:
                return treinador
        raise ValueError(Mensagens.ERRO_TREINADOR_NAO_ENCONTRADO)

    def batalhar(self, nome1, nome2):
        if nome1 == nome2:
            raise ValueError(Mensagens.ERRO_TREINADORES_IGUAIS)
        t1 = self.obter_treinador(nome1)
        t2 = self.obter_treinador(nome2)
        if len(t1.equipa) == 0 or len(t2.equipa) == 0:
            raise ValueError(Mensagens.ERRO_EQUIPA_VAZIA)
        exp1 = t1.experiencia_equipa
        exp2 = t2.experiencia_equipa
        if exp1 > exp2:
            t1.vencer_batalha()
            return t1
        elif exp1 < exp2:
            t2.vencer_batalha()
            return t2
        else:
            return None

    def gravar_treinadores(self, ficheiro):
        f = open(ficheiro, "w", encoding="utf-8")
        for treinador in self.__lst_treinadores:
            f.write(f"T,{treinador.nome},{treinador.vitorias}\n")
            for pokemon in treinador.equipa:
                f.write(f"P,{pokemon.nome},{pokemon.nivel}\n")
        f.close()

    def carregar_treinadores(self, ficheiro, pokedex):
        novos = []
        nomes = []
        for t in self.__lst_treinadores:
            nomes.append(t.nome)
        atual = None
        f = open(ficheiro, "r", encoding="utf-8")
        try:
            for linha in f:
                linha = linha.strip().split(",")
                if linha == [""]:
                    continue
                if len(linha) != 3:
                    raise ValueError
                tipo, nome, num = linha
                match tipo:
                    case "T":
                        num = int(num)
                        if nome in nomes or num < 0:
                            raise ValueError
                        atual = Treinador(nome, num)
                        nomes.append(atual.nome)
                        novos.append(atual)
                    case "P":
                        num = int(num)
                        if atual is None or not 1 <= num <= 100:
                            raise ValueError
                        atual.capturar_pokemon(pokedex.gerar_pokemon(nome, num))
                    case _:
                        raise ValueError
        finally:
            f.close()
        for t in novos:
            self.__lst_treinadores.append(t)

    def top10(self):
        top = []
        vits = []
        for t in self.__lst_treinadores:
            vits.append(t)
        while len(top) < 10 and len(vits) > 0:
            big = vits[0]
            for t in vits:
                if big.vitorias < t.vitorias:
                    big = t
            top.append(big)
            vits.remove(big)
        return tuple(top)

    def media_vitorias(self):
        if len(self.__lst_treinadores) == 0:
            raise ValueError(Mensagens.ERRO_SEM_TREINADORES)
        vits = []
        for t in self.__lst_treinadores:
            vits.append(t.vitorias)
        return sum(vits)/len(vits)

    def equipa_mais_experiente(self):
        vits = []
        count = 0
        for t in self.__lst_treinadores:
            vits.append(t)
        if len(vits) == 0:
            raise ValueError(Mensagens.ERRO_EQUIPAS_VAZIAS)
        big = vits[0]
        for t in vits:
            if big.experiencia_equipa < t.experiencia_equipa:
                big = t
            count += len(t.equipa)
        if count == 0:
            raise ValueError(Mensagens.ERRO_EQUIPAS_VAZIAS)
        return big

    def pokemon_mais_comum(self):
        freqs = {}
        for t in self.__lst_treinadores:
            for pokemon in t.equipa:
                if pokemon.nome not in freqs:
                    freqs[pokemon.nome] = 1
                else:
                    freqs[pokemon.nome] += 1
        if len(freqs) == 0:
            raise ValueError(Mensagens.ERRO_EQUIPAS_VAZIAS)
        mais_freq = None
        for pokemon in freqs:
            if mais_freq is None or freqs[pokemon] > freqs[mais_freq]:
                mais_freq = pokemon
        return mais_freq

    def distribuicao_tipos(self):
        dist = {}
        total_pok = 0
        for t in self.__lst_treinadores:
            total_pok += len(t.equipa)
        if total_pok == 0:
            raise ValueError(Mensagens.ERRO_EQUIPAS_VAZIAS)
        for t in self.__lst_treinadores:
            for pokemon in t.equipa:
                for tipo in pokemon.tipos:
                    if tipo not in dist:
                        dist[tipo] = 1/total_pok
                    else:
                        dist[tipo] += 1/total_pok
        return dist

def check(opcoes, exit_txt):
    count = 1
    for mss in opcoes:
        print(f"{count}. {mss}")
        count += 1
    print(f"0. {exit_txt}")
    while True:
        try:
            escolha = int(input("> "))
        except ValueError:
            print(Mensagens.ERRO_OPCAO_INVALIDA)
        else:
            if 0 <= escolha <= len(opcoes):
                return escolha
            print(Mensagens.ERRO_OPCAO_INVALIDA)

def menu_principal():
    pokedex = Pokedex("pokemon.txt")
    pg = EstadioPokemon("Pokégramação")
    while True:
        match check(OPCOES_PRINCIPAL, "Sair"):
            case 1:
                # Menu de treinador
                nome = input("Treinador: ")
                try:
                    trainer = pg.obter_treinador(nome=nome)
                except ValueError as e:
                    print(e)
                else:
                    menu_de_treinador(pokedex, pg, trainer)
            case 2:
                # Menu de gestão
                menu_de_gestao(pokedex, pg)
            case 3:
                # Menu de estatística
                menu_de_estatistica(pg)
            case 0:
                # fechar
                break

def menu_de_treinador(pokedex, estadio, treinador):
    while True:
        match check(OPCOES_TREINADOR, "Voltar"):
            case 1:
            # Ver equipa
                if len(treinador.equipa) == 0:
                    print(Mensagens.ERRO_EQUIPA_VAZIA)
                else:
                    for pokemon in treinador.equipa:
                        print(pokemon)
            case 2:
                # Capturar Pokémon
                try:
                    new = pokedex.gerar_pokemon_aleatorio()
                    treinador.capturar_pokemon(new)
                except ValueError as e:
                    print(e)
                else:
                    print(Mensagens.CAPTURA_SUCESSO.format(pokemon=new))
            case 3:
                # Remover da equipa
                if not treinador.equipa:
                    print(Mensagens.ERRO_EQUIPA_VAZIA)
                else:
                    count = 1
                    for pokemon in treinador.equipa:
                        print(f"{count}. {pokemon}")
                        count += 1
                    try:
                        posicao = int(input("Posição: "))
                    except ValueError:
                        print(Mensagens.ERRO_POSICAO_INVALIDA)
                    else:
                        if not 0 < posicao <= len(treinador.equipa):
                            print(Mensagens.ERRO_POSICAO_INVALIDA)
                        else:
                            treinador.remover_da_equipa(posicao - 1)
            case 4:
                # Batalhar
                inimigo = input("Treinador: ")
                try:
                    winner = estadio.batalhar(treinador.nome, inimigo)
                except ValueError as e:
                    print(e)
                else:
                    if winner is None:
                        print(Mensagens.BATALHA_EMPATE)
                    else:
                        print(Mensagens.BATALHA_VITORIA.format(vencedor=winner.nome))
            case 0:
                return

def menu_de_gestao(pokedex, estadio):
    while True:
        match check(OPCOES_GESTAO, "Voltar"):
            case 1:
                # Listar treinadores
                filtro = input("Filtro: ")
                for t in estadio.treinadores:
                    if filtro in t.nome:
                        print(t)
            case 2:
                # Adicionar treinador
                nome = input("Nome: ")
                try:
                    estadio.adicionar_treinador(nome=nome)
                except ValueError as e:
                    print(e)
            case 3:
                # Carregar treinadores
                ficheiro = input("Ficheiro: ")
                try:
                    estadio.carregar_treinadores(ficheiro=ficheiro, pokedex=pokedex)
                except ValueError, FileNotFoundError:
                    print(Mensagens.ERRO_FICHEIRO_INVALIDO)
            case 4:
                # Gravar treinadores
                ficheiro = input("Ficheiro: ")
                try:
                    estadio.gravar_treinadores(ficheiro=ficheiro)
                except ValueError as e:
                    print(e)
            case 0:
                return

def menu_de_estatistica(estadio):
    while True:
        match check(OPCOES_ESTATISTICAS, "Voltar"):
            case 1:
                # Top 10
                if len(estadio.top10()) == 0:
                    print(Mensagens.ERRO_SEM_TREINADORES)
                else:
                    for t in estadio.top10():
                        print(t)
            case 2:
                # Média de vitórias
                try:
                    print(round(estadio.media_vitorias(),2))
                except ValueError as e:
                    print(e)
            case 3:
                # Equipa mais experiente
                try:
                    treinador = estadio.equipa_mais_experiente()
                    print(treinador)
                    for pokemon in treinador.equipa:
                        print(pokemon)
                except ValueError as e:
                    print(e)
            case 4:
                # Pokémon mais comum
                try:
                    print(estadio.pokemon_mais_comum())
                except ValueError as e:
                    print(e)
            case 5:
                # Distribuição de tipos
                try:
                    dist = estadio.distribuicao_tipos()
                    for tipo, perc in dist.items():
                        print(f"{tipo.capitalize()}: {perc*100:.1f}%")
                except ValueError as e:
                    print(e)
            case 0:
                return

# ---------------------------------------------------------------------------
# NÃO ALTERAR O CÓDIGO A PARTIR DAQUI
# Este bloco inicia o programa quando o ficheiro é executado diretamente, mas
# não quando é importado (por exemplo, pelos testes automáticos).
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    menu_principal()
