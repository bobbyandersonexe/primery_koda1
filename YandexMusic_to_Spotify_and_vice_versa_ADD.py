# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import yandex

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # artist, title = yandex.print_name_of_a_track('https://music.yandex.ru/album/4807334/track/37840510')
    artist, title = yandex.print_name_of_a_track('https://music.yandex.ru/album/4807335/track/37840525')
    yandex.get_url_from_spotify_by_artist_and_title(artist, title)
