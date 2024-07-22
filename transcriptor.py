from langchain_community.document_loaders import YoutubeLoader
from langchain_core.exceptions import LangChainException


def get_transcript_from_youtube_with_url(video_url):
    all_languages = [
        "en", "hi", "bn", "te", "mr", "ta", "gu", "kn", "ml", "pa",
        "as", "or", "sd", "ur", "ne", "ks", "kok", "doi", "mni", "sit", "sa",
        "aa", "ab", "ae", "af", "ak", "am", "an", "ar", "av", "ay", "az", "ba",
        "be", "bg", "bi", "bm", "bo", "br", "bs", "ca", "ce", "ch", "co", "cr",
        "cs", "cu", "cv", "cy", "da", "de", "dv", "dz", "ee", "el", "eo", "es",
        "et", "eu", "fa", "ff", "fi", "fj", "fo", "fr", "fy", "ga", "gd", "gl", "gn",
        "gv", "ha", "he", "ho", "hr", "ht", "hu", "hy", "hz", "ia", "id",
        "ie", "ig", "ii", "ik", "io", "is", "it", "iu", "ja", "jv", "ka", "kg", "ki",
        "kj", "kk", "kl", "km", "ko", "kr", "ks", "ku", "kv", "kw", "ky", "la",
        "lb", "lg", "li", "ln", "lo", "lt", "lu", "lv", "mg", "mh", "mi", "mk", "ml",
        "mn", "ms", "mt", "my", "na", "nb", "nd", "ne", "ng", "nl", "nn", "no",
        "nr", "nv", "ny", "oc", "oj", "om", "or", "os", "pa", "pi", "pl", "ps", "pt",
        "qu", "rm", "rn", "ro", "ru", "rw", "sa", "sc", "sd", "se", "sg", "si", "sk",
        "sl", "sm", "sn", "so", "sq", "sr", "ss", "st", "su", "sv", "sw", "ta", "te",
        "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "ts", "tt", "tw", "ty", "ug",
        "uk", "ur", "uz", "ve", "vi", "vo", "wa", "wo", "xh", "yi", "yo", "za", "zh",
        "zu"
    ]

    translations = ["en", "hi", "bn", "te", "mr", "ta", "gu", "kn", "ml", "pa", "as", "or", "sd", "ur", "ne", "ks",
                    "kok", "doi", "mni", "sit", "sa"]

    for translation in translations:
        try:
            loader = YoutubeLoader.from_youtube_url(
                video_url,
                add_video_info=True,
                language=all_languages,
                translation=translation,
            )

            documents = loader.load()
            transcripts = "\n".join([doc.page_content for doc in documents if doc.page_content])
            if transcripts:
                return transcripts

        except LangChainException:
            continue

        except Exception as e:
            return f"Error: {e}"

    return "Transcript not found"
