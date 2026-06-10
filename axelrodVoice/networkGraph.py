import axelrodVoice as axlVoice
from axelrod import Action
from itertools import combinations
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib import colormaps, colors, pyplot as plt
import networkx as nx
import pandas as pd

class SimilarityGraph:
    def __init__(self):
        self.full_data = pd.DataFrame(columns=[
            "subject", "opponent", "seed", "num_rounds", "first_round", "last_round",
            "per_c", "per_C", "per_cC", "per_cD", "per_dC", "per_dD",
            "avg_score", "avg_net_score"
        ])
        self.subjects: list[str] = []
        self.opponents: list[str] = []
        self.partitions = pd.DataFrame(columns=["s_i"])
        self.frequency_table = pd.DataFrame(columns=[])

    @staticmethod
    def one_match_to_one_entry(match: axlVoice.Match, first_round=1, last_round=200):
        start = first_round - 1
        end = last_round - 1
        total_rounds = last_round - first_round + 1

        # Turn the match into a dataframe
        match_df = pd.DataFrame({
                'a' : [0 if response[0]==Action.C else 1 for response in match.result_voice[start:end]],
                'b' : [0 if response[1] == Action.C else 1 for response in match.result_voice[start:end]],
                'A' : [0 if response[0] == Action.C else 1 for response in match.result[start:end]],
                'B' : [0 if response[1] == Action.C else 1 for response in match.result[start:end]],
                'payoffsA' : [s[0] for s in match.scores()[start:end]],
                'payoffsB': [s[1] for s in match.scores()[start:end]],
                })

        # Get all of the independent variables
        match_header = [
                        match.players[0], # subject
                        match.players[1], # opponent
                        match.seed,       # seed (only compare strats with same seed. that ensures op random is same)
                        total_rounds,     # total number of rounds
                        first_round,      # first_round
                        last_round,       # last_round
                       ]

        # Calculate all of the behaviors
        behaviors = [1 - match_df.a.mean(), # %c
                     1 - match_df['A'].mean(), # %C
                     len(match_df.query('a == 0 and A == 0')) / total_rounds, # %cC
                     len(match_df.query('a == 0 and A == 1')) / total_rounds, # %cD
                     len(match_df.query('a == 1 and A == 0')) / total_rounds, # %dC
                     len(match_df.query('a == 1 and A == 1')) / total_rounds, # %dD
                     match_df.payoffsA.mean(), # avg score
                     (match_df.payoffsA - match_df.payoffsB).mean() # avg net score
                     ]

        return match_header + behaviors

    # Convert a list of subjects and opponents into a full dataframe
    def generate_data(self,
                      subjects: list[axlVoice.Player], opponents: list[axlVoice.Player],
                      first_round=1, last_round=200, seeds = range(5),
                      filename: str | None = None) -> pd.DataFrame:
        #print(f"Total matches: {len(subjects)*len(opponents)*len(seeds)}")

        counter = 0
        for subject in subjects:
            counter += 1
            print(f"...playing subject {counter}/{len(subjects)}")
            self.subjects.append(subject.name)
            for opponent in opponents:
                self.opponents.append(opponent.name)
                for seed_i in seeds:
                    #print(f"Playing {subject} vs {opponent} ({seed_i})")
                    match = axlVoice.Match( (subject, opponent), turns=last_round, seed=seed_i)
                    match.play()
                    entry_row = self.one_match_to_one_entry(match, first_round, last_round)
                    self.full_data.loc[len(self.full_data)] = entry_row

        # Save to csv. Recommended.
        if filename: self.full_data.to_csv(filename, index=False)

        return self.full_data

    # Reload existing data from csv file
    def reload_data(self, filename: str):
        self.full_data = pd.read_csv(filename)
        self.subjects = self.full_data.subject.unique()
        self.opponents = self.full_data.opponent.unique()


    # Build partition set
    def partition_by_metric_and_threshold(self,
                    behaviors: list[str], threshold: float,
                    subjects: list[str] | None = None,
                    opponents: list[str] | None = None,
                    start=1,         end=200):

        # Update subjects and opponents if needed
        if subjects is not None: self.subjects = subjects
        if opponents is not None: self.opponents = opponents

        # Build the filtered dataframe: [ opponent, seed, subject, behavior1, behavior2, ... ]
        filtered_data = (self.full_data.loc[self.full_data['subject'].isin(self.subjects)
                            & self.full_data['opponent'].isin(self.opponents)
                            & (self.full_data['first_round'] == start)
                            & (self.full_data['last_round'] == end)]
                         .sort_values(by=['opponent', 'seed', 'subject'])
                         )[["opponent", "seed", "subject"] + behaviors]

        # Apply clusters to each group.
        all_clusters = pd.DataFrame(columns=["cluster_id","subject"])
        batch_counter = 0; cluster_counter = 0
        for current_opponent in filtered_data["opponent"].unique(): # For each opponent,
            for current_seed in filtered_data["seed"].unique(): # Go through each entry

                # batch_df is [subject, behavior1, behavior2, ...]. Equivalent to ( s, R(s,o) ) for a fixed opponent
                batch_df = (filtered_data
                            .loc[filtered_data["opponent"] == current_opponent]
                            .loc[filtered_data["seed"] == current_seed]
                            )[["subject"] + behaviors]

                # R(s,o). n-tuple
                observed_behavior = batch_df[behaviors].to_numpy()

                # || R(s1,o) - R(s2, o) || for all s1,s2 and a fixed o
                distances = pdist(observed_behavior, metric='euclidean')

                # Compute clusters such that d < threshold for all d in distances
                # (uses UPGMA to make partitions)
                clusters = linkage(distances, method='average') # Compute hierarchical clusters
                cluster_labels = fcluster(clusters, t=threshold, criterion='distance') # Apply threshold and make usable

                # Store clusters
                cluster_ids = [ c + cluster_counter for c in cluster_labels ] # Each one gets a unique id
                cluster_counter += len(set(cluster_ids))
                result_df = pd.DataFrame({"cluster_id": cluster_ids, "subject": batch_df["subject"]}).sort_values(by=["cluster_id", "subject"])

                # Insert into P, the set of S_i's.
                all_clusters = pd.concat([all_clusters,result_df]); batch_counter += 1

        # Remove duplicated clusters, leaving only unique S_i's
        self.partitions = (all_clusters
                           .groupby("cluster_id")["subject"]
                           .apply(frozenset)
                           .reset_index()
                           .set_axis(["cluster_id","s_i"], axis=1)
                           .drop_duplicates(subset="s_i")
                           .drop(columns=["cluster_id"]))

        return self.partitions

    def partitions_to_freq_tbl(self):
        # Count shared partitions
        mate_frequency = {}
        for s_i in self.partitions["s_i"]: # for each set of strategies
            for s1, s2 in combinations(sorted(s_i), 2): # get all 2-way combos
                mate_frequency[ (s1,s2) ] = mate_frequency.get( (s1,s2), 0) + 1 # add them to the dictionary

        # Build frequency table
        self.frequency_table = pd.DataFrame(0, index=self.subjects, columns=self.subjects)
        for (s1, s2), freq in mate_frequency.items():
            self.frequency_table.loc[s1, s2] = freq
            self.frequency_table.loc[s2, s1] = freq
            if s1 == s2: self.frequency_table.loc[s1, s1] = sum( (s1 in s_i) for s_i in self.partitions["s_i"] )

        return self.frequency_table

    # Create the similarity graph
    def draw_similarity_graph(self, node_outlier_thresh: float=0, edge_outlier_thresh: float=0, show=True, filename: str | None = None) -> None:
        # Get the variables
        group_freq_tbl = self.partitions_to_freq_tbl()
        subjects = self.subjects

        # Add edges to graph
        plt.close()
        G = nx.from_pandas_adjacency(group_freq_tbl)

        # Remove nodes with no strong connections
        maximum_weight = 0
        for subject in subjects:
            if group_freq_tbl[subject].max() > maximum_weight: maximum_weight = group_freq_tbl[subject].max()
            if group_freq_tbl[subject].max() < node_outlier_thresh:
                G.remove_node(subject); print(f"...removed node {subject}")

        # Position based on edge weights
        pos = nx.forceatlas2_layout(G, weight="weight", seed=1, linlog=False)

        # Make discrete colormap and apply to edges
        edge_cmap = []
        for i in range (0, maximum_weight + 1):
            scaled_color = i / maximum_weight
            transparency = scaled_color if scaled_color > edge_outlier_thresh else 0
            edge_cmap.append(colormaps["Blues"](scaled_color, alpha=transparency))
        edge_cmap = colors.ListedColormap(edge_cmap)
        edgeColors = [edge_cmap(weight/maximum_weight) for u, v, weight in G.edges(data='weight')]

        # Draw the network graph
        nx.draw_networkx_nodes(G, pos, node_size=430, node_color="powderblue", cmap='tab20', alpha=0.7)
        nx.draw_networkx_edges(G, pos, width=2.5, edge_color=edgeColors)
        nx.draw_networkx_labels(G, pos, font_size=5, font_family="serif", font_weight="bold")

        # Adjust figure settings
        plt.tight_layout()
        fig = plt.gcf()
        fig_scale = 1; fig.set_size_inches(fig_scale * fig.get_figheight(), fig_scale * fig.get_figheight())
        sm = plt.cm.ScalarMappable(cmap=edge_cmap, norm=plt.Normalize(vmin=0, vmax=maximum_weight + 1))
        plt.colorbar(sm, ax=fig.axes, location='right', fraction=0.05, ticks=range(maximum_weight + 1))
        if filename: fig.canvas.manager.set_window_title(filename); fig.savefig(filename, transparent=True, dpi=300)
        if show: plt.show()