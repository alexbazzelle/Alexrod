import axelrodVoice as axlV
# Pick two strategies
players = (axlV.UnnamedStrategy(), axlV.FeldHonestToLiar())


# Set up the match
match = axlV.Match(players, turns=50)
match.show_output(output_mode=2) # Changing output_mode to 5 displays all options


# Play the match and print the scores
match.play()
print( f"{players[0].name}: {match.final_score()[0]},  {players[1].name}: {match.final_score()[1]}")