# Laboratorio: Introducción al cifrado, esteganografía y algoritmos resumen

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Herramientas necesarias: `openssl`, `sha512sum`, `git`, `steghide`, `docker`, `docker compose`.
- Repositorio GitHub de asignatura: puedes subir los programa desarrollados en el laboratorio.

## Esteganografía práctica

En este bloque ocultaremos un mensaje dentro de una imagen contenedora.

Si `steghide` no esta instalado:

```bash
sudo apt update
sudo apt install steghide -y
```

Preparar mensaje:

```bash
echo "SGSSI-26-27 Software is like sex: it's better when it's free" > msg_linus
```

Insertar mensaje con contraseña en imagen `linus.jpg`:

```bash
steghide embed -cf linus.jpg -ef msg_linus -sf linus_steg.jpg
```

Extraccion del mensaje oculto (Primero renombrar archivo original mensaje a `msg_linus_old`):

```bash
steghide extract -sf linus_steg.jpg
less msg_linus
```

Tamaño del contenedor:

```bash
ls -lh linus.jpg linus_steg.jpg
```

## Integridad con funciones hash

Cálculo de resúmenes:

```bash
echo "Este fichero verifica integridad" > integridad.txt
md5sum integridad.txt
sha256sum integridad.txt
```

Modifica un solo caracter y vuelve a calcular los resúmenes. ¿Cómo han cambiado?
Al modificar un solo carácter del fichero, tanto el resumen MD5 como el SHA-256 cambian completamente.

Antes de modificar el fichero:

* MD5: `68f8d19ba27a3d5f71fb69b0b4bb0b59`
* SHA-256: `d0272bfa04adeccadef82c488bb8d5b9d83944eefd086540c1840689e436b112`

Después de modificar el contenido:

* MD5: `0b9e494c93e50433c014e24c35f1e156`
* SHA-256: `4ced1d433f75b40147cc71a4249ef26c68506a3156c5f5db0d3ff08a935df3e7`

Aunque solo se ha añadido ` v2` al final del fichero, los dos valores hash han cambiado completamente. Esto se debe al efecto avalancha de las funciones hash: una pequeña modificación en los datos de entrada produce un resultado hash muy diferente.

Por tanto, los hashes permiten detectar modificaciones en un fichero, ya que si el contenido cambia, su resumen hash también cambia.


## Integridad y esteganografia

Compara los hashes de los mensajes usados en la esteganografía: 

```bash
sha256sum msg_linus
sha256sum msg_linus_old
```

¿Coinciden? 
Los hashes SHA-256 de `msg_linus` y `msg_linus_old` coinciden:

* `msg_linus`: `c3361d1a860a25ca4d2c721463a903ac22db903b381312dd1430df2e390a3439`
* `msg_linus_old`: `c3361d1a860a25ca4d2c721463a903ac22db903b381312dd1430df2e390a3439`

Por tanto, ambos ficheros tienen exactamente el mismo contenido. Esto confirma que el mensaje extraído mediante `steghide` es idéntico al mensaje original y que no se ha modificado durante el proceso de extracción.

Compara los hashes de los ficheros contenedor:

```bash
sha256sum linus.jpg
sha256sum linus_steg.jpg
```

¿Coinciden? 

Los hashes SHA-256 de los ficheros contenedor son diferentes:

* `linus.jpg`: `74d8d0047f89df9542723de8f3463371854ba46ff47d38c7bc034e1aee28b76f`
* `linus_steg.jpg`: `f0685353f2042e8548fdc4640635f6a6cdc853257ed642807e369211f6dff87b`

Por tanto, los hashes no coinciden. Esto indica que el fichero `linus_steg.jpg` ha sido modificado respecto al original. La modificación se debe a que `steghide` ha introducido el mensaje oculto dentro de la imagen.


Hay un mensaje importante de Buenaventura Durruti para vosotros en una de las imagenes del directorio `durruti`. El mensaje ha sido introducido mediante el programa steghide, con contraseña "durruti". La imagen que contiene el mensaje se corresponde con el Hash (SHA256) `7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb`.

