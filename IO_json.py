#-----ultimas modificaciones
#al llamar la función download se debe especificar el nombre del archivo con todo y extensión e.g. linea.json, mapa.geojson

import urllib.request, json 
#!pip install PyGithub
# from github import Github
# from github_contents import GithubContents

#raiz de la ruta para encontrar el contenido de los JSON
#link = "https://raw.githubusercontent.com/Grimaldo095/pruebas/main/"
# link = "https://raw.githubusercontent.com/GIL-UNAM/Miopers/master/"

#descargar json y guardarlo en un diccionario
def download_json(ruta):
    """Recibe la ruta del json en el repo. Regresa un diccionario con toda la info del json."""
    link_completo = link + ruta 
    with urllib.request.urlopen(link_completo) as url:
        data = json.loads(url.read().decode())
        return data

#token cuenta Grimaldo
token = "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"

ruta_repo = "GIL-UNAM/Miopers"
# acceder a mi cuenta de Github usando un access token
# g = Github(token)

#acceder al repo donde están los JSON
# repo = g.get_repo(ruta_repo)

#name="prueba.json"
def upload_json(ruta, dicc):
    """Se convierte el diccionario en un string con formato json y se sube al archivo especificado (dentro del repositorio)"""
    
    #acceder a un archivo dentro del repo, de este objeto podemos extraer la ruta, el sha, el contenido, etc.
    file = repo.get_contents(ruta)
    #convertir diccionario en string con formato json
    info = json.dumps(dicc)
    #editar archivo en el repo
    repo.update_file(file.path, message="Actualizar JSON", content=info, sha=file.sha)
    
#para documentos que pesan más de 1GB
# github = GithubContents(
#     "GIL-UNAM",
#     "Miopers",
#     token = "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",
#     branch="master"	
# )

# nombre = "Luis Grimaldo"
# email = "grimaldo.lae@gmail.com"

# def upload_heavy(ruta, diccionario, message):
#     content_sha, commit_sha = github.write(
#         filepath=ruta,
#         content_bytes=bytes(json.dumps(diccionario), 'utf-8'), #convertirlo a bytestring si no funciona
#         #sha=previous_sha, # Optional
#         # commit_message=message,
#         committer={
#             "name": nombre,
#             "email": email,
#         },
#     )

def ordenar(dicc):
  """Ordena las entradas del diccionario por orden cronologico y elimina repetidos """
  data = dicc['data']
  data.sort(key=lambda k:k['day'])
  #eliminar fechas repetidas
  aux = []
  data_procesado = []
  for tweet in data:
    fecha = tweet['day']
    if fecha not in aux:
      aux.append(fecha)
      data_procesado.append(tweet)
  dicc['data'] = data_procesado
  return dicc
