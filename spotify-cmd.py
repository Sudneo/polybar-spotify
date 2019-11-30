#!/usr/bin/python3
import dbus
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--playing', action='store_true', help="Returns the info about the song currently playing.")
    group.add_argument('--playpause_icon', action='store_true', help="Prints the icon opposite to status (Play if music"
                                                                     " is stopped, Pause if music is playing.")
    group.add_argument('--playpause', action='store_true', help="Plays/Pauses the current song.")
    group.add_argument('--next', action='store_true', help="Play next song if available, otherwise do nothing.")
    group.add_argument('--next_icon', action='store_true', help="Print previous symbol.")
    group.add_argument('--previous', action='store_true', help="Play previous song if available, otherwise do nothing.")
    group.add_argument('--previous_icon', action='store_true', help="Print next symbol.")
    parser.add_argument('--trim_or_pad', type=int, metavar="max_length", help="Max length for the song string")
    args = parser.parse_args()
    return args


def trim_or_pad(string, length):
    if len(string) > length:
        return string[:length]
    elif len(string) < length:
        return string + " " * (length - len(string))
    else:
        return string


def main():
    args = get_args()
    try:
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object(
            'org.mpris.MediaPlayer2.spotify',
            '/org/mpris/MediaPlayer2'
        )

        spotify_properties = dbus.Interface(
            spotify_bus,
            'org.freedesktop.DBus.Properties'
        )
        interface = dbus.Interface(spotify_bus, dbus_interface='org.mpris.MediaPlayer2.Player')
        if args.playing:
            # We need to print Song name - Artist (Album)
            status = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
            if args.trim_or_pad:
                max_length = args.trim_or_pad
            if status not in ['Playing', 'Paused', 'Stopped']:
                if args.trim_or_pad:
                    print(trim_or_pad('Spotify is not running'), max_length)
                else:
                    print('Spotify is not Running')
            metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            song_name = metadata['xesam:title']
            artist = metadata['xesam:artist'][0]
            album = metadata['xesam:albumArtist'][0]
            dash = '\u2014'
            status_icon = '\uf1bc'
            if args.trim_or_pad:
                print(trim_or_pad(f'{status_icon} {song_name} {dash} {artist} ({album})', max_length))
            else:
                print(f'{status_icon} {song_name} {dash} {artist} ({album})')
            exit(0)
        elif args.playpause:
            interface.PlayPause()
            exit(0)
        elif args.next:
            interface.Next()
            exit(0)
        elif args.previous:
            interface.Previous()
            exit(0)
        elif args.playpause_icon:
            status = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
            if status == 'Playing':
                print('\uf04c')
            else:
                print('\uf04b')
        elif args.next_icon:
            print("\uf051")
        elif args.previous_icon:
            print("\uf048")
    except Exception as error:
        exit(1)


main()
