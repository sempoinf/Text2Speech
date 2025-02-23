

if __name__ == "__main__":
    chunker = TextChunker()
    # text = "Небо было пасмурным, а тёмные облака подавляли величественную атмосферу Дворца. Великолепный дворцовый зал был окутан тёмными облаками, как будто это была огромная клетка, крепко удерживающая людей."
    # print(len(text))
    # formated_txt = chunker.split_text(text)
    # print(len(formated_txt)) # out 2, cause 198 symbs
    test_txt = chunker.from_file(r'../Pets/test_text.txt', split=True)
    # print(test_txt)
    # print(len(test_txt))
    # exit()
    
    tts = CoquiTTS(gpu=True)
    # model_name = "tts_models/multilingual/multi-dataset/xtts_v2"

    # stopped on 73 fragment
    for i, segment in enumerate(islice(test_txt, 0, None), start=1):
        print(i)
        # print(len(segment))
        path_save_file = f"output/coqui/Chong_Sheng_Zhi_Jiang_Men_Du_Hou/Glava_1_{i}.wav"
        tts.synthesize(str(segment), path_save_file, speaker= 'Baldur Sanjin', language="ru")
        print(f"Complete for fragment {i}")
    print(f"Complete for all")


    # processor = AudioPostProcessor(directory="output", base_filename="tts_output", output_format="mp3")
    # fin_audio_path = processor.merge_audio()
    # print(f"File merged: {fin_audio_path}")

        