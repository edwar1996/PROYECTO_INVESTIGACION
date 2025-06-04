import yagmail

# Autenticación
remitente = "3158209195santi@gmail.com"
contraseña = "AQUÍ_VA_LA_CONTRASEÑA_DE_LA_CUENTA"  # Usa una contraseña de aplicación si tienes verificación en 2 pasos

# Crear conexión
yag = yagmail.SMTP(user=remitente, password=contraseña)

# Enviar el correo
destinatario = "alejomartinez@gmail.com"
asunto = "Correo de prueba desde Python"
cuerpo = "Hola Alejo,\n\nEste es un mensaje de prueba enviado desde Python usando yagmail.\n\nSaludos."

yag.send(to=destinatario, subject=asunto, contents=cuerpo)

print("Correo enviado con éxito.")
