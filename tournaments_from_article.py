import axelrodVoice as axlV

players = [s() for s in axlV.strategiesCanon]

"""Uncomment for Table 2 (TIFT tournament)"""
#players.remove(axlV.FaceValue()); players.append(axlV.TitForTat())


"""Uncomment for Table 3 (DOWN alternative definition)"""
#players.remove(axlV.FaceValue()); players.append(axlV.TitForTat())
#players.remove(axlV.Downing()); players.append(axlV.Downing12())


"""Uncomment for TIFTxx (footnote 2)"""
#players.remove(axlV.FaceValue()); players.append(axlV.TitForTatXX())


"""Uncomment for TFTT (footnote 3)"""
#players.remove(axlV.FaceValue()); players.append(axlV.TitForTwoTats())


"""By default, this makes Table 4 (FACE tournament)"""



# Create the tournament
tournament = axlV.Tournament(players,seed=1)
tournament.use_progress_bar = True

# Play the tournament
results = tournament.play()

# Print results (Rank, Name, Score, Wins)
for playerResult in results.summarise():
    print(f"{playerResult.Rank + 1}, {playerResult.Name}, {playerResult.Median_score:.5f}, {playerResult.Wins:.0f}")