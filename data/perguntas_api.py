# Perguntas da Análise de Perfil do Investidor (API)
# Cada pergunta tem opções com código (A/B/C/D), descrição e pontos conforme sua tabela.

PERGUNTAS_API = [
    {
        "texto": "Qual o seu principal objetivo com este investimento?",
        "opcoes": [
            {"codigo": "A", "descricao": "Quero preservar o meu dinheiro sem correr riscos e não aceito perdas.", "pontos": 1},
            {"codigo": "B", "descricao": "Quero ganhar mais dinheiro, assumindo riscos moderados, aceito pequenas perdas.", "pontos": 15},
            {"codigo": "C", "descricao": "Quero ganhar muito dinheiro, não me importo em assumir riscos elevados.", "pontos": 25},
        ],
    },
    {
        "texto": "Você já investiu em Poupança, Tesouro Direto, CDB, Fundos de Investimento Renda Fixa, LCA ou LCI?",
        "opcoes": [
            {"codigo": "A", "descricao": "Sim", "pontos": 1},
            {"codigo": "B", "descricao": "Não", "pontos": 0},
        ],
    },
    {
        "texto": "Você já investiu em Fundos de Investimento Multimercado, Inflação ou Cambial ou COE?",
        "opcoes": [
            {"codigo": "A", "descricao": "Sim", "pontos": 3},
            {"codigo": "B", "descricao": "Não", "pontos": 0},
        ],
    },
    {
        "texto": "Você já investiu em Ações, Fundos de Ações ou Debêntures?",
        "opcoes": [
            {"codigo": "A", "descricao": "Sim", "pontos": 5},
            {"codigo": "B", "descricao": "Não", "pontos": 0},
        ],
    },
    {
        "texto": "Você já investiu em Termos, Opções e Futuros?",
        "opcoes": [
            {"codigo": "A", "descricao": "Sim", "pontos": 7},
            {"codigo": "B", "descricao": "Não", "pontos": 0},
        ],
    },
    {
        "texto": "Por quanto tempo pretende deixar o seu dinheiro investido?",
        "opcoes": [
            {"codigo": "A", "descricao": "Até 6 meses", "pontos": 0},
            {"codigo": "B", "descricao": "6 meses a 1 ano", "pontos": 1},
            {"codigo": "C", "descricao": "1 ano a 3 anos", "pontos": 2},
            {"codigo": "D", "descricao": "Mais de 3 anos", "pontos": 3},
        ],
    },
    {
        "texto": "Em relação ao seu conhecimento e experiência com investimentos, é possível afirmar que:",
        "opcoes": [
            {"codigo": "A", "descricao": "Não possuo formação relacionada ao mercado financeiro ou experiência no mercado financeiro.", "pontos": 1},
            {"codigo": "B", "descricao": "Minha formação está consideravelmente relacionada ao mercado financeiro ou possuo alguma experiência, mas às vezes preciso de orientação.", "pontos": 5},
            {"codigo": "C", "descricao": "Minha formação está diretamente relacionada ao mercado financeiro ou tenho vasta experiência e me sinto seguro(a) ao investir sem orientação.", "pontos": 10},
        ],
    },
    {
        "texto": "Considerando sua necessidade de liquidez, em relação aos recursos que está investindo, assinale a opção que melhor define sua necessidade:",
        "opcoes": [
            {"codigo": "A", "descricao": "Quero ter a totalidade dos recursos disponíveis para resgate imediato.", "pontos": 0},
            {"codigo": "B", "descricao": "Quero ter disponível para resgate imediato 50% do recurso investido.", "pontos": 3},
            {"codigo": "C", "descricao": "Quero ter disponível para resgate imediato 25% do recurso investido.", "pontos": 5},
        ],
    },
]


