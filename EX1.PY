# IDENTIFICAÇÃO DO ESTUDANTE    
# Numero :40240120
# Ñome:Dinis Miranda


import random

def analisarLista(lista):
    return [num for num in lista if num % 5 == 0 or num % 10 == 0]

def main():
    numeros_gerados = []
    numero_atual = random.randint(1, 100)
    numeros_gerados.append(numero_atual)

    print(f"Número gerado: {numero_atual}")

    while numero_atual != 100:
        resposta = input("Deseja gerar novo número (S/N)? ").strip().upper()
        if resposta == 'N':
            break
        elif resposta == 'S':
            numero_atual = random.randint(numero_atual + 1, 100)
            if numero_atual not in numeros_gerados:
                numeros_gerados.append(numero_atual)
                print(f"Número gerado: {numero_atual}")
            else:
                print("Número repetido! Gerando novamente...")
        else:
            print("Resposta inválida. Escreva 'S' para Sim ou 'N' para Não.")

    print("\nPrograma terminado.")
    print("Lista dos números de forma decrescente:", sorted(numeros_gerados, reverse=True))

    numeros_divisiveis = analisarLista(numeros_gerados)
    print("Números divisíveis por 5 ou 10:", numeros_divisiveis)

if __name__ == "__main__":
    main()
