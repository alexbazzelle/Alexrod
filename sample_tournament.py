import axelrodVoice as axlV

# Pick the players
players = [s() for s in axlV.strategiesCanon]


# Create the tournament
tournament = axlV.Tournament(players,seed=1)
tournament.use_progress_bar = True

# Play the tournament
results = tournament.play()


# Print results (Rank, Name, Score, Wins)
for playerResult in results.summarise():
    print(f"{playerResult.Rank + 1}, {playerResult.Name}, {playerResult.Median_score:.3f}, {playerResult.Wins:.0f}")