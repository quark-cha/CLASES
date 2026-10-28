# Herramientas de CLASES

Autor: Víctor Estrada Díaz. Código HL3; condiciones en https://estradad.es/licencia.php.
Python 3.10 o posterior. Solo biblioteca estándar; no requiere descargas ni acceso a red.

Desde la raíz del proyecto:

```powershell
python src/fuentes.py listar
python src/fuentes.py sincronizar
python src/fuentes.py verificar
python src/ramanujan.py --terminos 3 --precision 80
python -m unittest discover -s tests -v
```

`fuentes.py` lee únicamente los españoles actuales de `../UNIHOLOG` indicados en
`fuentes.json`. Copia sus bytes íntegros a `documentos/UNIHOLOG`, registra SHA-256
y las líneas donde aparecen clases, y no modifica ni mueve los originales.
Una copia local editada bloquea la actualización para impedir sustituciones
descontroladas. Ejecutarlo de nuevo sin cambios no reescribe archivos.

`verificar` compara también el origen cuando está disponible. En un clon aislado
de GitHub comprueba la integridad de las copias mediante el manifiesto incluido.
`--origen RUTA` permite indicar otra ubicación actual del proyecto UNIHOLOG.

`ramanujan.py` calcula sumas racionales exactas, comprueba las identidades
algebraicas del artículo y la invariancia de los productos `ab` y `ac` bajo
`(a,b,c) → (λa,b/λ,c/λ)`. La aproximación decimal a π procede de la suma truncada;
el número de dígitos de trabajo no es una certificación de exactitud de todos ellos.
No demuestra las evaluaciones elípticas de partida ni relaciones físicas nuevas.


## Empaquetado y página del proyecto

`empaquetado.py` prepara `zenodo/CLASES.zip` desde el commit local actual.
Requiere Git instalado, además de Python. No consulta remotos ni accede a Zenodo.
Incluye el proyecto registrado y un manifiesto con commit y SHA-256. Rechaza
cambios locales sin registrar, enlaces y submódulos para no sustituir fuentes
actuales por una copia anterior ni incorporar rutas externas.

```powershell
python publica.py --solo-zip
python publica.py --preparar-web
python publica.py --web
```

`--preparar-web` crea `pdfs/proyecto.html`, la portada y la copia web del mismo ZIP.
La copia en `pdfs/` y la de `zenodo/` son idénticas y atienden a dos destinos;
no son versiones distintas. Solo `--web` ejecuta FTP mediante PUBLICAR y verifica
los archivos remotos. Un fallo de generación impide continuar con la subida.
