import axelrodVoice as axlVoice
from axelrod import Action
from itertools import combinations
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib import colormaps, colors, pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

class SimilarityGraph:
    def __init__(self):
        self.full_data = pd.DataFrame(columns=[
            "subject", "opponent", "seed", "num_rounds", "first_round", "last_round",
            "per_c", "per_C", "per_cC", "per_cD", "per_dC", "per_dD",
            "avg_score", "avg_net_score"
        ])
        self.subjects: list[str] = []
        self.opponents: list[str] = []
        self.partitions = pd.DataFrame(columns=["cluster"])
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
        # FUTURE WORK: Use Principal Component Analysis (PCA) to identify important behaviors

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
                cluster_dendogram = linkage(distances, method='average') # Compute hierarchical clusters
                cluster_labels = fcluster(cluster_dendogram, t=threshold, criterion='distance') # Apply thresholds

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
                           .set_axis(["cluster_id","cluster"], axis=1)
                           .drop_duplicates(subset="cluster")
                           .drop(columns=["cluster_id"]))

        return self.partitions

    def partitions_to_freq_tbl(self):
        count_occurrences = pd.DataFrame(0, index=self.subjects, columns=self.subjects)

        for cluster in self.partitions["cluster"]:
            # Count the total clusters each subject appears in
            for subject in cluster: count_occurrences.loc[subject,subject] += 1
            # Count the shared clusters for each combination of subjects
            for s1, s2 in combinations(cluster, 2):
                count_occurrences.loc[s1, s2] += 1
                count_occurrences.loc[s2, s1] += 1

        # Build the probability frequency table. Index I,J is P(J|I) for chance of sharing cluster.
        # This table is akin to a Markov Chain
        self.frequency_table = pd.DataFrame(0.0, index=self.subjects, columns=self.subjects)
        for s1,s2 in combinations(self.subjects, 2):
            self.frequency_table.loc[s1,s2] = count_occurrences.loc[s1,s2] / count_occurrences.loc[s1,s1]
            self.frequency_table.loc[s2,s1] = count_occurrences.loc[s2,s1] / count_occurrences.loc[s2,s2]

        return self.frequency_table

    # Create the similarity graph
    def draw_similarity_graph(self, edge_outlier_thresh: float=0, show=True, filename: str | None = None) -> None:
        # Get the variables
        group_freq_tbl = self.partitions_to_freq_tbl()

        # Add edges to graph
        plt.close()
        G = nx.from_pandas_adjacency(group_freq_tbl, create_using=nx.DiGraph)
        sorted_edges = sorted(G.edges(data=True), key=lambda edge: edge[2].get('weight', 1))
        G = nx.from_edgelist(sorted_edges, create_using=nx.DiGraph)

        # Position based on edge weights
        pos = nx.forceatlas2_layout(G, weight="weight", seed=1, linlog=False)

        # Create custom colormap
        blank_slots = int(np.floor(edge_outlier_thresh * 256))
        cmap = [[0.0, 0.0, 0.0, 0.0] for _ in range(blank_slots)]
        cmap_colors = colormaps["Blues"](np.linspace(0, 1, 256-blank_slots))
        cmap_colors[:,3] = [min(v + 0.1, 1) for v in np.linspace(0, 1, 256-blank_slots)]
        cmap.extend(cmap_colors)
        edge_cmap = colors.ListedColormap(cmap)
        # Apply cmap to edges
        edgeColors = [edge_cmap(w) for _, _, w in G.edges(data='weight')]

        # Draw the network graph
        nx.draw_networkx_nodes(G, pos, node_size=430, node_color="powderblue", cmap='tab20', alpha=1)
        nx.draw_networkx_edges(G, pos, edge_color=edgeColors, arrows=True, arrowstyle='simple, tail_width=0.09, head_width=0.6, head_length=0.6')
        nx.draw_networkx_labels(G, pos, font_size=5, font_family="serif", font_weight="bold")

        # Adjust figure settings
        plt.tight_layout()
        fig = plt.gcf()
        fig_scale = 2; fig.set_size_inches(fig_scale * fig.get_figheight(), fig_scale * fig.get_figheight())
        colorbar_sm = plt.cm.ScalarMappable(cmap=colors.ListedColormap(cmap_colors), norm=plt.Normalize(vmin=edge_outlier_thresh, vmax=1))
        plt.colorbar(colorbar_sm, ax=fig.axes, location='right')
        if filename: fig.canvas.manager.set_window_title(filename); fig.savefig(filename, transparent=True, dpi=300)
        if show: plt.show()
