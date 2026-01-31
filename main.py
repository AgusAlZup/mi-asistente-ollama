import ollama
import subprocess
import webbrowser
import os
import json

# Nombre del archivo de memoria
ARCHIVO_MEMORIA = "memoria_ia.json"

def guardar_memoria(historial):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)
    print("\n💾 Memoria guardada con éxito.")

def cargar_memoria():
    if os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return [{'role': 'system', 'content': 'Eres un asistente de terminal Linux breve y con memoria.'}]

def buscar_en_youtube(busqueda):
    if not busqueda: return None, None
    try:
        comando = ['yt-dlp', f'ytsearch1:{busqueda}', '--get-title', '--get-id']
        resultado = subprocess.check_output(comando, stderr=subprocess.STDOUT).decode("utf-8").strip().split("\n")
        if len(resultado) >= 2:
            return resultado[0], f"https://www.youtube.com/watch?v={resultado[1]}"
        return None, None
    except: return None, None

def chat():
    print("\n🚀 ASISTENTE CON MEMORIA PERSISTENTE")
    print("------------------------------------")
    
    historial = cargar_memoria()
    if len(historial) > 1:
        print("🧠 He recuperado recuerdos de nuestra última charla.")
    
    while True:
        try:
            msg = input("\nTú: ")
        except KeyboardInterrupt:
            msg = "salir"

        if msg.lower() in ['salir', 'exit', 'chau', 'limpiar']:
            if msg.lower() == 'limpiar':
                historial = [historial[0]]
                if os.path.exists(ARCHIVO_MEMORIA): os.remove(ARCHIVO_MEMORIA)
                print("🧠 Memoria borrada.")
                continue
            
            # Preguntar antes de salir
            confirmar = input("\n¿Querés que guarde esta charla para la próxima? (s/n): ")
            if confirmar.lower() == 's':
                guardar_memoria(historial)
            else:
                print("🗑️ Memoria de esta sesión descartada.")
            break
        
        texto_usuario = msg

        for palabra in msg.split():
            if palabra.lower().endswith(".txt") and os.path.exists(palabra):
                with open(palabra, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                print(f"📖 Leyendo {palabra}...")
                texto_usuario = f"ARCHIVO '{palabra}':\n{contenido}\n\nPREGUNTA: {msg}"
                break

        if "youtube" in msg.lower():
            termino = msg.lower().replace("busca en youtube", "").replace("youtube", "").strip()
            if termino:
                print(f"🔍 Buscando '{termino}'...")
                titulo, url = buscar_en_youtube(termino)
                if url:
                    webbrowser.open(url)
                    texto_usuario = f"SISTEMA: Video '{titulo}' abierto. Confirma brevemente."

        historial.append({'role': 'user', 'content': texto_usuario})

        try:
            response = ollama.chat(model='llama3', messages=historial, stream=True)
            print("AI: ", end='', flush=True)
            respuesta_completa = ""
            try:
                for chunk in response:
                    txt = chunk['message']['content']
                    print(txt, end='', flush=True)
                    respuesta_completa += txt
            except KeyboardInterrupt:
                print("\n[Interrumpido]")
            
            historial.append({'role': 'assistant', 'content': respuesta_completa})
            print()
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    chat()
