def clean_facebook_comments(batch: list) -> list:
    new_batch = []
    for comment in batch:
        
        # Filtro 1
        if comment in ["Me gusta", "Responder", "Editado", "Fan destacado"] or comment.isnumeric():
            continue
        
        
        comment = comment.split(" ")
        
        # Filtro 2: registros que tienen patrón "# h" excluídos
        if len(comment)==2 and comment[1] in ['h', "min", "d", "sem", "respuesta", "respuestas"]:
            continue


        # Filtro 3: eliminar autores
        # filter_3 = [False if word.istitle() else True for word in comment]
        filter_3 = [not word.istitle() for word in comment]
        


        if any(filter_3):
            new_batch.append(" ".join(comment))

    return new_batch