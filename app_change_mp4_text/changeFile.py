import os
import subprocess
import whisper
import openai

# Adicionando o caminho do FFmpeg à variável PATH
os.environ["PATH"] += os.pathsep + r"C:\Users\ALUNO\ffmpeg-7.1-full_build\bin"

def check_ffmpeg_installed():
    """Verifica se o FFmpeg está instalado e acessível."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("FFmpeg está instalado corretamente.")
        else:
            print("Erro ao tentar acessar o FFmpeg.")
            return False
    except FileNotFoundError:
        print("FFmpeg não encontrado. Por favor, instale o FFmpeg e adicione ao PATH.")
        return False
    return True

def extract_audio_from_mp4(input_file, output_audio="audio.wav"):
    """
    Extrai o áudio de um arquivo MP4.
    """
    try:
        command = f"ffmpeg -i {input_file} -vn -acodec pcm_s16le -ar 16000 -ac 1 {output_audio}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"Áudio extraído com sucesso: {output_audio}")
            return output_audio
        else:
            print(f"Erro ao extrair áudio: {result.stderr.decode()}")
            return None
    except Exception as e:
        print(f"Erro ao extrair áudio: {e}")
        return None

def transcribe_audio(audio_file):
    """
    Transcreve o áudio para texto usando o Whisper da OpenAI.
    """
    try:
        model = whisper.load_model("base")  # Escolha o modelo conforme sua necessidade.
        result = model.transcribe(audio_file)
        print("Áudio transcrito com sucesso.")
        return result["text"]
    except Exception as e:
        print(f"Erro ao transcrever áudio: {e}")
        return None

def enhance_text_with_chatgpt(text, api_key):
    """
    Processa o texto transcrito com o GPT para melhorar a qualidade ou tradução.
    """
    try:
        openai.api_key = api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que traduz e corrige transcrições."},
                {"role": "user", "content": f"Por favor, traduza e corrija o seguinte texto: {text}"}
            ]
        )
        print("Texto processado com sucesso pelo GPT.")
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erro ao processar texto com GPT: {e}")
        return None

def main():
    # Verificar se o FFmpeg está instalado
    if not check_ffmpeg_installed():
        return

    # Caminhos dos arquivos
    input_mp4 = r"C:\Users\ALUNO\Documents\Sara\GlicoseUfam\app_change_mp4_text\Glicose3.m4a"
    audio_file = "Glicose3.wav"

    # Chave da API do OpenAI (não exposta diretamente no código)
    openai_api_key = "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"  # Defina a chave de API como variável de ambiente

    # 1. Extrair áudio do MP4
    print("Extraindo áudio...")
    audio_file = extract_audio_from_mp4(input_mp4, audio_file)
    if audio_file is None:
        return  # Se falhar, não continua

    # 2. Transcrever áudio para texto
    print("Transcrevendo áudio...")
    transcribed_text = transcribe_audio(audio_file)
    if transcribed_text is None:
        return  # Se falhar, não continua

    # 3. Melhorar ou traduzir o texto com GPT
    print("Processando texto com GPT...")
    enhanced_text = enhance_text_with_chatgpt(transcribed_text, openai_api_key)
    if enhanced_text is None:
        return  # Se falhar, não continua

    # 4. Resultado final
    print("Texto final:")
    print(enhanced_text)

# Certifique-se de usar o nome correto da função principal
if __name__ == "__main__":
    main()
