import ollama
import subprocess

def buscar_en_youtube(busqueda):
    try:
        # Esto busca el video y nos devuelve el título y la URL
        comando = f'yt-dlp "ytsearch1:{busqueda}" --get-title --get-id'
        resultado = subprocess.check_output(comando, shell=True).decode("utf-8").strip().split("\n")
        titulo = resultado[0]
        video_id = resultado[1]
        url = f"https://www.youtube.com/watch?v={video_id}"
        return f"Encontré: {titulo}\nEnlace: {url}"
    except:
        return "No pude encontrar nada en YouTube."

def chat():
    print("\n🔴 ASISTENTE MULTIMEDIA")
    print("Dime: 'busca en youtube musica lo-fi' o similares.")
    
    while True:
        msg = input("Tú: ").lower()
        if msg in ['salir', 'exit']: break
        
        if "youtube" in msg:
            termino = msg.replace("busca en youtube", "").replace("youtube", "").strip()
            print(f"🔍 Buscando '{termino}' en YouTube...")
            info_video = buscar_en_youtube(termino)
            prompt_final = f"El usuario buscó en YouTube y encontré esto: {info_video}. Por favor, responde de forma amable y ofrece el link."
        else:
            prompt_final = msg

        response = ollama.generate(model='llama3', prompt=prompt_final, stream=True)
        print("AI: ", end='', flush=True)
        for chunk in response:
            print(chunk['response'], end='', flush=True)
        print("\n")

if __name__ == "__main__":
    chat()
