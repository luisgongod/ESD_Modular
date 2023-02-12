"""See menu.md for details."""
from time import sleep
sleep(0.8) 

from bootloader import BootloaderMenu

from contrib.bernoulli_gates import BernoulliGates
from contrib.coin_toss import CoinToss
from contrib.consequencer import Consequencer
from contrib.cvecorder import CVecorder

from contrib.diagnostic import Diagnostic
from contrib.hamlet import Hamlet
from contrib.harmonic_lfos import HarmonicLFOs
from contrib.master_clock import MasterClock

from contrib.noddy_holder import NoddyHolder
from contrib.polyrhythmic_sequencer import PolyrhythmSeq
from contrib.poly_square import PolySquare
from contrib.scope import Scope
from calibrate import Calibrate

# Scripts that are included in the menu
EUROPI_SCRIPT_CLASSES = [
    BernoulliGates,
    CoinToss,
    Consequencer,
    CVecorder,
    
    Diagnostic,    
    Hamlet,
    HarmonicLFOs,    
    MasterClock,
    
    NoddyHolder,
    PolyrhythmSeq,
    PolySquare,        
    Scope,
    Calibrate
]


if __name__ == "__main__":
    BootloaderMenu(EUROPI_SCRIPT_CLASSES).main()