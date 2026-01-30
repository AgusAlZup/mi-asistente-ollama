import ollama

def chat():
    print("\n🟢 ASISTENTE LOCAL ACTIVO")
    print("--------------------------")
    print("Escribe 'salir' para finalizar.\n")
    
    while True:
        msg = input("Tú: ")
        if msg.lower() in ['salir', 'exit']:
            print("👋 ¡Nos vemos!")
            break
        
        try:
            # Usamos llama3. Si tienes otro modelo (ej. phi3), cámbialo aquí
            response = ollama.generate(model='llama3', prompt=msg, stream=True)
            print("AI: ", end='', flush=True)
            for chunk in response:
                print(chunk['response'], end='', flush=True)
            print("\n")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    chat()
