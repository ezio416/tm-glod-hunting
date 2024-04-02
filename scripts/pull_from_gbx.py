# c 2024-04-01
# m 2024-04-01

import os


def read_map(path: str) -> dict:
    with open(path, 'r', errors='ignore') as f:
        contents: str = f.read().split('</header>')[0]

    uid: str = contents.split('<ident uid="')[1][:27]
    if uid[-1] == '"':
        uid = uid[:26]

    map_name: str = contents.split('" name="')[1].split('"')[0]
    map_name = f'0{map_name[-1]}_{map_name}'

    map_type: str = map_name[3:-2]

    times: str = contents.split('<times ')[1].split('"/>')[0]

    t1:          str = times.split('bronze="')[1]
    bronze:      int = int(t1.split('"')[0])

    t2:          str = t1.split(' silver="')[1]
    silver:      int = int(t2.split('"')[0])

    t3:          str = t2.split(' gold="')[1]
    gold:        int = int(t3.split('"')[0])

    t4:          str = t3.split(' authortime="')[1]
    authorTime:  int = int(t4.split('"')[0])

    t5:          str = t4.split(' authorscore="')[1]
    authorScore: int = int(t5.split('"')[0])

    return {
        'uid':         uid,
        'name':        map_name,
        'type':        map_type,
        'bronze':      bronze,
        'silver':      silver,
        'gold':        gold,
        'authorTime':  authorTime,
        'authorScore': authorScore
    }


def read_replay(path: str) -> dict:
    with open(path, 'r', errors='ignore') as f:
        contents: str = f.read().split('</header>')[0]

    uid: str = contents.split('<challenge uid="')[1].split('"/>')[0]

    times: str = contents.split('<times ')[1].split('"/>')[0]

    t1:       str = times.split('best="')[1]
    best:     int = int(t1.split('"')[0])

    t2:       str = t1.split(' respawns="')[1]
    respawns: int = int(t2.split('"')[0])

    t3:       str = t2.split(' stuntscore="')[1]
    score:    int = int(t3.split('"')[0])

    return {
        'uid':      uid,
        'best':     best,
        'respawns': respawns,
        'score':    score
    }


def main() -> None:
    maps: dict = {}

    dirs: tuple[str] = (
        'B:/PortableGames/TrackMania Original/GameData/Tracks/Campaigns/Nadeo/Original/Series/Platform',
        'B:/PortableGames/TrackMania Original/GameData/Tracks/Campaigns/Nadeo/Original/Series/Puzzle',
        'B:/PortableGames/TrackMania Original/GameData/Tracks/Campaigns/Nadeo/Original/Series/Race',
        'B:/PortableGames/TrackMania Original/GameData/Tracks/Campaigns/Nadeo/Original/Series/Stunts'
    )

    for dir in dirs:
        os.chdir(dir)

        for file in os.listdir('.'):
            if not file.endswith('Challenge.Gbx'):
                continue

            map_info: dict = read_map(file)
            maps[map_info['uid']] = map_info

    os.chdir('B:/PortableGames/TrackMania Original/GameData/Tracks/Replays/Autosaves')

    for file in os.listdir('.'):
        if not file.endswith('Replay.gbx'):
            continue

        pb: dict = read_replay(file)
        maps[pb['uid']]['pb'] = pb

    for uid, map in maps.items():
        if map['type'] == 'Race':
            map['grandparent'] = '01_Race'
        elif map['type'] == 'Puzzle':
            map['grandparent'] = '02_Puzzle'
        elif map['type'] == 'Platform':
            map['grandparent'] = '03_Platform'
        elif map['type'] == 'Stunts':
            map['grandparent'] = '04_Stunts'

        if map['name'][-2] == 'A':
            map['parent'] = f'01_{map['name'][3:-1]}'
        elif map['name'][-2] == 'B':
            map['parent'] = f'02_{map['name'][3:-1]}'
        elif map['name'][-2] == 'C':
            map['parent'] = f'03_{map['name'][3:-1]}'
        elif map['name'][-2] == 'D':
            map['parent'] = f'04_{map['name'][3:-1]}'
        elif map['name'][-2] == 'E':
            map['parent'] = f'05_{map['name'][3:-1]}'
        elif map['name'][-2] == 'F':
            map['parent'] = f'06_{map['name'][3:-1]}'
        elif map['name'][-2] == 'G':
            map['parent'] = f'07_{map['name'][3:-1]}'

    final: dict = {
        '01_Race': {},
        '02_Puzzle': {},
        '03_Platform': {},
        '04_Stunts': {}
    }

    for uid, map in maps.items():
        to_insert: dict = {
            'mapUid': map['uid'],
            'medals': {}
        }

        if map['type'] in ('Race', 'Puzzle'):
            to_insert['medals']['author'] = map['authorTime']
        elif map['type'] == 'Stunts':
            to_insert['medals']['author'] = map['authorScore']

        to_insert['medals']['gold']   = map['gold']
        to_insert['medals']['silver'] = map['silver']
        to_insert['medals']['bronze'] = map['bronze']

        if map['type'] in ('Race', 'Puzzle'):
            to_insert['medals']['ezio'] = map['pb']['best']
        elif map['type'] == 'Platform':
            to_insert['medals']['ezio'] = map['pb']['respawns']
        elif map['type'] == 'Stunts':
            to_insert['medals']['ezio'] = map['pb']['score']

        if not final[map['grandparent']].get(map['parent']):
            final[map['grandparent']][map['parent']] = {}

        final[map['grandparent']][map['parent']][map['name']] = to_insert
        final_str: str = str(final).replace("'", '"')

    pass


if __name__ == '__main__':
    main()
