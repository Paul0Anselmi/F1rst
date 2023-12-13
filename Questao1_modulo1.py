#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Animal:
    def fazer_som(self):
        pass

class Gato(Animal):
    def fazer_som(self):
        return "Miau"

class Cachorro(Animal):
    def fazer_som(self):
        return "Auau"

class Historico:
    _instance = None
    historico = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Historico, cls).__new__(cls)
            cls._instance.historico = []
        return cls._instance

    def adicionar_execucao(self, animal):
        som = animal.fazer_som()
        opcao = '1' if isinstance(animal, Gato) else '2'
        self.historico.append(f"{opcao} {som}")

    def exibir_historico(self):
        return "\n".join(self.historico)


def main():
    historico = Historico()

    while True:
        opcao = input("Digite '1' para GATO, '2' para CACHORRO ou 'histórico' para exibir o histórico: ")

        if opcao == '1':
            gato = Gato()
            historico.adicionar_execucao(gato)
            print(f"Output: {gato.fazer_som()}")
        elif opcao == '2':
            cachorro = Cachorro()
            historico.adicionar_execucao(cachorro)
            print(f"Output: {cachorro.fazer_som()}")
        elif opcao.lower() == 'histórico':
            historico_output = historico.exibir_historico()
            print(f"Output: {historico_output}")
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()


# In[ ]:




