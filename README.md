# CLASES

Investigación de Víctor Estrada Díaz sobre clases, transformaciones e invariantes, basada en UNIHOLOG. Textos CC BY-NC-SA 4.0; código HL3.

Proyecto de Víctor Estrada Díaz, basado en las clases de UNIHOLOG, para estudiar transformaciones, invariantes y relaciones entre constantes.

## Artículo inicial

[Ramanujan, π y la estructura que relaciona las constantes](ES_01_Ramanujan_y_las_constantes.md).

Artículo de Víctor Estrada Díaz preparado para CLASES. Fórmulas en LaTeX, con `$...$` en línea y `$$...$$` en bloque para su representación en Markdown. Se conservan el contenido, las referencias y la licencia del autor. Su incorporación al proyecto no constituye una revisión científica nueva.

## Publicación

El proyecto utiliza el sistema compartido PUBLICAR/PackPublica. Desde esta carpeta:

```text
python publica.py
```

Genera los derivados locales y el catálogo. Para subirlos a la web del autor mediante la configuración existente de PUBLICAR:

```text
python publica.py --web
```

Destino configurado: /estradad.es/teorias/pdf/CLASES. La creación del proyecto no implica que ya esté publicado.

Los artículos usan nombres ES_01_…, ES_02_…; las traducciones conservan el número y cambian el prefijo de idioma. Este README se excluye de la publicación.

## Desarrollo previsto

Precisar las clases de UNIHOLOG que se estudiarán, sus elementos y operaciones; definir las transformaciones admisibles y los invariantes; comprobar qué relaciones pueden deducirse sin introducir de antemano las constantes buscadas.

## Procedencia

Artículo inicial conservado en el proyecto local CLASES desde el 25 de octubre de 2026.
La procedencia y las huellas de las fuentes de UNIHOLOG están documentadas en su manifiesto.


## Fuentes actuales recuperadas de UNIHOLOG

[Índice y procedencia de los documentos](FUENTES_UNIHOLOG.md).
Las copias de consulta están en `documentos/UNIHOLOG`. Se conservan íntegros
los españoles actuales y sus originales permanecen en el proyecto vecino.
ES_49, ES_50 y ES_51 desarrollan las clases; ES_46_RV6 aporta contexto sobre
clases de onda y transporte. Se excluye el total para no duplicar sus documentos.

## Herramientas en src

[Uso y alcance de las herramientas](src/README.md).

```powershell
python src/fuentes.py verificar
python src/ramanujan.py --terminos 3 --precision 80
python -m unittest discover -s tests -v
```

La sincronización con `python src/fuentes.py sincronizar` compara huellas y
conserva el origen. No toma material de archivos históricos ni sobrescribe
una copia local modificada sin resolver la discrepancia.

## Portada

![CLASES: exploración de un mundo matemático y montañas fractales](img/CLASES_mundo_matematico.png)

Concepto visual: Víctor Estrada Díaz. Portada generada por IA a partir de ese concepto.

## Licencias

[Autoría, licencias y condiciones de uso](LICENCIAS.md).


## Archivo completo para Zenodo y publicación web

`publica.py` prepara un único archivo `zenodo/CLASES.zip` con la versión
registrada del proyecto: código, documentos, portada, pruebas e instrucciones.
Dentro del ZIP, `CLASES/VERSION_ARCHIVO.json` identifica el commit exacto y
las huellas de todos sus archivos. El paquete conserva las licencias y la autoría.

Se excluyen `.git`, credenciales, cachés, temporales, logs y respaldos antiguos.
La carpeta `zenodo/` tampoco se introduce dentro de su propio archivo. Solo hay
un ZIP actual: una versión nueva sustituye el anterior; una versión idéntica no
reescribe el archivo. Si hay cambios sin registrar, el programa se detiene para
no archivar una copia anterior como si fuera la actual. El programa no hace
commits automáticamente.

```powershell
# Solo ZIP local: sin conversores, FTP ni llamadas a Zenodo
python publica.py --solo-zip

# ZIP y página local, sin convertir documentos ni subir archivos
python publica.py --preparar-web

# Generación local de documentos, ZIP y página del proyecto
python publica.py

# Generar y publicar el proyecto en la web del autor
python publica.py --web
```

Con `--web`, PUBLICAR verifica la copia remota del ZIP, la página del proyecto,
el catálogo de artículos, la portada y las fuentes de UNIHOLOG. La página
`proyecto.html` enlaza el ZIP, GitHub y los artículos. El catálogo `index.php`
incluye un acceso visible al proyecto y a la descarga completa.
Destino configurado: `https://estradad.es/teorias/pdf/CLASES/`.
Una generación fallida detiene la subida para evitar publicar derivados antiguos.

**Zenodo:** este cambio prepara el ZIP; no crea depósitos, no reserva DOI y no
publica automáticamente en Zenodo. El archivo que se entregue allí será
únicamente `CLASES.zip`, con todos los metadatos de versión dentro de él.
