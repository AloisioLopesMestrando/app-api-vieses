# Perguntas de vieses (Likert 1-5).
# IMPORTANTE: a questão "27" do seu instrumento é invertida.
# Aqui marcamos reverse=True para ela.

PERGUNTAS_VIESES = [
    # Excesso de confiança (4)
    {"id": "v14", "vies": "Excesso de Confiança", "texto": "Eu sei qual ação tomar para aumentar o valor do meu investimento.", "reverse": False},
    {"id": "v15", "vies": "Excesso de Confiança", "texto": "Eu me considero um investidor inteligente no mercado financeiro.", "reverse": False},
    {"id": "v16", "vies": "Excesso de Confiança", "texto": "Eu estou sempre confiante de que vou ganhar quando invisto no mercado financeiro.", "reverse": False},
    {"id": "v17", "vies": "Excesso de Confiança", "texto": "Eu consigo escolher ativos para investir com taxas de retorno mais altas do que as taxas médias do mercado.", "reverse": False},

    # Ancoragem (3)
    {"id": "v18", "vies": "Ancoragem", "texto": "Eu confio nos retornos alcançados anteriormente nos meus investimentos como referência para estimar retornos futuros.", "reverse": False},
    {"id": "v19", "vies": "Ancoragem", "texto": "Eu confio nas minhas experiências passadas no mercado financeiro para fazer meus investimentos futuros.", "reverse": False},
    {"id": "v20", "vies": "Ancoragem", "texto": "Eu estimo mudanças futuras na minha rentabilidade com base na rentabilidade recente dos meus investimentos.", "reverse": False},

    # Aversão à perda (7) — última invertida
    {"id": "v21", "vies": "Aversão à Perda", "texto": "Ao tomar uma decisão, penso muito mais no que posso perder do que no que posso ganhar.", "reverse": False},
    {"id": "v22", "vies": "Aversão à Perda", "texto": "A dor de perder dinheiro importa mais para mim do que o prazer de ganhar a mesma quantia.", "reverse": False},
    {"id": "v23", "vies": "Aversão à Perda", "texto": "Sinto-me nervoso(a) quando preciso tomar uma decisão que pode levar a uma perda.", "reverse": False},
    {"id": "v24", "vies": "Aversão à Perda", "texto": "A dor de perder algo importa muito mais para mim do que o prazer de o conquistar.", "reverse": False},
    {"id": "v25", "vies": "Aversão à Perda", "texto": "Vivenciar uma grande perda permanece mais tempo na minha mente do que vivenciar um grande ganho.", "reverse": False},
    {"id": "v26", "vies": "Aversão à Perda", "texto": "Um possível fracasso me assusta mais do que um possível sucesso me encoraja.", "reverse": False},
    {"id": "v27", "vies": "Aversão à Perda", "texto": "O sofrimento causado por perdas pode ser totalmente compensado pelo prazer dos ganhos.", "reverse": True},

    # Status quo (3)
    {"id": "v28", "vies": "Status Quo", "texto": "Eu prefiro fazer o mesmo investimento repetidamente se ele me deu bons retornos no mês ou ano passado.", "reverse": False},
    {"id": "v29", "vies": "Status Quo", "texto": "Eu prefiro manter um investimento mesmo quando outro com perspectivas semelhantes também está disponível.", "reverse": False},
    {"id": "v30", "vies": "Status Quo", "texto": "Acredito que o mercado de investimentos está sempre sob ameaça e mudar de produto pode ser muito arriscado.", "reverse": False},

    # Ilusão de controle (5)
    {"id": "v31", "vies": "Ilusão de Controle", "texto": "Em comparação às pessoas com quem trabalho e convivo, minhas habilidades estão acima da média.", "reverse": False},
    {"id": "v32", "vies": "Ilusão de Controle", "texto": "Mesmo com informações incertas do ambiente externo, mantenho o controle da situação ao investir.", "reverse": False},
    {"id": "v33", "vies": "Ilusão de Controle", "texto": "É pouco provável que uma situação disruptiva afete expressivamente o mercado onde invisto.", "reverse": False},
    {"id": "v34", "vies": "Ilusão de Controle", "texto": "Minhas decisões são mais acertadas que a média em meus investimentos.", "reverse": False},
    {"id": "v35", "vies": "Ilusão de Controle", "texto": "Não percebo riscos de mudanças bruscas afetarem meus investimentos no curto e médio prazo.", "reverse": False},

    # Autocontrole (4)
    {"id": "v36", "vies": "Autocontrole", "texto": "Consigo seguir metas financeiras de longo prazo.", "reverse": False},
    {"id": "v37", "vies": "Autocontrole", "texto": "Considero cuidadosamente as consequências das minhas decisões de compra antes de gastar.", "reverse": False},
    {"id": "v38", "vies": "Autocontrole", "texto": "Consigo resistir a tentações para alcançar meus objetivos orçamentários.", "reverse": False},
    {"id": "v39", "vies": "Autocontrole", "texto": "Eu sei quando “dizer chega” em relação aos meus gastos.", "reverse": False},
]

