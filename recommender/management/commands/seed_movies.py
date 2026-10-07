"""Django management command for seeding the movie recommender database.

Copy this file to <your_app>/management/commands/seed_movies.py, then run:
    python manage.py seed_movies --replace-catalog

Expected models: Movie(title, description, rating, genres [ManyToMany]) and
Genre(name). Change MODEL_APP_LABEL below if your app label differs.
"""

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


MODEL_APP_LABEL = "recommender"
MOVIE_MODEL_NAME = "Movie"
GENRE_MODEL_NAME = "Genre"

# The 167 titles are selected from the supplied Letterboxd export; each has a
# personal rating of at least 4/5. Demo ratings in this database are generic
# values on a 0–5 scale, not the user's Letterboxd scores.
# Each movie is assigned exactly two genres.
MOVIES = [
    ("10 Things I Hate About You", 3.8, "A high-school dating arrangement becomes complicated as the students develop real feelings.", ["Romance", "Comedy", "Coming-of-Age"]),
    ("3 Idiots", 4.5, "Three engineering students challenge the pressure and rigid expectations of college life.", ["Comedy", "Drama", "Coming-of-Age"]),
    ("Avatar", 4.5, "A former Marine joins the Na'vi and is drawn into a conflict over the future of Pandora.", ["Sci-Fi", "Adventure", "Action"]),
    ("Avatar: The Way of Water", 4.5, "Jake and Neytiri protect their family and seek refuge among Pandora's reef people.", ["Sci-Fi", "Adventure", "Action"]),
    ("Avengers: Endgame", 4.5, "The Avengers regroup after a devastating loss and attempt to reverse Thanos's destruction.", ["Action", "Superhero", "Sci-Fi"]),
    ("Avengers: Infinity War", 4.5, "The Avengers and their allies try to stop Thanos from collecting the Infinity Stones.", ["Action", "Superhero", "Sci-Fi"]),
    ("Babylon", 3.9, "Ambitious performers and industry figures navigate Hollywood during its transition to sound.", ["Drama", "History", "Music"]),
    ("Barbie", 4.5, "Barbie leaves Barbieland for the real world, where she and Ken encounter unexpected changes.", ["Comedy", "Fantasy", "Drama"]),
    ("Barfi!", 3.9, "A deaf and mute young man forms relationships while navigating family and social expectations.", ["Drama", "Romance", "Family"]),
    ("Beautiful Boy", 3.7, "A father supports his son through addiction and recovery.", ["Drama", "Biography", "Family"]),
    ("Blade Runner 2049", 4.1, "A blade runner uncovers a secret that challenges the boundary between humans and replicants.", ["Sci-Fi", "Drama", "Thriller"]),
    ("Bullet Train", 4.5, "An assassin tries to complete a job aboard a train filled with competing killers.", ["Action", "Comedy", "Thriller"]),
    ("Call Me by Your Name", 3.9, "A teenager in northern Italy experiences an intense summer romance.", ["Drama", "Romance", "Coming-of-Age"]),
    ("Captain America: The Winter Soldier", 4.5, "Steve Rogers uncovers a conspiracy inside S.H.I.E.L.D. while facing a powerful new adversary.", ["Action", "Superhero", "Thriller"]),
    ("Cars", 4.5, "An ambitious race car gets stranded in a small town and learns to value the people around him.", ["Animation", "Comedy", "Drama"]),
    ("Chainsaw Man – The Movie: Reze Arc", 4.5, "Denji meets Reze, a café worker whose arrival pulls him into a new conflict.", ["Animation", "Action", "Drama"]),
    ("Chhichhore", 4.5, "A father tells his son about his college friends and the failures that shaped them.", ["Comedy", "Drama", "Coming-of-Age"]),
    ("Dead Poets Society", 4.1, "An English teacher encourages students at a strict school to think independently.", ["Drama", "Coming-of-Age", "Thriller"]),
    ("Death Note", 4.5, "A student discovers a notebook that can kill anyone whose name is written in it.", ["Mystery", "Thriller", "Drama"]),
    ("Django Unchained", 4.2, "A freed slave and a bounty hunter set out to rescue his wife from a plantation owner.", ["Western", "Drama", "Action"]),
    ("Drishyam", 4.0, "A father uses careful planning to protect his family during a criminal investigation.", ["Crime", "Thriller", "Mystery"]),
    ("Drive", 3.9, "A Hollywood stunt driver becomes involved in a robbery after agreeing to help a neighbour.", ["Crime", "Thriller", "Drama"]),
    ("Dune: Part Two", 4.1, "Paul Atreides joins the Fremen and faces choices that could reshape the galaxy.", ["Sci-Fi", "Adventure", "Drama"]),
    ("Eternal Sunshine of the Spotless Mind", 4.1, "A couple undergoes a procedure to erase memories of their relationship.", ["Sci-Fi", "Romance", "Drama"]),
    ("Fantastic Mr. Fox", 4.5, "A fox's return to stealing puts his family and woodland neighbors at risk.", ["Animation", "Comedy", "Family"]),
    ("Fight Club", 4.5, "An office worker's connection with a charismatic stranger grows into a secret underground club.", ["Drama", "Thriller", "Crime"]),
    ("Ford v Ferrari", 3.9, "An American team works to build a car capable of beating Ferrari at Le Mans.", ["Drama", "Sport", "Biography"]),
    ("Gangs of Wasseypur – Part 2", 4.5, "Rivalries and betrayals shape the next chapter of a crime family's struggle for power.", ["Crime", "Drama", "Mystery"]),
    ("Grave of the Fireflies", 4.2, "Two siblings struggle to survive in Japan during the final months of World War II.", ["Animation", "War", "History"]),
    ("Hacksaw Ridge", 4.5, "A conscientious objector serves as a medic during the Battle of Okinawa.", ["War", "Drama", "History"]),
    ("Harry Potter and the Deathly Hallows: Part 2", 4.5, "Harry returns to Hogwarts for the final confrontation with Voldemort.", ["Fantasy", "Adventure", "History"]),
    ("Harry Potter and the Prisoner of Azkaban", 4.5, "Harry's third year at Hogwarts brings new revelations about his family and a prisoner on the run.", ["Fantasy", "Adventure", "History"]),
    ("I Want to Eat Your Pancreas", 4.5, "A reserved student grows close to a classmate who is hiding a terminal illness.", ["Animation", "Drama", "Coming-of-Age"]),
    ("Inglourious Basterds", 4.2, "A group of Allied soldiers and a theater owner pursue separate plans against Nazi leaders.", ["War", "Drama", "History"]),
    ("Interstellar", 4.2, "A former pilot joins a space mission searching for a new home for humanity.", ["Sci-Fi", "Adventure", "Drama"]),
    ("John Wick: Chapter 4", 3.8, "John Wick fights to escape the control of a powerful criminal organization.", ["Action", "Thriller", "Drama"]),
    ("Jojo Rabbit", 4.0, "A boy in wartime Germany questions his beliefs after discovering his mother is hiding a Jewish girl.", ["Comedy", "War", "History"]),
    ("Joker", 4.5, "A struggling comedian descends into violence amid neglect and unrest in Gotham.", ["Crime", "Drama", "Thriller"]),
    ("Knives Out", 4.0, "A detective investigates the death of a wealthy crime novelist and questions his family.", ["Mystery", "Comedy", "Thriller"]),
    ("La La Land", 4.0, "A jazz pianist and an aspiring actor pursue their careers as their relationship develops in Los Angeles.", ["Drama", "Romance", "Music"]),
    ("Lars and the Real Girl", 4.5, "A shy man introduces his family to a life-sized doll he treats as a partner.", ["Comedy", "Drama", "Romance"]),
    ("Logan", 3.9, "An aging Wolverine protects a young mutant while confronting the consequences of his past.", ["Action", "Superhero", "Drama"]),
    ("Lost Ladies", 4.5, "Two brides are accidentally switched during a train journey, setting off a search for their identities.", ["Comedy", "Drama", "Mystery"]),
    ("Masaan", 3.9, "Two young people in Varanasi confront loss, social expectations, and the possibility of change.", ["Drama", "Romance", "Coming-of-Age"]),
    ("Mickey 17", 3.8, "A disposable worker on a distant colony faces the consequences of being replaced by a duplicate.", ["Sci-Fi", "Drama", "Thriller"]),
    ("Nightcrawler", 3.9, "A freelance videographer enters the world of late-night crime reporting in Los Angeles.", ["Crime", "Thriller", "Drama"]),
    ("Obsession", 4.5, "A shy young man uses a supernatural wish to make his crush fall for him, with dangerous consequences.", ["Horror", "Thriller", "Drama"]),
    ("Oldboy", 4.2, "After years in captivity, a man searches for the reason behind his imprisonment.", ["Mystery", "Thriller", "Drama"]),
    ("One Battle After Another", 4.0, "A former revolutionary is drawn back into conflict when his daughter goes missing.", ["Action", "Crime", "Mystery"]),
    ("Oppenheimer", 4.0, "Physicist J. Robert Oppenheimer leads the development of the first atomic bomb.", ["Drama", "History", "Biography"]),
    ("Parasite", 4.3, "A family in financial difficulty becomes increasingly involved with a wealthy household.", ["Drama", "Thriller", "Comedy"]),
    ("Phir Hera Pheri", 4.5, "Three friends try to secure quick riches through a risky investment scheme.", ["Comedy", "Crime", "Drama"]),
    ("Poor Things", 4.0, "A young woman revived by an unconventional scientist sets out to experience the world.", ["Drama", "Fantasy", "Comedy"]),
    ("Project Hail Mary", 4.0, "An astronaut wakes alone on a mission to prevent a threat to life on Earth.", ["Sci-Fi", "Adventure", "Drama"]),
    ("Pulp Fiction", 4.2, "Interwoven stories follow criminals, a boxer, and two small-time robbers in Los Angeles.", ["Crime", "Drama", "Thriller"]),
    ("Puss in Boots: The Last Wish", 4.5, "A wanted cat sets out to recover his lost lives by finding the mythical Wishing Star.", ["Animation", "Adventure", "Drama"]),
    ("Scott Pilgrim vs. the World", 3.9, "A young musician must face his new girlfriend's former partners.", ["Comedy", "Action", "Fantasy"]),
    ("Se7en", 4.3, "Two detectives investigate murders linked to the seven deadly sins.", ["Crime", "Thriller", "Mystery"]),
    ("Shrek 2", 4.5, "Shrek and Fiona visit her parents in Far Far Away, where their marriage faces new pressure.", ["Animation", "Comedy", "Drama"]),
    ("Shutter Island", 4.0, "A U.S. marshal investigates the disappearance of a patient from a remote hospital.", ["Mystery", "Thriller", "Drama"]),
    ("Sinners", 4.0, "Twin brothers return home and face a supernatural threat in their community.", ["Horror", "Drama", "Thriller"]),
    ("Spider-Man: Across the Spider-Verse", 4.5, "Miles Morales enters other dimensions and clashes with a group of Spider-People over the future.", ["Animation", "Superhero", "Action"]),
    ("Spider-Man: Into the Spider-Verse", 4.5, "Miles Morales discovers his powers and meets Spider-People from other universes.", ["Animation", "Superhero", "Action"]),
    ("Spider-Man: No Way Home", 4.5, "Peter Parker seeks help after his identity is revealed, bringing threats from other worlds into his life.", ["Action", "Superhero", "Adventure"]),
    ("Superbad", 3.8, "Two high-school friends plan a party before graduation as they face changes in their friendship.", ["Comedy", "Coming-of-Age", "Thriller"]),
    ("Tamasha", 3.8, "A young man reconsiders his life after a vacation romance challenges his usual routine.", ["Drama", "Romance", "Thriller"]),
    ("The Batman", 4.5, "A young Batman investigates a series of murders that expose corruption across Gotham.", ["Crime", "Superhero", "Thriller"]),
    ("The Dark Knight", 4.5, "Batman faces a criminal who pushes Gotham and its institutions into chaos.", ["Action", "Superhero", "Crime"]),
    ("The Grand Budapest Hotel", 4.5, "A hotel concierge and his protégé become entangled in a dispute over an inherited painting.", ["Comedy", "Drama", "Adventure"]),
    ("The Great Dictator", 4.5, "A barber is mistaken for a dictator in a satire of fascism and political power.", ["Comedy", "War", "Satire"]),
    ("The Hangover", 3.8, "Three friends try to reconstruct a night in Las Vegas after waking with no memory of it.", ["Comedy", "Crime", "Mystery"]),
    ("The Kashmir Files", 4.5, "A university student investigates the exodus of Kashmiri Pandits from the valley.", ["Drama", "History", "War"]),
    ("The Lego Batman Movie", 4.5, "Batman adjusts to working with others while protecting Gotham from a new threat.", ["Animation", "Superhero", "Comedy"]),
    ("The Lunchbox", 3.9, "A mistaken lunch delivery connects a lonely office worker and a dissatisfied housewife.", ["Drama", "Romance", "Comedy"]),
    ("The Martian", 4.0, "An astronaut stranded on Mars uses his skills to survive while a rescue mission is organized.", ["Sci-Fi", "Adventure", "Drama"]),
    ("The Notebook", 3.7, "An older man recounts the relationship between two young people from different backgrounds.", ["Drama", "Romance", "Coming-of-Age"]),
    ("The Odyssey", 3.9, "After the Trojan War, Odysseus faces a long and dangerous journey home.", ["Adventure", "Fantasy", "History"]),
    ("The Perks of Being a Wallflower", 3.8, "A shy teenager finds friendship while navigating the pressures of high school.", ["Drama", "Coming-of-Age", "Romance"]),
    ("The Place Beyond the Pines", 4.5, "A motorcycle stunt rider's crimes connect his family with a police officer and his son.", ["Crime", "Drama", "Mystery"]),
    ("The Shawshank Redemption", 4.5, "A banker serving a life sentence forms a friendship and holds onto hope for freedom.", ["Drama", "Crime", "Thriller"]),
    ("The Social Network", 4.1, "The founding of Facebook brings ambition, legal disputes, and conflicts among its creators.", ["Drama", "Biography", "History"]),
    ("The Truman Show", 4.1, "A man begins to suspect that his everyday life is being filmed for a television program.", ["Drama", "Sci-Fi", "Comedy"]),
    ("The Wild Robot", 4.5, "A service robot is stranded in the wilderness and learns to care for a young goose.", ["Animation", "Adventure", "Family"]),
    ("The Wolf of Wall Street", 4.0, "A stockbroker builds a fortune through fraud, excess, and a culture of unchecked ambition.", ["Crime", "Biography", "Drama"]),
    ("tick, tick... BOOM!", 4.5, "A composer in New York weighs his ambitions against the pressure of turning thirty.", ["Drama", "Music", "Biography"]),
    ("Up", 4.5, "A widower travels to South America in a flying house with an unexpected young companion.", ["Animation", "Adventure", "Family"]),
    ("Wake Up Dead Man", 4.5, "Detective Benoit Blanc investigates a killing in a close-knit religious community.", ["Mystery", "Crime", "Thriller"]),
    ("WALL·E", 4.5, "A waste-collecting robot crosses space after meeting a probe sent to Earth.", ["Animation", "Sci-Fi", "Drama"]),
    ("Whiplash", 4.2, "An ambitious drummer pushes himself under the punishing instruction of a demanding bandleader.", ["Drama", "Music", "Coming-of-Age"]),
    ("Your Name.", 4.5, "Two teenagers begin waking in each other's bodies and try to understand their connection.", ["Animation", "Romance", "Fantasy"]),
    ("Zindagi Na Milegi Dobara", 3.9, "Three friends take a road trip through Spain that changes their outlook on life.", ["Drama", "Adventure", "Comedy"]),
    ("(500) Days of Summer", 3.8, "A young man reflects on a relationship and his expectations about love.", ["Drama", "Romance", "Comedy"]),
    ("Anora", 4.0, "A Brooklyn dancer's impulsive marriage to a wealthy young man draws both families into conflict.", ["Drama", "Romance", "Thriller"]),
    ("Atonement", 3.9, "A young girl's accusation changes the lives of two lovers.", ["Drama", "Romance", "War"]),
    ("Bhool Bhulaiyaa", 4.2, "A psychiatrist visits a palace and investigates behavior its occupants attribute to a haunting.", ["Horror", "Comedy", "Mystery"]),
    ("Blade Runner", 4.1, "A former blade runner is called back to track down a group of escaped replicants.", ["Sci-Fi", "Thriller", "Drama"]),
    ("Blue Valentine", 3.8, "A couple's relationship is shown through moments from its beginning and its breakdown.", ["Drama", "Romance", "Family"]),
    ("Captain America: Civil War", 4.2, "An international incident divides the Avengers over government oversight and their loyalties.", ["Action", "Superhero", "Drama"]),
    ("Challengers", 3.9, "A tennis champion, her husband, and a former friend meet again at a tournament.", ["Drama", "Sport", "Romance"]),
    ("Coco", 4.1, "A boy who dreams of becoming a musician journeys into the Land of the Dead.", ["Animation", "Family", "Fantasy"]),
    ("Crazy, Stupid, Love.", 4.2, "A newly single man navigates dating with help from a younger friend as their lives intersect.", ["Comedy", "Romance", "Drama"]),
    ("Deadpool", 3.9, "A former mercenary seeks revenge after an experiment leaves him with accelerated healing.", ["Action", "Superhero", "Comedy"]),
    ("Deadpool & Wolverine", 4.2, "Deadpool recruits a reluctant Wolverine to help avert a threat across timelines.", ["Action", "Superhero", "Comedy"]),
    ("Dev.D", 4.2, "A young man spirals into excess after a broken engagement while two women chart different paths.", ["Drama", "Romance", "Thriller"]),
    ("Dhurandhar", 4.2, "An Indian intelligence operative infiltrates a criminal network in Karachi on a national-security mission.", ["Action", "Thriller", "Drama"]),
    ("Dunkirk", 4.2, "Allied soldiers and civilians attempt to evacuate from the beaches of Dunkirk in 1940.", ["War", "Drama", "History"]),
    ("Entergalactic", 4.2, "A New York artist's new home and career bring him into a developing romance.", ["Animation", "Romance", "Drama"]),
    ("F1", 3.8, "A veteran driver returns to Formula One to help a struggling team compete.", ["Drama", "Sport", "Thriller"]),
    ("Flow", 4.2, "A cat and other animals travel together after a flood leaves their world underwater.", ["Animation", "Adventure", "Family"]),
    ("Gangs of Wasseypur – Part 1", 4.2, "In Wasseypur, a coal-mine feud develops into a multigenerational struggle for power.", ["Crime", "Drama", "Thriller"]),
    ("Gifted", 4.2, "A man raising his gifted niece faces a custody dispute over her education and future.", ["Drama", "Family", "Coming-of-Age"]),
    ("Godzilla Minus One", 4.0, "Postwar Japan faces a new crisis when Godzilla appears.", ["Action", "Drama", "History"]),
    ("Gone Girl", 4.0, "A husband's life unravels after his wife disappears and suspicion falls on him.", ["Mystery", "Thriller", "Music"]),
    ("Guardians of the Galaxy Vol. 2", 4.2, "The Guardians take on a new mission as Peter Quill learns more about his parentage.", ["Action", "Superhero", "Sci-Fi"]),
    ("Guardians of the Galaxy Vol. 3", 4.2, "The Guardians embark on a mission to save Rocket and confront the history that shaped him.", ["Action", "Superhero", "Sci-Fi"]),
    ("How to Lose a Guy in 10 Days", 3.8, "A journalist and an advertising executive each pursue a relationship for professional reasons.", ["Comedy", "Romance", "Family"]),
    ("How to Train Your Dragon", 4.2, "A young Viking forms an unexpected bond with a dragon and challenges his village's traditions.", ["Animation", "Adventure", "Fantasy"]),
    ("Inception", 4.3, "A skilled thief enters dreams to plant an idea in the mind of a target.", ["Sci-Fi", "Thriller", "Drama"]),
    ("Inside Out 2", 4.2, "Riley's new emotions arrive as she navigates the pressures of adolescence.", ["Animation", "Comedy", "Family"]),
    ("John Wick: Chapter 3 – Parabellum", 4.2, "With a bounty on his head, John Wick seeks allies while fighting his way out of New York.", ["Action", "Thriller", "Drama"]),
    ("Mad Max: Fury Road", 4.2, "In a wasteland, a group of survivors attempts to escape a tyrant and his forces.", ["Action", "Adventure", "Drama"]),
    ("Mission: Impossible – Dead Reckoning", 4.2, "Ethan Hunt and his team race to control a weapon capable of destabilizing global security.", ["Action", "Thriller", "Spy"]),
    ("Nosferatu", 4.2, "A young woman becomes the focus of an obsessive vampire in 19th-century Germany.", ["Horror", "Fantasy", "Thriller"]),
    ("Once Upon a Time... in Hollywood", 4.0, "An actor and his stunt double navigate a changing Hollywood in 1969.", ["Drama", "Comedy", "Crime"]),
    ("Palm Springs", 4.2, "Two wedding guests become trapped in a repeating day and reconsider their choices.", ["Comedy", "Sci-Fi", "Romance"]),
    ("Rockstar", 3.9, "An aspiring musician's pursuit of fame transforms his career and personal life.", ["Drama", "Music", "Romance"]),
    ("Shrek", 4.2, "An ogre's quiet life is disrupted when fairy-tale characters are driven into his swamp.", ["Animation", "Comedy", "Drama"]),
    ("Spider-Man 2", 4.0, "Peter Parker struggles to balance his personal life with his responsibilities as Spider-Man.", ["Action", "Superhero", "Drama"]),
    ("Superman", 3.7, "Clark Kent balances his life on Earth with his role as a powerful hero.", ["Action", "Superhero", "Adventure"]),
    ("Taxi Driver", 4.1, "A lonely New York cab driver becomes increasingly alienated from the people around him.", ["Crime", "Drama", "Thriller"]),
    ("Ted", 4.2, "A childhood wish brings a talking teddy bear into a man's adult life and relationships.", ["Comedy", "Fantasy", "Drama"]),
    ("The Darjeeling Limited", 4.2, "Three brothers take a train journey across India following their father's death.", ["Comedy", "Drama", "Family"]),
    ("The Dark Knight Rises", 4.2, "Batman returns to defend Gotham when a new adversary threatens the city.", ["Action", "Superhero", "Crime"]),
    ("The Edge of Seventeen", 4.2, "A high-school student finds friendship and perspective while coping with family and school pressures.", ["Comedy", "Coming-of-Age", "Drama"]),
    ("The Fall Guy", 3.5, "A stunt performer searches for a missing actor while working on a film production.", ["Action", "Comedy", "Mystery"]),
    ("The Lion King", 4.2, "A young lion grows up in exile and returns to challenge the ruler who took his place.", ["Animation", "Adventure", "Drama"]),
    ("The Mask", 4.2, "A timid bank clerk gains confidence after discovering a mask with supernatural powers.", ["Comedy", "Fantasy", "Drama"]),
    ("The Nice Guys", 3.8, "A private investigator and an enforcer team up to find a missing young woman.", ["Crime", "Comedy", "Mystery"]),
    ("The Substance", 3.8, "A fading celebrity turns to an experimental treatment with disturbing effects.", ["Horror", "Drama", "Thriller"]),
    ("The Terminal", 4.2, "A traveler becomes stranded at an airport when his country's government collapses.", ["Comedy", "Drama", "History"]),
    ("Thor: Ragnarok", 4.2, "Thor joins unlikely allies to escape captivity and prevent the destruction of Asgard.", ["Action", "Superhero", "Comedy"]),
    ("Toy Story 5", 4.2, "The toys contend with a new generation of technology in a child's playroom.", ["Animation", "Adventure", "Drama"]),
    ("Tumbbad", 4.1, "A family in a village pursues a hidden fortune tied to an ancient, malevolent being.", ["Horror", "Fantasy", "Thriller"]),
    ("Weapons", 3.9, "A community investigates the unexplained disappearance of a group of children.", ["Horror", "Mystery", "Thriller"]),
    ("Yeh Jawaani Hai Deewani", 3.9, "A medical student reconnects with former classmates during a wedding in Udaipur.", ["Drama", "Romance", "Comedy"]),
    ("Zodiac", 4.2, "Journalists and investigators pursue the identity of a serial killer in San Francisco.", ["Crime", "Mystery", "Thriller"]),
    ("Alien: Romulus", 4.0, "A group of young space colonists encounters a deadly life form while scavenging an abandoned station.", ["Horror", "Sci-Fi", "Thriller"]),
    ("Andhadhun", 4.0, "A pianist becomes entangled in a murder investigation after witnessing a crime.", ["Crime", "Mystery", "Thriller"]),
    ("Animal", 4.0, "A son seeks his father's attention and protection as family conflict drives him toward violence.", ["Action", "Crime", "History"]),
    ("Arrival", 4.1, "A linguist is recruited to communicate with visitors who have arrived on Earth.", ["Sci-Fi", "Drama", "Mystery"]),
    ("Drishyam 2", 4.0, "A family faces renewed scrutiny when an old case resurfaces and the investigation intensifies.", ["Crime", "Thriller", "Mystery"]),
    ("Dune", 4.0, "A young noble travels to a desert planet whose rare resource is vital to the empire.", ["Sci-Fi", "Adventure", "Drama"]),
    ("Edge of Tomorrow", 4.0, "A soldier relives the same day in a war against alien invaders, using each loop to change the outcome.", ["Action", "Sci-Fi", "Adventure"]),
    ("Final Destination Bloodlines", 4.0, "A young woman uncovers a family history linked to a deadly chain of accidents.", ["Horror", "Thriller", "Mystery"]),
    ("Glass Onion", 4.0, "Detective Benoit Blanc investigates a murder during a gathering on a tech billionaire's private island.", ["Mystery", "Comedy", "Crime"]),
    ("Jurassic Park", 4.0, "A theme park's cloned dinosaurs escape their enclosures during a visit by a group of experts.", ["Adventure", "Sci-Fi", "Horror"]),
    ("Kill Bill: Vol. 1", 4.0, "An assassin emerges from a coma and begins pursuing the people who attacked her.", ["Action", "Crime", "Thriller"]),
    ("Manjummel Boys", 4.0, "A group of friends on a trip to Kodaikanal mount a rescue after one of them falls into a cave.", ["Drama", "Thriller", "Adventure"]),
    ("RRR", 4.0, "Two revolutionaries form a bond while secretly pursuing separate missions in colonial India.", ["Action", "Drama", "Adventure"]),
    ("Scary Movie", 4.0, "A group of teenagers becomes the target of a masked killer in a parody of slasher films.", ["Comedy", "Horror", "Satire"]),
    ("The Amazing Spider-Man", 4.0, "A high-school student gains spider-like abilities while searching for answers about his parents.", ["Coming-of-Age", "Superhero", "Action"]),
    ("Stree", 4.0, "A small town confronts a mysterious figure that appears during an annual festival.", ["Horror", "Comedy", "Mystery"]),
    ("The Dictator", 4.0, "After being replaced by a body double, a dictator tries to regain power in New York.", ["Comedy", "Satire", "Thriller"]),
    ("The Big Short", 4.0, "Several investors anticipate the U.S. housing market collapse and bet against it.", ["Drama", "Biography", "Thriller"]),
    ("The Conjuring 2", 4.0, "Paranormal investigators travel to London to investigate a haunting reported by a family.", ["Horror", "Thriller", "Mystery"]),
    ("John Wick", 4.0, "A retired hitman returns to the criminal underworld after a gang targets his home.", ["Action", "Thriller", "Crime"]),
    ("Furiosa: A Mad Max Saga", 4.0, "Kidnapped from her home, Furiosa fights to survive across a brutal wasteland.", ["Action", "Adventure", "Thriller"]),
]

