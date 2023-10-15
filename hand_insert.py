from moviestowatch import Moviestowatch

############## Mau cho Movie
# film_data = {
#     "title": "PAW Patrol: The Mighty Movie",
#     "slug": "paw-patrol-the-mighty-movie",
#     "description": "A magical meteor crash-lands in Adventure City, gives the PAW Patrol pups superpowers, and transforms them into The Mighty Pups. When the Patrol's archrival Humdinger breaks out of jail and teams up with mad scientist Victoria Vance to steal the powers for themselves, the Mighty Pups must save Adventure City and stop the supervillains before it's too late.",
#     "post_type": "single",
#     "trailer_id": "GxfoQlmduvc",
#     "cover_src": "https://web.fmoviesto.site/_sf/287/08558438.jpg",
#     "extra_info": {
#         "Quality": "HD",
#         "Duration": "92 min",
#         "Country": " United States, Canada",
#         "Genre": "Movies, Animation, Action, Adventure",
#         "Released": "2023",
#         "Director": "Cal Brunker",
#         "Casts": " Finn Lee-Epp, Ron Pardo, Mckenna Grace",
#     },
# }
# episodes_data = {"Episode 1": "https://vidsrc.to/embed/movie/tt15837338"}


############## Mau cho TV Shows
film_data = {
    "title": "Pantheon Season 2",
    "slug": "pantheon-season-2",
    "description": "A bullied teen receives mysterious help from someone online: a stranger soon revealed to be her recently deceased father, David, whose consciousness has been uploaded to the Cloud following an experimental destructive brain scan. David is the first of a new kind of being – an “Uploaded Intelligence” or “UI” – but he will not be the last, as a global conspiracy unfolds that threatens to trigger a new kind of world war.",
    "post_type": "series",
    "trailer_id": "z_HJ3TSlo5c",
    "cover_src": "https://web.fmoviesto.site/_sf/287/70395598.jpg",
    "extra_info": {
        "Quality": "HD",
        "Duration": "42 min",
        "Country": " United States",
        "Genre": "Drama, TV Shows, Animation, Action",
        "Released": "2023",
        "Director": "Craig Silverstein",
        "Casts": " Katie Chang, Paul Dano, Aaron Eckhart",
        "Tags": "Watch Pantheon Season 2 Online Free,Pantheon Season 2 Online Free,Where to watch Pantheon Season 2,Pantheon Season 2 movie free online,Pantheon Season 2 free online",
    },
}
episodes_data = {
    "Episode 1": "https://vidsrc.to/embed/tv/tt11680642/2/1",
    "Episode 2": "https://vidsrc.to/embed/tv/tt11680642/2/2",
    "Episode 3": "https://vidsrc.to/embed/tv/tt11680642/2/3",
    "Episode 4": "https://vidsrc.to/embed/tv/tt11680642/2/4",
    "Episode 5": "https://vidsrc.to/embed/tv/tt11680642/2/5",
    "Episode 6": "https://vidsrc.to/embed/tv/tt11680642/2/6",
    "Episode 7": "https://vidsrc.to/embed/tv/tt11680642/2/7",
    "Episode 8": "https://vidsrc.to/embed/tv/tt11680642/2/8",
}


def main():
    Moviestowatch(film=film_data, episodes=episodes_data).insert_film()


if __name__ == "__main__":
    main()
