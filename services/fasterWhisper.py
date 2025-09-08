from faster_whisper import WhisperModel

class FasterWhisper:
    def __init__(self):
        pass

    def recognize(self, model, audioFile, beamSize, vadFilter, minSilenceDurationMs, speechPadMs, temp0, temp1, temp2, wordTimestamps, noSpeechThreshold, conditionOnPreviousText):
        model = WhisperModel(model, device='cuda', compute_type='float16') # Задаем модель

        segments, _ = model.transcribe( # Распознаем текст
            audioFile,
            beam_size=beamSize,
            vad_filter=vadFilter,
            vad_parameters={
                "min_silence_duration_ms": minSilenceDurationMs,
                "speech_pad_ms": speechPadMs
            },
            temperature= [temp0, temp1, temp2],
            word_timestamps=wordTimestamps,
            no_speech_threshold=noSpeechThreshold,
            condition_on_previous_text=conditionOnPreviousText
        )

        text = ''

        for seg in segments:
            text += f"[{self.format_timestamp(seg.start)} -> {self.format_timestamp(seg.end)}] {seg.text}" + '\n'
        
        return(text)

    def format_timestamp(self, seconds: float) -> str:
        millis = int(seconds * 1000)
        hours = millis // (3600 * 1000)
        minutes = (millis % (3600 * 1000)) // (60 * 1000)
        seconds_int = (millis % (60 * 1000)) // 1000
        millis = millis % 1000
        return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{millis:03d}"