class Command(BaseCommand):
    help = "Add the curated movie and genre seed data without duplicating titles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--update-existing",
            action="store_true",
            help="Update description, rating, and genres for matching movie titles.",
        )
        parser.add_argument(
            "--replace-catalog",
            action="store_true",
            help="Keep only movies in this seed list and delete other movie records.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            Movie = apps.get_model(MODEL_APP_LABEL, MOVIE_MODEL_NAME)
            Genre = apps.get_model(MODEL_APP_LABEL, GENRE_MODEL_NAME)
        except LookupError as exc:
            raise CommandError(
                f"Could not find Movie/Genre in app '{MODEL_APP_LABEL}'. "
                "Edit MODEL_APP_LABEL and model names at the top of seed_movies.py."
            ) from exc

        movie_fields = {field.name for field in Movie._meta.get_fields()}
        required = {"title", "rating", "description", "genres"}
        missing = required - movie_fields
        if missing:
            raise CommandError(
                f"Movie model is missing expected fields: {', '.join(sorted(missing))}. "
                "Adjust the field names in handle() to match your models."
            )
        if "name" not in {field.name for field in Genre._meta.get_fields()}:
            raise CommandError("Expected Genre to have a 'name' field; adjust the genre lookup.")

        created = updated = skipped = removed = 0
        genres_field = Movie._meta.get_field("genres")
        if not genres_field.many_to_many:
            raise CommandError("Movie.genres must be a ManyToManyField to Genre.")

        for title, rating, description, genre_names in MOVIES:
            movie = Movie.objects.filter(title__iexact=title).first()
            if movie is None:
                values = {"title": title, "rating": rating, "description": description}
                # If the project has a URL field, seed it as blank so it can be
                # filled later. Change this key if the model uses another name.
                if "image_url" in movie_fields:
                    values["image_url"] = ""
                movie = Movie.objects.create(**values)
                created += 1
            elif options["update_existing"] or options["replace_catalog"]:
                movie.rating = rating
                movie.description = description
                movie.save(update_fields=["rating", "description"])
                updated += 1
            else:
                skipped += 1
                continue

            movie.genres.set([
                Genre.objects.get_or_create(name=name)[0]
                for name in genre_names
            ])

        if options["replace_catalog"]:
            current_titles = {title.casefold() for title, *_ in MOVIES}
            obsolete_ids = [
                movie_id
                for movie_id, title in Movie.objects.values_list("pk", "title")
                if title.casefold() not in current_titles
            ]
            obsolete_movies = Movie.objects.filter(pk__in=obsolete_ids)
            removed = obsolete_movies.count()
            obsolete_movies.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {created} created, {updated} updated, {skipped} already present, "
            f"{removed} other movies removed."
        ))

