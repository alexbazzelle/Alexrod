from .titfortat import (TitForTat, TitForTatXX, FaceValue, TitForTatCX, TitFor2Tats)
from .rand import (Random, RandomCX, RandomXX)
from .stock import (Liar, Cooperator, Defector, AllBarkNoBite, Alternator, AlternatorCX)
from .grudger import (Grudger, GrudgerCX, GrudgerXX)
from .steinandrapoport import (SteinAndRapoport, SteinAndRapoportFV, SteinAndRapoportCX, SteinAndRapoportXX)
from .graaskamp import (Graaskamp, GraaskampCX, GraaskampXX)
from .grofman import (Grofman, GrofmanCX, GrofmanXX)
from .joss import (JossLiar, JossClassic, JossCX, JossXX)
from .davis import (Davis, DavisCX, DavisXX)
from .tullock import (Tullock, TullockIndependent, TullockCX, TullockXX)
from .tidemanandchieruzzi import (TidemanAndChieruzzi, TidemanAndChieruzziRandom, TidemanAndChieruzziOrdered, TidemanAndChieruzziCX, TidemanAndChieruzziXX)
from .feld import (FeldHonestToLiar, FeldLiarToHonest, FeldCX, FeldXX)
from .shubik import (Shubik, ShubikCX, ShubikXX)
from .downing import (Downing, DowningCX, DowningXX, DowningRCX, DowningRXX)
from .unnamedstrategy import (UnnamedStrategy, UnnamedStrategyCX, UnnamedStrategyXX)
from .testers import *
from .nydegger import (NydeggerCX, NydeggerXX)


strategiesCanon = [FaceValue, Random, Grudger, SteinAndRapoport,
                   Graaskamp, Grofman, JossLiar, Davis, Tullock,
                   TidemanAndChieruzzi, FeldLiarToHonest, Shubik,
                   Downing, UnnamedStrategy, Cooperator]

strategiesSolid = [Cooperator, AllBarkNoBite, Liar, Defector]

strategiesNew = [TitForTat, TitForTatXX, FaceValue, TitForTatCX, TitFor2Tats,
                 Random, RandomCX, RandomXX, Alternator, AlternatorCX,
                 Liar, Cooperator, Defector, AllBarkNoBite,
                 Grudger, SteinAndRapoport,
                 SteinAndRapoportFV,
                 Graaskamp,
                 Grofman,
                 JossLiar, JossClassic,
                 Davis,
                 Tullock, TullockIndependent,
                 TidemanAndChieruzzi, TidemanAndChieruzziRandom, TidemanAndChieruzziOrdered,
                 FeldHonestToLiar, FeldLiarToHonest,
                 Shubik,
                 Downing,
                 UnnamedStrategy]

strategiesXX = [
    TitForTatXX, RandomXX, Alternator, GrudgerXX, SteinAndRapoportXX,
    GraaskampXX, GrofmanXX, JossXX, DavisXX, TullockXX, TidemanAndChieruzziXX,
    FeldXX, ShubikXX, DowningRXX, UnnamedStrategyXX, NydeggerXX
]

strategiesCX = [
    TitForTatCX, RandomCX, AlternatorCX, GrudgerCX, SteinAndRapoportCX,
    GraaskampCX, GrofmanCX, JossCX, DavisCX, TullockCX, TidemanAndChieruzziCX,
    FeldCX, ShubikCX, DowningRCX, UnnamedStrategyCX, NydeggerCX
]

strategiesAll = [TitForTat, TitForTatXX, FaceValue, TitForTatCX, TitFor2Tats,
                 Random, RandomCX, RandomXX, Alternator, AlternatorCX,
                 Liar, Cooperator, Defector, AllBarkNoBite,
                 Grudger, GrudgerCX, GrudgerXX, SteinAndRapoport,
                 SteinAndRapoportFV, SteinAndRapoportCX, SteinAndRapoportXX,
                 Graaskamp, GraaskampCX, GraaskampXX,
                 Grofman, GrofmanCX, GrofmanXX,
                 JossLiar, JossClassic, JossCX, JossXX,
                 Davis, DavisCX, DavisXX,
                 Tullock, TullockIndependent, TullockCX, TullockXX,
                 TidemanAndChieruzzi, TidemanAndChieruzziRandom, TidemanAndChieruzziOrdered,
                 TidemanAndChieruzziCX, TidemanAndChieruzziXX,
                 FeldHonestToLiar, FeldLiarToHonest, FeldCX, FeldXX,
                 Shubik, ShubikCX, ShubikXX,
                 Downing, DowningCX, DowningXX, DowningRCX, DowningRXX,
                 UnnamedStrategy, UnnamedStrategyCX, UnnamedStrategyXX,
                 NydeggerCX, NydeggerXX,
                 TestD7, TestD78, TestD47, TestDp15, TestDp30, TestDp70,
                 TestL7, TestL78, TestL47, TestLp15, TestLp30, TestLp70]

strategiesTestD = [TestD7, TestD78, TestD47, TestDp15, TestDp30, TestDp70]
strategiesTestL = [TestL7, TestL78, TestL47, TestLp15, TestLp30, TestLp70]