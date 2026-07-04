#!/usr/bin/env python3
"""CLI wrapper for the SynapseMD AI risk prediction engine."""

from synapsemd_platform.ai.prediction import AIPredictionEngine, main

__all__ = ["AIPredictionEngine", "main"]

if __name__ == "__main__":
    main()
