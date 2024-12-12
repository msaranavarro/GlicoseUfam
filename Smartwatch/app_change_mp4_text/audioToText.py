from pydub import AudioSegment
import speech_recognition as sr
import os
import json


def converter_mp4_para_wav(caminho_mp4, caminho_wav):
    """
    Converte um arquivo MP4/M4A para WAV.
    """
    try:
        # Carrega o áudio do arquivo MP4/M4A
        audio = AudioSegment.from_file(caminho_mp4, format="mp4")
        # Exporta o áudio como WAV
        audio.export(caminho_wav, format="wav")
        print(f"Arquivo convertido: {caminho_wav}")
    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")


def audio_para_texto(caminho_wav):
    """
    Converte o áudio de um arquivo WAV para texto usando reconhecimento de fala.
    """
    reconhecedor = sr.Recognizer()

    try:
        # Carrega o arquivo de áudio
        with sr.AudioFile(caminho_wav) as source:
            print("Processando o áudio...")
            audio = reconhecedor.record(source)

        # Reconhece o texto usando o Google Web Speech API
        texto = reconhecedor.recognize_google(audio, language='pt-BR')
        print("Texto reconhecido:")
        print(texto)

        # Converte o texto reconhecido para JSON
        resultado_json = json.dumps({"texto_reconhecido": texto}, ensure_ascii=False, indent=4)
        print("Resultado em JSON:")
        print(resultado_json)

        return resultado_json

    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
        return json.dumps({"erro": "Não foi possível entender o áudio"}, ensure_ascii=False)

    except sr.RequestError as e:
        print(f"Erro na solicitação: {e}")
        return json.dumps({"erro": f"Erro na solicitação: {str(e)}"}, ensure_ascii=False)


def main():
    # Caminhos dos arquivos
    input_mp4 = r"C:\Users\ALUNO\Documents\Sara\GlicoseUfam\app_change_mp4_text\Glicose2.mp4"
    audio_file = "Glicose2.wav"

    # Passo 1: Converter MP4/M4A para WAV
    if not os.path.exists(input_mp4):
        print(f"Arquivo MP4/M4A não encontrado: {input_mp4}")
        return

    converter_mp4_para_wav(input_mp4, audio_file)

    # Passo 2: Converter áudio para texto
    if os.path.exists(audio_file):
        resultado = audio_para_texto(audio_file)
        # Exemplo: Salvar o resultado JSON em um arquivo
        with open("resultado.json", "w", encoding="utf-8") as arquivo_json:
            arquivo_json.write(resultado)
    else:
        print(f"Arquivo WAV não encontrado: {audio_file}")


if __name__ == "__main__":
    main()
