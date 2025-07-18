maze = """...###.#####.#####.#####.##.##...................
......#.....#.....#.....#..#..#........#........#
#..#..#..###...###...#..#..#..#..#######..#..###.
#..#........#.....#..#........#..#........#.....#
.########...#..###.##...####..#..#..#..####..#..#
#..#.....#...........#..#..#..#.....#..#.....#..#
#...###...###..#..#..#..#..#..#...##.##.###...##.
#.....#..#.....#..#..#.....#..#..#........#..#..#
#..###...#..###.##...#...##.##.##.##...###...#..#
#.................#..#..#........#..#...........#
.###..####..#...##...#..#..######...#..######.##.
#..#..#.....#..#........#.....#..#...........#..#
#..#..######.##...####..#..#..#..###...###...#..#
#...........#..#..#..#..#..#..#.....#.....#.....#
.#####.##...#..#..#..#..#..#..#..###.##....#####.
#.....#..#..#..#.....#..#..#..#.....#..#.....#..#
#..#..#...##....##....##....##...#..#..#..###...#
#..#........#..#..#..#...........#........#.....#
.##.###..#..#..#..#..#..#..###.######..#..#..###.
#..#.....#..#.....#..#..#.....#........#........#
#..#..###.###..##########..###.######..######...#
#.....#.............................#........#..#
#..#...#####...##########..#########...######...#
#..#........#.....#..#.....#........#..#.....#..#
#...#####.##....##...#..###.######..#..#..#..#..#
#..#.....#.....#..#........#........#..#..#.....#
#..#..####...##...###.###..####..#...##.##.###..#
#...........#..#.....#........#..#..#..#........#
.###..####..#..#..###...######.##...#...#####...#
#.....#.....#.....#....................#.....#..#
#..###.#####.###..#..##########..####..#..###.##.
#..............#...........#........#...........#
.##############.###########.########.#########..#"""

## start = 23, 11
## size: 49 * 33
maze = maze.split('\n')
maze = list(map(lambda x: x.replace("#","1").replace(".","0"), maze))
maze = ''.join(maze)
for i in range(0,len(maze), 256):
    print(hex(int(maze[i:i+256][::-1],2)))

maze = [0x41327924f1b91fe820120120804b93f9248e3926010092082080000036fbefb8
0x8c4f3a002402480003238db6237239920124124120b1db1249271c6412092400
0x24904920be1b9249246fa082092492003238e493c6fc9900120804824b7e47e4
0xf9fb9ff9dc9804020920904b927ee49249da0804004920131c9230c30c499048
0x260920100904132493f7230df1904804120804c7e3fe7fe3e264020000000831
0x4000b7279ff93bee64100000820831f11bf1c93ce804920104800ced89e7718f
0x13feff7ff7ffe80080400]
# aaawwwwwwaaaaaaaaaawwaaaaaawwaaaaw -> 0,0
maze = [format(x,'0256b')[::-1] for x in maze]
maze = [list(x) for x in maze]
maze = sum(maze,[])