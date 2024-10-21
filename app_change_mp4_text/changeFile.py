import os
import subprocess
import whisper
import openai


def extract_audio_from_mp4(input_file, output_audio="audio.wav"):
    """
    Extrai o áudio de um arquivo MP4.
    """
    command = f"ffmpeg -i {input_file} -vn -acodec pcm_s16le -ar 16000 -ac 1 {output_audio}"
    subprocess.call(command, shell=True)
    return output_audio


def transcribe_audio(audio_file):
    """
    Transcreve o áudio para texto usando o Whisper da OpenAI.
    """
    model = whisper.load_model("base")  # Escolha o modelo conforme sua necessidade.
    result = model.transcribe(audio_file)
    return result["text"]


def enhance_text_with_chatgpt(text, api_key):
    """
    Processa o texto transcrito com o GPT para melhorar a qualidade ou tradução.
    """
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente que traduz e corrige transcrições."},
            {"role": "user", "content": f"Por favor, traduza e corrija o seguinte texto: {text}"}
        ]
    )
    return response['choices'][0]['message']['content']


def main():
    # Caminhos dos arquivos
    input_mp4 = "Glicose1.mp4"
    audio_file = "audio.wav"

    # Chave da API do OpenAI
    openai_api_key = "SUA_API_KEY"

    # 1. Extrair áudio do MP4
    print("Extraindo áudio...")
    audio_file = extract_audio_from_mp4(input_mp4, audio_file)

    # 2. Transcrever áudio para texto
    print("Transcrevendo áudio...")
    transcribed_text = transcribe_audio(audio_file)

    # 3. Melhorar ou traduzir o texto com GPT
    print("Processando texto com GPT...")
    enhanced_text = enhance_text_with_chatgpt(transcribed_text, openai_api_key)

    # 4. Resultado final
    print("Texto final:")
    print(enhanced_text)


if __name__ == "__main__":
    main()
