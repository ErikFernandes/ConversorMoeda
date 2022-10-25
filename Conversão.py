import PySimpleGUI as sg
import requests as rq

sg.theme('dark')

layout = [
    [sg.Text("Digite a sigla da moeda:                "), sg.Combo(values=["BRL", "USD", "EUR"],key="term", size=(8, 0))],
    [sg.Text("Qual valor você deseja converter?   "), sg.Input(key="valorConv", size=(8, 0))],
    [sg.Button("Pegar cotação", key="calcu"), sg.Button("Cancelar", key="cancel"),
     sg.Radio("Real", "mo", key="br", default=True), sg.Radio("Dolar", "mo", key="usa")],
    [sg.Text(justification='center', key="valorCota", expand_x=True)],
]

janela = sg.Window('',  layout)

def pegar_cotacao(codigo_moeda, tipo_moeda):
    try:
        requisicao = rq.get(f"https://economia.awesomeapi.com.br/last/{codigo_moeda}-{tipo_moeda}")
        requisicao_dic = requisicao.json()
        cotacao = requisicao_dic[f"{codigo_moeda}{tipo_moeda}"]["bid"]
        return cotacao

    except:
        return None

def Calcular():

    while True:

        evento, valores = janela.read()

        if evento == sg.WIN_CLOSED or evento == "cancel":
            break

        if evento == "calcu":

            term = valores["term"]
            term = term.upper()
            br = valores["br"]
            usa = valores["usa"]

            if usa == True and term == "USD":
                janela["valorCota"].update(f"Termos iguais")
                janela["valorConv"].update("")
                janela["term"].update("")
                Calcular()

            if br == True and term == "BRL":
                janela["valorCota"].update(f"Termos iguais")
                janela["valorConv"].update("")
                janela["term"].update("")
                Calcular()

            if usa == True:
                cotacao = pegar_cotacao(term, "USD")
                valorConv = valores["valorConv"]


                if valorConv == '':

                    if cotacao == None:
                        janela["valorCota"].update(f"Termo inválido")
                        janela["term"].update("")

                    else:
                        cotacao = float(cotacao)
                        janela["valorCota"].update(f"A cotação do {term} é $ {cotacao:.2f}")

                else:
                    try:
                        cotacao = float(cotacao)
                        valorConv = float(valorConv)
                        janela["valorCota"].update(f"O valor obtido é de $ {(valorConv * cotacao):.2f}")

                    except:
                        janela["valorCota"].update(f"Termo inválido")
                        janela["valorConv"].update("")
                        janela["term"].update("")

            if br == True:
                cotacao = pegar_cotacao(term, "BRL")
                valorConv = valores["valorConv"]

                if valorConv == '':

                    if cotacao == None:
                        janela["valorCota"].update(f"Termo inválido")
                        janela["term"].update("")

                    else:
                        cotacao = float(cotacao)
                        janela["valorCota"].update(f"A cotação do {term} é R$ {cotacao:.2f}")

                else:
                    try:
                        cotacao = float(cotacao)
                        valorConv = float(valorConv)
                        janela["valorCota"].update(f"O valor obtido é de R$ {(valorConv * cotacao):.2f}")

                    except:
                        janela["valorCota"].update(f"Termo inválido")
                        janela["valorConv"].update("")
                        janela["term"].update("")

            else:
                print('')
Calcular()