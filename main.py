import ollama
import subprocess
import webbrowser
import os

def buscar_en_youtube(busqueda):
    try:
        comando = f'yt-dlp "ytsearch1:{busqueda}" --get-title --get-id'
        resultado = subprocess.check_output(comando, shell=True).decode("utf-8").strip().split("\n")
        if len(resultado) >= 2:
            return resultado[0], f"https://www.youtube.com/watch?v={resultado[1]}"
        return None, None
    except: return None, None

def chat():
    print("\n🚀 ASISTENTE TOTAL (v3 - Modo Forzado)")
    print("---------------------------------------")
    
    while True:
        msg = input("\nTú: ")
        if msg.lower() in ['salir', 'exit']: break
        
        prompt_final = msg
        contexto_sistema = "Eres un asistente de IA que tiene acceso a los archivos del usuario porque el sistema te los proporciona directamente."

        # --- DETECTAR ARCHIVOS .TXT ---
        for palabra in msg.split():
            if palabra.endswith(".txt") and os.path.exists(palabra):
                with open(palabra, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                print(f"📖 Leyendo {palabra}...")
                # Aquí forzamos a la IA a aceptar el contenido
                prompt_final = f"SISTEMA: El contenido del archivo '{palabra}' es el siguiente:\n\n{contenido}\n\nUSUARIO PREGUNTA: {msg}"
                break

        # --- DETECTAR YOUTUBE ---
        if "youtube" in msg.lower():
            termino = msg.lower().replace("busca en youtube", "").replace("youtube", "").strip()
            print(f"🔍 Buscando '{termino}'...")
            titulo, url = buscar_en_youtube(termino)
            if url:
                webbrowser.open(url)
                prompt_final = f"SISTEMA: Se abrió el video '{titulo}' en el navegador. Confírmale al usuario."

        try:
            # Usamos 'system' para decirle quién es y qué puede hacer
            response = ollama.chat(model='llama3', messages=[
                {'role': 'system', 'content': contexto_sistema},
                {'role': 'user', 'content': prompt_final},
            ], stream=True)
            
            print("AI: ", end='', flush=True)
            for chunk in response:
                print(chunk['message']['content'], end='', flush=True)
            print()
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    chat()
