


def nombres_propios(batch: list) -> list:
    "Devuelve un listado de todas las palabras que comienzan con mayúsculas"
    result = []
    
    for parrafo in batch:
        muestras = [palabra for palabra in parrafo.split(" ") if palabra.istitle()]
        result.append(muestras)
    return result




if __name__ == "__main__":
    texto = 'José Jose joseeee Patricia Bullrich PATRICIA BULLRICH patricia bullrich Este es otro ejemplo de tokenizadorrrrr tokenizador basado en palabras Conclusión Conclusion conclusion conclusión'
    batch = [texto, "ejemplo número 2 Hola", "una lista vacia"]
            
    print("nombres propios")
    print(nombres_propios(batch))
    
    # OUTPUT: [['José', 'Jose', 'Patricia', 'Bullrich', 'Este', 'Conclusión', 'Conclusion'], ['Hola'], []]
    # OK