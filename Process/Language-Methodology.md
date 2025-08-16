Multilingual Subtitles 
Sources: Best Picture, Cinematography, Screenwriting, Animations, Foreign Language, Oscars Submissions, Mubi Lists, Awards Lists
Primary Language: German, French, Russian, Spanish, Italian, Portuguese, English, Arabic, Chinese, Japanese, South Korea, Hindi, Indonesian
Streaming method: Watch full, watch skipping, get Screenshots, do chatgpt Lacanian Analysis, do Jouissance classification 
Create e-book from subtitles, get important dialogues

Resources: subtitles, ebook, input text

## Dual Subtitles: Chrome extension for 
Netflix: https://chromewebstore.google.com/detail/netflix-dual-subtitles-su/fkmkfpejabcjnabammjkhodkpjjbfipo
HBO max: https://chromewebstore.google.com/detail/hbo-max-dual-subtitles-su/hgonbljnbdgjdmflachhbplipifagfei
SM player + Translate Subtitles + Merge Subtitles + Transliteration
asbplayer: Language-learning with subtitles: https://chromewebstore.google.com/detail/asbplayer-language-learni/hkledmpjpaehamkiehglnbelcpdflcab
https://github.com/killergerbah/asbplayer?tab=readme-ov-file#getting-started
AI Subtitles & Immersive Translate - Trancy: https://chromewebstore.google.com/detail/ai-subtitles-immersive-tr/mjdbhokoopacimoekfgkcoogikbfgngb?hl=en
https://www.trancy.org/changelog?

To do:
Mubi
Wow Presents

## Epub Versions: Calibre + Python
Original
Translation
Only-Translation = remove original
Double
Triple: Double + Transliteration
n-Multilingual: (en, es, pt, fr, it, ge, ru, ar, hi, ch, ja, ko)

## n-Multilingual App
Take an input, translate/transliterate:
(en, es, pt, fr, it, ge, ru, ar, hi, ch, ja, ko)


Useful examples of regular expressions:

([\(（]([^\(\)（）]|(([\(（][^\(\)（）]+[\)）])))+[\)）]) : Remove names enclosed by parenthesis to indicate speakers (e.g. "（山田）　元気ですか？")
(.*)\n+(?!-)(.*) : Some subtitles are split in several lines and this regex forces them into a single line. For this filter to work, you must also put $1 $2 in the "Subtitle regex filter text replacement" field.
NB: When using this regex pattern in combination with other patterns (using the | operator, see below), place this pattern at the end. This ensures that all other regex transformations are applied first, and then the results are finally combined into a single line.
-?\[.*\] : Remove indications enclosed by square brackets that sound or music that is playing (e.g. "[PLAYFUL MUSIC]" or "-[GASPS]")
^[\-\(\)\.\s\p{Lu}]+$ : As an alternative to the above, filter out descriptions written in capital letters, but without the square brackets (e.g. "PLAYFUL MUSIC"). If your language has additional letters with diacritics, you feel free to add them to this list.
[♪♬#～〜]+ : Any combination of symbols on their own that represent playing music (e.g. ♪♬♪)
