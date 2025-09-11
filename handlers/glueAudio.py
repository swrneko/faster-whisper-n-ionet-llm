from pydub import AudioSegment

class GlueAudio():
    def glue(self, audioFiles):
        glued = AudioSegment.empty()

        for audioFile in audioFiles:
            audio = AudioSegment.from_file(audioFile)
            glued += audio

        return glued