### ¿Qué archivo es?

Se ha buscado el hash SHA-256 proporcionado entre todos los archivos del directorio `durruti` y sus subdirectorios mediante:

```bash
find . -type f -exec sha256sum {} \; | grep '7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb'
```

El resultado ha sido:

```text
7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb  ./imagen27.jpg
```

Por tanto, la imagen que contiene el mensaje oculto es **`imagen27.jpg`**.

### ¿Qué dice la frase?

Se ha extraído el mensaje utilizando `steghide` y la contraseña proporcionada:

```bash
steghide extract -sf ./imagen27.jpg
```

El contenido del fichero extraído `frase` es:

> "Al Fascismo no se le discute, se le destruye." Buenaventura Durruti

### ¿Cómo automatizar la búsqueda?

Si hubiese muchos archivos distribuidos en diferentes carpetas y subcarpetas, se podría automatizar la búsqueda utilizando `find` junto con `sha256sum`. Por ejemplo:

```bash
find . -type f -exec sha256sum {} \; | grep '7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb'
```

El comando recorre todos los archivos de forma recursiva, calcula su SHA-256 y filtra el resultado para localizar el hash buscado.

Una vez localizado el archivo, se puede extraer automáticamente el mensaje con:

```bash
steghide extract -sf ./imagen27.jpg -p "durruti"
```

De esta forma se puede localizar primero la imagen mediante su hash y posteriormente extraer el mensaje oculto utilizando `steghide`.


## Contraseñas y sal

Ejecuta:

```bash
echo -n "ContrasenaSegura" | sha256sum
echo -n "ContrasenaSegura" | sha256sum
```

Observa que el resultado es idéntico.

Uso de sal con OpenSSL:

```bash
openssl passwd -6 -salt SAL001 ContrasenaSegura
openssl passwd -6 -salt SAL002 ContrasenaSegura
```

¿Cambian los Hashes?
Sí, los hashes cambian.

Aunque se utiliza la misma contraseña (`ContrasenaSegura`), se utilizan dos sales diferentes:

```bash
openssl passwd -6 -salt SAL001 ContrasenaSegura
openssl passwd -6 -salt SAL002 ContrasenaSegura
```

Como resultado, se obtienen dos hashes diferentes.

Esto demuestra que la utilización de una **sal (salt)** hace que una misma contraseña produzca hashes distintos cuando se utilizan sales diferentes.

En la carpeta `password_hash_demo` tienes una pequeña aplicación web con tres versiones de la misma funcionalidad:

- `plain`: almacena la contraseña en texto plano.
- `hashed`: almacena un hash SHA-256 de la contraseña.
- `salted`: almacena unq sal aleatoria y un hash PBKDF2-HMAC-SHA256.

Para ejecutarla:

```bash
cd password_hash_demo
docker compose up --build
```

Después abre:

- http://localhost:5001/ -> versión insegura (texto plano)
- http://localhost:5002/ -> versión con hash
- http://localhost:5003/ -> versión con sal

Registra el mismo usuario y la misma contraseña en las tres versiones y compara la base de datos o la información mostrada por cada servicio. Fíjate en que:

- En texto plano se ve la contraseña original;
- Con hash, la misma contraseña produce el mismo valor hash para todos los usuarios;
- Con sal, cada usuario tiene una sal distinta, por lo que iguales contraseñas no generan el mismo valor almacenado.

Despliega el proyecto en tu servidor Google Cloud y comprueba que funciona correctamente, y que puedes cambiar la sal a un número definido por tí.

## Hashes y Git

Clona, si no lo has hecho ya, el repositorio de la asignatura (Usando SSH):

```bash
git clone git@github.com:mikel-egana-aranguren/EHU-SGSSI-01.git
cd cd EHU-SGSSI-01/
git log
```

¿Qué identifica el hash del commit?¿Por qué Git detecta cambios de contenido de forma eficiente?


