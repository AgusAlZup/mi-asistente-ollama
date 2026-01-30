import ollama
import os

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer el archivo: {e}"

def chat():
    print("\n🟢 ASISTENTE CON LECTURA DE ARCHIVOS")
    print("-----------------------------------")
    print("Escribe 'leer:nombre.txt' para que analice un archivo.")
    print("Escribe 'salir' para finalizar.\n")
    
    while True:
        msg = input("Tú: ")
        if msg.lower() in ['salir', 'exit']:
            break
        
        # Superpoder: Si el mensaje empieza con 'leer:', busca el archivo
        if msg.startswith("leer:"):
            archivo = msg.split(":")[1].strip()
            contenido = leer_archivo(archivo)
            prompt_final = f"Contexto del archivo {archivo}:\n{contenido}\n\nPregunta: Por favor, resume o analiza este contenido."
            print(f"📖 Leyendo {archivo}...")
        else:
            prompt_final = msg

        try:
            response = ollama.generate(model='llama3', prompt=prompt_final, stream=True)
            print("AI: ", end='', flush=True)
            for chunk in response:
                print(chunk['response'], end='', flush=True)
            print("\n")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    chat()
