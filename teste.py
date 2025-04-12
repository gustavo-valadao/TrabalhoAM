from datetime import datetime

def pedir_nome():
    while True:
        try:
            userName = input("Antes de iniciar, digite o seu nome: ").strip()

            if not userName:
                raise ValueError("O nome não pode estar vazio.")
            if any(char.isdigit() for char in userName):
                raise ValueError("O nome não deve conter números.")
            if len(userName) > 20:
                raise ValueError("O nome deve ter no máximo 20 caracteres.")

            confirmar = input(f"Você digitou '{userName}'. Está correto? (s/n): ").strip().lower()

            if confirmar == "s":
                return userName  
            elif confirmar == "n":
                print("Ok, vamos tentar de novo.\n")
            else:
                print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.\n")

        except ValueError as e:
            print(f"Erro: {e}\n")



def registrar_log(mensagem):
    datahora = datetime.now().strftime("%d/%m/%y  %H:%M:%S")
    log = f"[{datahora}] {userName}: {mensagem}\n"
    

    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(log)




userName = pedir_nome()  

registrar_log("Programa iniciado")  

print(f"\nOlá, {userName}! Vamos começar.")
