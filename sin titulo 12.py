import openai 

# Configura tu clave de API
openai.api_key = "TU_CLAVE_DE_API"

print("¡Hola! Soy un chatbot inteligente. ¿De qué te gustaría hablar?")
while True:
    user_input = input("Tú: ")
    if user_input.lower() in ["salir", "adiós", "exit"]:
        print("Chatbot: ¡Adiós! Fue un placer hablar contigo. 😊")
        break

    # Enviar la consulta a ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=150
    )
    print("Chatbot:", response.choices[0].text.strip())
