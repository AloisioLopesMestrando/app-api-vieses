def classificar_perfil(perguntas_api, respostas_api):
    score = 0
    for i, q in enumerate(perguntas_api):
        codigo = respostas_api[i]
        pontos = 0
        for op in q["opcoes"]:
            if op["codigo"] == codigo:
                pontos = op["pontos"]
                break
        score += pontos

    if score <= 19:
        perfil = "Conservador"
    elif 20 <= score <= 43:
        perfil = "Moderado"
    else:
        perfil = "Arrojado"

    return perfil, score


def calcular_media_vieses(perguntas_vieses, respostas_vieses):
    acum = {}
    cont = {}

    for item in perguntas_vieses:
        qid = item["id"]
        vies = item["vies"]
        reverse = item.get("reverse", False)

        if qid not in respostas_vieses:
            continue

        val = int(respostas_vieses[qid])

        if vies == "Autocontrole":
            val = 6 - val  # Mede a presença da falta de autocontrole.
        elif reverse:
            val = 6 - val  # 1<->5, 2<->4, 3->3

        acum[vies] = acum.get(vies, 0) + val
        cont[vies] = cont.get(vies, 0) + 1

    return {v: (acum[v] / cont[v]) for v in acum.keys() if cont.get(v, 0) > 0}


def top_vieses(medias, top_n=3):
    return sorted(medias.items(), key=lambda x: x[1], reverse=True)[:top_n]

