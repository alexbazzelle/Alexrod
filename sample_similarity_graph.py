import axelrodVoice as axlV


# Define the subject and opponent sets
subjects = [s().name for s in axlV.strategiesNew]
for boring_strats in ["ALTRcx", "ALTRxx", "RAND", "RANDcx", "RANDxx"]: subjects.remove(boring_strats)
#subjects = [axlV.Cooperator().name, axlV.Defector().name, axlV.Grudger().name, axlV.TitForTat().name]
#opponents = [o().name for o in axlV.strategiesTestD + axlV.strategiesTestL]
#opponents = [axlV.Defector().name, axlV.TestDp15().name, axlV.FaceValue().name, axlV.Random().name]
opponents = [o().name for o in axlV.strategiesAll]


# Create the graph object
graph = axlV.SimilarityGraph()

# On first run, generate full data by running matches
#all_strategies = [s() for s in axlV.strategiesAll]
#graph.generate_data(subjects=all_strategies, opponents=all_strategies, last_round=200, filename="full_data.csv")

# Or just generate data for your subjects and opponents
#graph.generate_data(subjects, opponents, last_round=200, filename="full_data.csv")

# If data is already generated, use that.
graph.reload_data("full_data.csv")


# Create clusters using behaviors
graph.partition_by_metric_and_threshold( behaviors=["avg_score"], threshold=0.07, subjects=subjects, opponents=opponents)

# REMARK: Behaviors is an n-tuple. Partitions are made using Euclidean distance and UPGMA.
# ....... To use (cC,cD,dC,dD), set behaviors = ["per_cC", "per_cD", "per_dC", "per_dD"].
#  ......... threshold of .06 to .07 worked well


# Draw the graph. Determine the least visible edge (for coloring). Show and save the graph.
graph.draw_similarity_graph(edge_outlier_thresh=0.4, show=True, filename="similarity_graph.png")
