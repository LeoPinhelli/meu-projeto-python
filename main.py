import sys

# "Banco de dados" simples em memória
historico = []


def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ValueError("Não é possível dividir por zero")
    return a / b


def registrar_operacao(op, a, b, resultado):
    historico.append({
        "operacao": op,
        "a": a,
        "b": b,
        "resultado": resultado
    })


def seed():
    print("🌱 Populando histórico com dados iniciais...")
    registrar_operacao("soma", 2, 3, somar(2, 3))
    registrar_operacao("subtracao", 5, 2, subtrair(5, 2))
    registrar_operacao("multiplicacao", 3, 4, multiplicar(3, 4))
    registrar_operacao("divisao", 10, 2, dividir(10, 2))
    print("✅ Seed concluído!")


def listar():
    print("📋 Histórico de operações:")
    if not historico:
        print("Nenhuma operação registrada.")
        return

    for i, op in enumerate(historico, start=1):
        print(f"{i}. {op['operacao']} ({op['a']}, {op['b']}) = {op['resultado']}")


def estatisticas():
    print("📊 Estatísticas:")
    if not historico:
        print("Sem dados.")
        return

    total = len(historico)
    soma_resultados = sum(op["resultado"] for op in historico)

    print(f"Total de operações: {total}")
    print(f"Soma dos resultados: {soma_resultados}")
    print(f"Média dos resultados: {soma_resultados / total:.2f}")


def calcular(op, a, b):
    a = float(a)
    b = float(b)

    if op == "soma":
        resultado = somar(a, b)
    elif op == "sub":
        resultado = subtrair(a, b)
    elif op == "mult":
        resultado = multiplicar(a, b)
    elif op == "div":
        resultado = dividir(a, b)
    else:
        print("Operação inválida")
        return

    registrar_operacao(op, a, b, resultado)
    print(f"Resultado: {resultado}")


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print(" python main.py seed")
        print(" python main.py list")
        print(" python main.py stats")
        print(" python main.py soma 2 3")
        return

    comando = sys.argv[1]

    if comando == "seed":
        seed()
    elif comando == "list":
        listar()
    elif comando == "stats":
        estatisticas()
    elif comando in ["soma", "sub", "mult", "div"]:
        if len(sys.argv) != 4:
            print("Uso: python main.py soma 2 3")
            return
        calcular(comando, sys.argv[2], sys.argv[3])
    else:
        print("Comando inválido")


if __name__ == "__main__":
    main()