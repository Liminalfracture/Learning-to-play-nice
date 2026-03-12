# Learning-to-play-nice
Random tools 
# learning-to-play-nice

A collection of utility scripts for managing and organizing large personal file collections.

## dedupe.py
Scans a folder recursively, finds duplicate files by content hash, and moves them to a separate folder for review. Nothing is deleted automatically — you control what goes.

### Usage
1. Edit the three path variables at the top of the script
2. Run: `python dedupe.py`
3. Review `_duplicates` folder and delete in chunks when ready

Built because 20 years of digital life across multiple devices creates chaos. These tools help clean it up.
